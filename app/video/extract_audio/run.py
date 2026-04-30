"""

> ffmpeg -i input_video.mp4 -vn -acodec copy output_audio.m4a

"""

import contextlib
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Generator

from loguru import logger


@contextlib.contextmanager
def extract_audio(video_path: str) -> Generator[str, str, str]:
    """
    Extracts the audio from an MP4 video using FFmpeg as a .wav,
    file and yields the audio filepath

    Args:
        - video_path (str): Path to the video file

    Yields:
        - str: Path to the .wav audio file

    Usage:
        >>> with extract_audio("tests/Assets/1.mp4") as audiofile:
        ...     print(audiofile)
        /tmp/....wav
    """
    logger.debug(f"Extracting audio from: {video_path}")
    # Validate file path
    video_file = Path(video_path)
    if not video_file.is_file():
        logger.error(f"File not found: {video_path}")
        raise FileNotFoundError(f"File not found: {video_path}")
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio_file:
        os.unlink(temp_audio_file.name)
        # Run ffprobe to extract the audio
        cmd = [
            "tools/ffmpeg",
            "-i",
            video_path,
            temp_audio_file.name,
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.debug(f"Extracted audio saved to: {temp_audio_file.name}")
        try:
            yield temp_audio_file.name
        finally:
            # Teardown
            os.unlink(temp_audio_file.name)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
