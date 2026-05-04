import json
import pathlib
import subprocess

from loguru import logger


def get_duration(video_path: str) -> float:
    """
    Extracts the runtime (in seconds) of an MP4 video.

    Args:
        video_path (str): Path to the MP4 video file.

    Returns:
        float: The runtime of the video in seconds.

    Usage:
        >>> get_runtime("tests/Assets/1.mp4")
        5.1

        >>> get_runtime("tests/Assets/2.mp4")
        7.11

        >>> get_runtime("tests/Assets/3.mp4")
        60.1

    """
    logger.debug(f"Getting the runtime of the video: {video_path}")
    # Validate file path
    video_file = pathlib.Path(video_path)
    if not video_file.is_file():
        logger.error(f"File not found: {video_path}")
        raise FileNotFoundError(f"File not found: {video_path}")
    # Extract the runtime
    cmd = [
        "tools/ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    runtime_secs: float = json.loads(result.stdout)
    logger.debug(f"Runtime: {runtime_secs:.2f}")
    return round(runtime_secs, 2)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
