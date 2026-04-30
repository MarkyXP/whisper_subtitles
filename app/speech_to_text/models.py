import contextlib
import dataclasses
import tempfile
import textwrap


def _format_time(time: float):
    """
    Converts a time in seconds to a string formatted as HH:MM:SS,mmm.

    Usage:
        >>> _format_time(0)
        '00:00:00,000'
        >>> _format_time(59)
        '00:00:59,000'
        >>> _format_time(60)
        '00:01:00,000'
        >>> _format_time(3601)
        '01:00:01,000'
        >>> _format_time(45296.789)
        '12:34:56,789'
    """
    seconds = f"{(time % 60):06.3f}".replace(".", ",")
    minutes = f"{int(time // 60) % 60:02d}"
    hours = f"{int(time // 3600):02d}"
    formatted = f"{hours}:{minutes}:{seconds}"
    return formatted


@dataclasses.dataclass
class TranscriptSegment:
    """
    Represents a segment of text as transcription from a Whisper model.
    Key attributes needed by the SRT file are start time, end time, and the text to show.
    """

    start: int
    end: int
    text: str

    @classmethod
    def from_whisper(cls, start_f: float, end_f: float, text: str):
        # Extract the time and text from the line
        start_time = _format_time(start_f)
        end_time = _format_time(end_f)
        formatted_text = text.strip().rstrip(".")

        return cls(start=start_time, end=end_time, text=formatted_text)


class Transcript:
    """
    Receives a list of transcript segments, makes methods available
    to represent this is a built string, or as a temp file
    """

    def __init__(self, transcript_segments: list[TranscriptSegment]):
        self.segments = transcript_segments

    def __str__(self):
        str = "\n\n".join(textwrap.dedent(f"""
                {i+1}
                {segment.start} --> {segment.end}
                {segment.text}""").strip() for i, segment in enumerate(self.segments))
        return str

    @contextlib.contextmanager
    def as_tempfile(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".srt") as transcript_file:
            transcript_file.write(str(self))
            try:
                yield transcript_file.name
            finally:
                # Teardown
                pass


if __name__ == "__main__":
    import doctest

    doctest.testmod(
        verbose=True, optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    )
