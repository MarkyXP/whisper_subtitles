import os
import pathlib
import zipfile

import httpx
import loguru
import pip_system_certs.wrapt_requests

pip_system_certs.wrapt_requests.inject_truststore()

_FFMPEG_NAME = "ffmpeg"
_FFPMPEG_PATH = pathlib.Path("tools") / _FFMPEG_NAME

if not _FFPMPEG_PATH.exists():
    loguru.logger.info(f"Downloading ffmpeg zip file...")
    response = httpx.get(
        "https://github.com/ffbinaries/ffbinaries-prebuilt/releases/download/v6.1/ffmpeg-6.1-linux-32.zip",
        follow_redirects=True,
    )
    _FFPMPEG_PATH.parent.mkdir(parents=True, exist_ok=True)
    zip_filename = (
        response.headers["content-disposition"].split("filename=")[-1].strip()
    )
    ZIP_PATH = _FFPMPEG_PATH.parent / zip_filename
    with open(ZIP_PATH, "wb") as f:
        f.write(response.content)
    loguru.logger.info("Extracting ffmpeg binary from zip file...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(_FFPMPEG_PATH.parent)
    loguru.logger.info("Changing ffmpeg into an executable")
    os.chmod(_FFPMPEG_PATH, 0o755)
    os.remove(ZIP_PATH)

    loguru.logger.info(
        f"ffmpeg binary downloaded and saved to {_FFPMPEG_PATH.with_suffix('.zip')}"
    )
else:
    loguru.logger.debug(
        f"ffmpeg binary {_FFMPEG_NAME} already exists at {_FFPMPEG_PATH}, skipping download."
    )
