import pathlib
import zipfile

import httpx
import loguru
import pip_system_certs.wrapt_requests

pip_system_certs.wrapt_requests.inject_truststore()

_FFPROBE_NAME = "ffprobe"
_FFPROBE_PATH = pathlib.Path("tools") / _FFPROBE_NAME

if not _FFPROBE_PATH.exists():
    loguru.logger.info(f"Downloading ffprobe zip file...")
    response = httpx.get("https://github.com/ffbinaries/ffbinaries-prebuilt/releases/download/v6.1/ffprobe-6.1-linux-32.zip", follow_redirects=True)
    _FFPROBE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ZIP_PATH = _FFPROBE_PATH.parent / response.headers['content-disposition'].split('filename=')[-1].strip()
    with open(ZIP_PATH, "wb") as f:
        f.write(response.content)
    loguru.logger.info(f"Extracting ffprobe binary from zip file...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(_FFPROBE_PATH.parent)
    
    loguru.logger.info(f"ffprobe binary downloaded and saved to {_FFPROBE_PATH}")
else:
    loguru.logger.debug(f"ffprobe binary {_FFPROBE_NAME} already exists at {_FFPROBE_PATH}, skipping download.")