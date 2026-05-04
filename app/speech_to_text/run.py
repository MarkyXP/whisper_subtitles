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
from tqdm import tqdm

from app.core import CONFIG
from app.speech_to_text.models import TranscriptSegment, Transcript


def transcribe(
    audio_path: str, src_duration: float | None = None, verbose: bool = True
) -> Transcript:
    """
    Transcribe an audio file using Whisper.

    Args:
        audio_path (str): Path to the audio file.
        total_duration (float | None): Total duration of the audio file in seconds - Note if not given verbose will be effectively false
        verbose (bool): Whether to show the progress bar.

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
        CONFIG.TTS_MODEL,
        device=CONFIG.TTS_DEVICE,
        compute_type="int8",
        download_root="tools",
    )
    segments, _ = model.transcribe(audio_path, beam_size=5)

    progress_bar = tqdm(
        total=src_duration, leave=False, disable=not verbose and src_duration
    )
    data = []
    for segment in segments:
        # Skip lines that are descriptions (e.g. '[music]', '[applause]')
        if segment.text.endswith("]"):
            continue
        transcript_segment = TranscriptSegment.from_whisper(
            segment.start, segment.end, segment.text
        )
        data.append(transcript_segment)
        progress_bar.update(int(segment.end - segment.start))

    end_time = time.monotonic()
    progress_bar.close()
    transcription_duration = end_time - start_time
    log_message = f"Whisper took {transcription_duration:.2f} seconds"
    if src_duration:
        log_message += f" (for a {src_duration:.2f} second video, {src_duration / transcription_duration:.2f} x faster than realtime) "
    logger.info(log_message)
    return Transcript(data)


# Tests
if __name__ == "__main__":
    import doctest

    doctest.testmod(
        verbose=True, optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    )
