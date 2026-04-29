import json
import pathlib
import subprocess

from loguru import logger


def has_subtitles(video_path : str) -> bool:
    """
    Check if an MP4 video has embedded subtitle tracks.
    Requires FFmpeg/ffprobe installed and available in PATH.

    Args:
        video_path (str): Path to the MP4 video file.
    
    Returns:
        bool: True if subtitles are present, False otherwise.
    
    Usage:
        >>> has_subtitles("tests/Assets/3.mkv")
        True
        >>> has_subtitles("tests/Assets/2.mp4")
        False
    """
    logger.debug(f"Checking for subtitles in: {video_path}")
    # Validate file path
    video_file = pathlib.Path(video_path)
    if not video_file.is_file():
        logger.error(f"File not found: {video_path}")
        raise FileNotFoundError(f"File not found: {video_path}")
    #if video_file.suffix.lower() != ".mp4":
    #    raise ValueError("Only .mp4 files are supported in this check.")

    try:
        logger.debug("Running ffprobe to check for subtitle streams...")
        # Run ffprobe to get stream info in JSON
        cmd = [
            "tools/ffprobe", "-v", "error",
            "-select_streams", "s",  # 's' = subtitle streams
            "-show_entries", "stream=index:stream_tags=language",
            "-of", "json", str(video_file.absolute())
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        # If there are subtitle streams, return True
        logger.debug(f"Subtitle streams found: {len(data.get('streams', []))}")
        has_subtitles = bool(data.get("streams"))
        return has_subtitles

    except subprocess.CalledProcessError as e:
        logger.error(f"ffprobe error: {e.stderr}")
        return False
    except json.JSONDecodeError:
        logger.error("Failed to parse ffprobe output.")
        return False
    except FileNotFoundError:
        logger.error("ffprobe not found. Please ensure FFmpeg is installed")
        return False

# Testing
if __name__ == "__main__":
    import doctest
    doctest.testmod(
        verbose=True,
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    )
