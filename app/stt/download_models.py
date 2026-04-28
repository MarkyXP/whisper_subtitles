import pathlib

import httpx
import loguru
import pip_system_certs.wrapt_requests

pip_system_certs.wrapt_requests.inject_truststore()

_MODEL_NAME = "ggml-medium-q5_0.bin"
_MODEL_PATH = pathlib.Path("tools") / _MODEL_NAME

if not _MODEL_PATH.exists():
    loguru.logger.info(f"Downloading Whisper Speech to Text model: {_MODEL_NAME}...")
    response = httpx.get("https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium-q5_0.bin?download=true", follow_redirects=True)
    _MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_MODEL_PATH, "wb") as f:
        f.write(response.content)
    loguru.logger.info(f"Model downloaded and saved to {_MODEL_PATH}")
else:
    loguru.logger.debug(f"Model {_MODEL_NAME} already exists at {_MODEL_PATH}, skipping download.")