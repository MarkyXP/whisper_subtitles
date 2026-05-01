# ffmpeg -i input.mp4 -vf subtitles=subtitles.srt output.mp4

import pathlib
import shutil
import subprocess
import tempfile

from loguru import logger


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
    with tempfile.NamedTemporaryFile(
        suffix=".mp4", delete_on_close=False
    ) as temp_video_file:
        pathlib.Path(temp_video_file.name).unlink()
        # Use FFmpeg to add subtitles to the video
        cmd = [
            "tools/ffmpeg",
            "-i",
            video_path,
            "-f",
            "srt",  # Format - SRT Subtitles
            "-i",
            transcript_path,
            "-c",
            "copy",  # Copies the original video and audio streams without re-encoding
            "-c:s",
            "mov_text",  # Converts the SRT text into the standard subtitle format
            temp_video_file.name,
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        shutil.move(temp_video_file.name, video_file)
        logger.info(f"Subtitles added to {video_path}")


if __name__ == "__main__":
    import doctest
    import shutil

    doctest.testmod(
        verbose=True, optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    )
