import os
import pathlib

import httpx
import loguru
import pip_system_certs.wrapt_requests

pip_system_certs.wrapt_requests.inject_truststore()

_WHISPER_NAME = "whisperfile"
_WHISPER_PATH = pathlib.Path("tools") / _WHISPER_NAME

if not _WHISPER_PATH.exists():
    loguru.logger.info(f"Downloading Whisper Speech to Text model: {_WHISPER_NAME}...")
    response = httpx.get("https://github.com/mozilla-ai/llamafile/releases/download/0.10.0/whisperfile-0.10.0", follow_redirects=True)
    _WHISPER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_WHISPER_PATH, "wb") as f:
        f.write(response.content)
    loguru.logger.info("Changing to executable permissions...")
    os.chmod(_WHISPER_PATH, 0o755)
    loguru.logger.info(f"Model downloaded and saved to {_WHISPER_PATH}")


