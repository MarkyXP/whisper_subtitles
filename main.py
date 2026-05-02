"""
Whisper-Subtitles

This script continuously watches a set of directories for new video files,
checks whether they already contain subtitles, and automatically adds
subtitles when necessary.  It also performs an optional deep scan of all
configured folders at startup to ensure that existing files are processed
immediately.

Key components
----------------
* :func:`is_video` - quick MIME‑type check to identify video files.
* :func:`check_and_add_subtitles` - verifies a file’s status and adds
  subtitles via ``app.video`` and ``app.speech_to_text``.
* :func:`monitor` - asynchronous file‑system watcher powered by
  :mod:`watchfiles`.  It reacts to added, deleted, and modified events.
* :func:`deep_scan` - one‑time recursive scan of all monitoring folders
  that enqueues sub‑directories for processing.
* :func:`main` - entry point that runs ``monitor`` and ``deep_scan`` in
  parallel using :mod:`asyncio`.

Configuration
-------------
Configuration values are read from :mod:`app.core.CONFIG`, which must
provide:

* ``MONITORING_FOLDERS`` - list of absolute or relative paths to watch.
* ``DEEP_SCAN_ON_STARTUP`` - ``True`` to run a full scan before monitoring.

Dependencies
------------
* :mod:`watchfiles` - for efficient async directory watching.
* :mod:`asyncio` - for concurrent execution of monitoring and scanning.
* :mod:`loguru` - structured logging.
* :mod:`app.video` - video processing utilities (audio extraction,
  subtitle addition, etc.).
* :mod:`app.speech_to_text` - transcription engine.

Typical usage
-------------
Run the module directly:

```bash
python -m main
```
"""

import asyncio
import mimetypes
import pathlib
import time

import loguru
import watchfiles

# Load the config
from app.core import CONFIG
from app.core import logging

# Download the models
from app.video.add_subtitles import download_tool
from app.video.check_subtitles import download_tool

# Load the libraries needed
from app import speech_to_text
from app import video

logging.init_logging()
loguru.logger.info(
    f"Starting Whisper Subtitles - {CONFIG.WHISPER_SUBTITLES_VERSION}"
)

def is_video(file_path):
    """
    Determine whether a given file is a video.

    Checks the MIME type of the file to see if it starts with the string
    ``video``. This is a quick, lightweight test that works for most common
    video formats (mp4, mkv, avi, etc.) as long as the file has a recognised
    extension.

    Args:
        file_path (str): The path to the file that should be examined.

    Returns:
        bool: ``True`` if the file is a video; ``False`` otherwise.

    Usage:
        >>> is_video('tests/Assets/1.mp4')
        True
        >>> is_video('main.py')
        False
        >>> is_video('uv.lock')
        False
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("video")


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
    if not is_video(video_path):
        return
    # Skip if the video already has subtitles
    if video.has_subtitles(video_path):
        loguru.logger.debug(
            f"Video file already has subtitles - No action required: {video_path}"
        )
        return
    loguru.logger.info(f"Processing video: {video_path}...")
    with video.extract_audio(video_path) as audio_path:
        transcript = speech_to_text.transcribe(audio_path)
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
                loguru.logger.info(f"File added to: {filepath} - Processing")
                check_and_add_subtitles(filepath)
            elif change_type == watchfiles.Change.deleted:
                loguru.logger.debug(f"File deleted: {filepath} - No action required.")
            elif change_type == watchfiles.Change.modified:
                loguru.logger.debug(f"File modified: {filepath} - No action required")


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
        deep_scan(),
        monitor(),
    )


if __name__ == "__main__":
    while True:
        try:
            with loguru.logger.catch():
                asyncio.run(main())
        except:
            time.sleep(10)
            loguru.logger.info("Restarting...")
