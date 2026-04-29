import json
import pathlib
import subprocess
import time

from loguru import logger

from app.core import CONFIG
from app.stt.models import TranscriptLine


def transcribe(audio_path : str) -> list[TranscriptLine]:
    """
    Transcribe an audio file using Whisper.

    Args:
        audio_path (str): Path to the audio file.
    
    Returns:
        list[TranscriptLine]: List of transcribed lines.
    
    Usage:
        >>> transcribe("tests/Assets/2.mp3")
        [TranscriptLine(start=00:00:00,000, end=00:00:00,839, text="Hello world")]
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
        cmd = [
            "bash", "tools/whisperfile",
            "-m", str(_MODEL_FILE),
            str(audio_file.absolute())
        ]
        start_time = time.monotonic()
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        end_time = time.monotonic()
        data = []
        for line in result.stdout.split("\n"):
            # Look for lines that start with the timestamp
            if not line.startswith("["):
                continue
            # Skip lines that are descriptions (e.g. '[music]', '[applause]')
            if line.endswith(']'):
                continue
            data.append(
                TranscriptLine.from_whisper(line.strip())
            )
        logger.info(f"Whisper took {end_time - start_time:.2f} seconds")
        return data

    except subprocess.CalledProcessError as e:
        logger.error(f"Whisper error: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error("Whisper not found. Please ensure Whisper is installed")
        return False

# Tests
if __name__ == "__main__":
    import doctest
    doctest.testmod(
        verbose=True,
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    )
