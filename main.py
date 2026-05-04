"""
Whisper-Subtitles

This script continuously watches a set of directories for new video files,
checks whether they already contain subtitles, and automatically adds
subtitles when necessary.  It also performs an optional deep scan of all
configured folders at startup to ensure that existing files are processed
immediately.
"""

import asyncio
import collections
import pathlib
import time

import loguru
import watchfiles

# Load the config
from app.core import CONFIG
from app.core import logging

logging.init_logging()
loguru.logger.info(f"Starting Whisper Subtitles - {CONFIG.WHISPER_SUBTITLES_VERSION}")

# Download the models
from app.video.add_subtitles import download_tool
from app.video.check_subtitles import download_tool

# Load the libraries needed
from app import speech_to_text
from app import video

# Debounce the monitor - The file is initially detected as added, then modified as the contents are written.
monitor_queue = asyncio.Queue()


def check_and_add_subtitles(video_path: str):
    """
    Checks whether a file:
        1. Is a video file, and
        2. already has subtitles
    It will then add the subtitles if appropriate.

    Args:
        video_path (str): Path to the video file to inspect and potentially annotate.

    Usage:
        >>> check_and_add_subtitles('tests/Assets/1.mp4')

    """
    # Skip if it's not a video
    if not video.is_video(video_path):
        return
    # Skip if the video already has subtitles
    if video.has_subtitles(video_path):
        loguru.logger.debug(
            f"Video file already has subtitles - No action required: {video_path}"
        )
        return
    loguru.logger.info(f"Processing video: {video_path}...")
    duration_sec = video.get_duration(video_path)
    with video.extract_audio(video_path) as audio_path:
        transcript = speech_to_text.transcribe(audio_path, duration_sec, verbose=True)
    with transcript.as_tempfile() as transcript_path:
        video.add_subtitles(video_path, transcript_path)
    loguru.logger.info(f"Subtitles added to video: {video_path}")


async def monitor():
    """Watch configured folders for file system changes.

    - **Added** - call `check_and_add_subtitles` for the new file.
    - **Deleted** - Log a debug message
    - **Modified** - Log a debug message

    Returns:
        None
    """
    async for changes in watchfiles.awatch(*CONFIG.MONITORING_FOLDERS):
        for change in changes:
            change_type = change[0]
            filepath = change[1]
            if change_type == watchfiles.Change.added:
                loguru.logger.info(f"File added to: {filepath} - Added to queue")
                await monitor_queue.put(filepath)
            elif change_type == watchfiles.Change.deleted:
                loguru.logger.debug(f"File deleted: {filepath} - No action required.")
                # await monitor_queue.put(filepath)
            elif change_type == watchfiles.Change.modified:
                loguru.logger.debug(f"File modified: {filepath} - No action required")
                await monitor_queue.put(filepath)


async def monitor_processing():
    """
    Process the files detected as changing by the `monitor` function.
    Note that this implements a `debouncing` mechanism so that files that are
    being actively downloaded (i.e. reprt being added, then constantly being
    modified) isn't processed and subtitles are added mid-download.
    """
    while True:
        filepath = await monitor_queue.get()
        await asyncio.sleep(60)
        # If there are more changes going on with the file
        if filepath in monitor_queue._queue:
            # Drop the duplicates in the queue
            monitor_queue._queue = collections.deque(set(monitor_queue._queue))
            # Loop, get the next file in the queue, and look for ongoing changes again
            continue
        if not pathlib.Path(filepath).exists():
            continue
        # If the file hasn't changed
        loguru.logger.info(f"Processing: {filepath}")
        check_and_add_subtitles(filepath)


async def deep_scan():
    """
    Perform an initial recursive scan of all monitored folders,
    and adds subtitles to all recursive files in those folders.

    Returns:
        None
    """
    if not CONFIG.DEEP_SCAN_ON_STARTUP:
        return
    loguru.logger.info("Deep scan started...")
    queue = asyncio.Queue()
    # Add all folders to the queue
    for folderpath in CONFIG.MONITORING_FOLDERS:
        await queue.put(folderpath)
    # As long as there are folders to process, get the next folder and start processing it
    while True:
        if queue.empty():
            break
        folderpath = await queue.get()
        # Add all files in the folder to the queue
        for entry in pathlib.Path(folderpath).iterdir():
            if entry.is_file():
                check_and_add_subtitles(entry.as_posix())
            elif entry.is_dir():
                await queue.put(entry.as_posix())
    loguru.logger.info("Deep scan completed.")


async def main():
    """Entry point for the asynchronous monitoring and deep-scan tasks.

    Executes `monitor` and `deep_scan` concurrently.

    Returns:
        None
    """
    await asyncio.gather(
        monitor(),
        monitor_processing(),
        deep_scan(),
    )


if __name__ == "__main__":
    while True:
        try:
            with loguru.logger.catch():
                asyncio.run(main())
        except:
            time.sleep(10)
            loguru.logger.info("Restarting...")
