# ffmpeg -i input.mp4 -vf subtitles=subtitles.srt output.mp4

import pathlib
import subprocess
import tempfile

from loguru import logger

from app.speech_to_text.models import Transcript


def add_subtitles(video_path: str, transcript_path: str) -> None:
    """
    Add subtitles to an MP4 video using FFmpeg.

    Usage:
        >>> add_subtitles("tests/Assets/3.mkv", subtitles)
    """
    logger.debug(f"Adding subtitles to: {video_path}")
    # Validate file path
    video_file = pathlib.Path(video_path)
    transcript_file = pathlib.Path(transcript_path)
    if not video_file.is_file():
        logger.error(f"File not found: {video_path}")
        raise FileNotFoundError(f"File not found: {video_path}")
    if not transcript_file.is_file():
        logger.error(f"File not found: {transcript_file}")
        raise FileNotFoundError(f"File not found: {transcript_path}")
    # Use FFmpeg to add subtitles to the video
    cmd = [
        "tools/ffmpeg",
        "-i",
        video_path,
        "-vf",
        f"subtitles={transcript_path}",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    logger.debug(f"FFmpeg command: {result.stdout}")
    return True


if __name__ == "__main__":
    import doctest
    import shutil

    doctest.testmod(
        verbose=True, optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    )
