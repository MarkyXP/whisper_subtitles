import dataclasses
import re

# Example:
# [00:00:45.840 --> 00:00:50.280]   --It's okay. You are only 15. --No, I'm not. I'm 24.
_LINE_PATTERN = re.compile(r"\[([0-9\:\.]*) --> ([0-9\:\.]*)\](.*)")

@dataclasses.dataclass
class TranscriptLine:
    start_time : int
    end_time : int
    text : str

    @classmethod
    def from_whisper(cls, line : str):
        # Check if the line matches the expected format
        matches = _LINE_PATTERN.findall(line)
        if not matches:
            return None
        # Extract the time and text from the line
        start_time, end_time, text = matches[0]
        return cls(
            start_time=start_time.replace(".", ","),
            end_time=end_time.replace(".", ","),
            text=text.strip()
        )
        