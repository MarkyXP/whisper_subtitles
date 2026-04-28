import json
import pathlib
import subprocess
import time

from loguru import logger

from app.core import CONFIG
from app.stt.models import TranscriptLine


def transcribe(audio_path : str) -> bool:
    """
    Check if an MP4 video has embedded subtitle tracks.
    Requires FFmpeg/ffprobe installed and available in PATH.

    Args:
        video_path (str): Path to the MP4 video file.
    
    Returns:
        bool: True if subtitles are present, False otherwise.
    
    Usage:
        >>> transcribe("tests/Assets/1.mp3")
        True
    """
    logger.debug(f"Transcribing: {audio_path}")
    # Validate file path
    audio_file = pathlib.Path(audio_path)
    if not audio_file.is_file():
        logger.error(f"File not found: {audio_path}")
        raise FileNotFoundError(f"File not found: {audio_path}")

    try:
        logger.debug("Running Whisper...")
        _MODEL_FILE = pathlib.Path("tools") / CONFIG.TTS_MODEL
        # Run ffprobe to get stream info in JSON
        # whisperfile -m whisper-tiny.en-q5_1.bin audio.wav
        cmd = [
            "bash", "tools/whisperfile",
            "-m", str(_MODEL_FILE),
            str(audio_file.absolute())
        ]
        start_time = time.monotonic()
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        end_time = time.monotonic()
        data = json.loads(result.stdout)
        logger.info(f"Whisper took {end_time - start_time:.2f} seconds")

        return data

    except subprocess.CalledProcessError as e:
        logger.error(f"ffprobe error: {e.stderr}")
        return False
    except json.JSONDecodeError:
        logger.error("Failed to parse ffprobe output.")
        return False
    except FileNotFoundError:
        logger.error("ffprobe not found. Please ensure FFmpeg is installed and in PATH.")
        return False

# Example usage
if __name__ == "__main__":
    import doctest
    doctest.testmod(
        verbose=True,
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    )
