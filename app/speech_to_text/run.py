"""
#==========================================================
# ** Run Speech to Transcription service
#---------------------------------------------------------
# Author: MarkyXP
#==========================================================
"""

import pathlib
import time

from faster_whisper import WhisperModel
from loguru import logger

from app.core import CONFIG
from app.speech_to_text.models import TranscriptSegment, Transcript


def transcribe(audio_path: str) -> Transcript:
    """
    Transcribe an audio file using Whisper.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        list[TranscriptLine]: List of transcribed lines.

    Usage:
        >>> transcribe("tests/Assets/2.mp3")
        [TranscriptSegment(start='00:00:00,000', end='00:00:02,000', text='Hello world')]
    """
    logger.debug(f"Transcribing: {audio_path}")
    # Validate file path
    audio_file = pathlib.Path(audio_path)
    if not audio_file.is_file():
        logger.error(f"File not found: {audio_path}")
        raise FileNotFoundError(f"File not found: {audio_path}")

    logger.debug("Running Whisper...")
    start_time = time.monotonic()
    model = WhisperModel(
        CONFIG.TTS_MODEL, device="cpu", compute_type="int8", download_root="tools"
    )
    segments, _ = model.transcribe(audio_path, beam_size=5)

    data = []
    for segment in segments:
        # Skip lines that are descriptions (e.g. '[music]', '[applause]')
        if segment.text.endswith("]"):
            continue
        data.append(
            TranscriptSegment.from_whisper(segment.start, segment.end, segment.text)
        )

    end_time = time.monotonic()
    logger.info(f"Whisper took {end_time - start_time:.2f} seconds")
    return Transcript(data)


# Tests
if __name__ == "__main__":
    import doctest

    doctest.testmod(
        verbose=True, optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    )
