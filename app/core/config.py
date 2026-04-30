import dataclasses
import os

import dotenv

dotenv.load_dotenv()

@dataclasses.dataclass
class Config():
    # In case I want to add a ui
    HOST = os.getenv("HOST", "localhost")
    PORT = os.getenv("PORT", "8000")
    # File Locations
    MONITORING_FOLDER = os.getenv("MONITORING_FOLDER", "/monitoring")
    # TTS Model
    TTS_MODEL = os.getenv("TTS_MODEL", "small.en")

CONFIG = Config()