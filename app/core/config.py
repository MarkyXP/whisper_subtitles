import dataclasses
import datetime
import os

import dotenv

dotenv.load_dotenv()


@dataclasses.dataclass
class Config:
    WHISPER_SUBTITLES_VERSION = os.getenv(
        "WHISPER_SUBTITLES_VERSION",
        "DEBUG_" + datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S"),
    )
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()
    # In case I want to add a ui
    HOST = os.getenv("HOST", "localhost")
    PORT = os.getenv("PORT", "8000")
    # File Locations
    MONITORING_FOLDERS = os.getenv("MONITORING_FOLDERS", "/monitoring").split(",")
    DEEP_SCAN_ON_STARTUP = os.getenv("DEEP_SCAN_ON_STARTUP", "True").lower() == "true"
    # TTS Model
    TTS_MODEL = os.getenv("TTS_MODEL", "small.en")
    TTS_DEVICE = os.getenv("TTS_DEVICE", "cpu")


CONFIG = Config()
