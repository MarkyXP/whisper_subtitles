<div align="center">
    <p align="center">

# Whisper Subtitles ![](assets/icon_32.png)

> **Video Subtitles Generation with Whisper**

[![Python](https://img.shields.io/badge/Python%203.14-3776AB?logo=python&logoColor=fff)](https://docs.astral.sh/uv/getting-started/installation/) 
[![watchfiles Badge](https://img.shields.io/badge/watchfiles-546d78?logo=data:img/ico;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAVCAYAAABG1c6oAAAABHNCSVQICAgIfAhkiAAAAbxJREFUOI3tk80vXFEYxn9nMlipmY5rhB3DNZhhUiqtz4mGBokKCxIff0Az0UUldtJlky70T9A0jW4kBAtMfCSEFM1MO+XqxM5CJlwfC9HUTBekqXDPqJWFZ3fe87y/POfNeUWbrz+GgYQQtNZ7eV75BIDJ+SVGpmaN7ACYZZfdLxpo8lb8PXc01ZFgNvN5ctqwxyQDVj/2XKnVPi2VJpQCo1HDadwOOLu8eqXmX/oiBUpn+Gl8ipPTXzTWlPP77IyJuUXG/AtSoGjz9cc+vnuDfnhMRD9gPbTJSiBEZF+XNtpTbZQVFVDszEWxWrCmJNP5euA8YVJiIumKjXTFhis3m56WRoJamNGZeYJa+BLIk6/SXFtFQU7W/z3ZrTpwqw5Wv20wODSMySTo7W7nUWGeNLl0hgAlLidv+14ihCAjTYlnjw8EyLSn3cQGxPk2t9E98A4CzQBdfQNYUx6gWC148lXKigpRHlqkjbt7+6wEQgQ2tojoB+iHR8DFLl/X4FYdND+rxq06LtW//tAY9S8Q+rltnPA6BbUwQS1MicvJq552otEY7z8Ms/Z9U5rcMOG/yrSfr9zObiSelT9IV3rbUe5YSwAAAABJRU5ErkJggg==)](https://watchfiles.helpmanual.io/) 
[![FFmpeg Version](https://img.shields.io/badge/FFmpeg-FFprobe-007808?style=flat&logo=ffmpeg&logoColor=white)](https://ffmpeg.org/download.html) 
[![Faster Whisper Badge](https://img.shields.io/badge/Faster%20Whisper-0081A5?logo=openaigym&logoColor=fff&style=flat)](https://pypi.org/project/faster-whisper/) 
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions%20CI-2088FF?logo=github-actions&logoColor=white)](https://github.com/MarkyXP/whisper-subtitles/tree/master/.github/workflows) 

  </p>
</div>

---------
@Author(s): MarkyXP  

---------

## Summary:
- This tool scans and monitors a list of folders, and uses AI to generate subtitles.
- pathlib and **watchfiles** perform the initial deep scan and ongoing monitoring respectively to find the video files.
- **FFprobe** detects if the video already has subtitles (in which case stop processing the file)
- **FFmpeg** extracts the audio, and **Faster Whisper** performs the transcription
- **FFmpeg** soft codes the subtitle tracks, which can be displayed/hidden in your media player of choice

```yaml
services:
  server:
    image: ghcr.io/markyxp/whisper-subtitles:latest
    container_name: whispersubtitles
    environment:
      - MONITORING_FOLDERS=/tv,/movies,/anime
      - TZ=Australia/Melbourne
    volumes:                                      
      - 'E:/Media/TV Shows:/tv'
      - 'E:/Media/Movies:/movies'
      - 'E:/Media/Anime:/anime'
    restart: unless-stopped
  ```

## AI Usage
All code, documentation, and mistakes were made by me.

## ToDo:
- [ ] Consider adding a healh check for docker
- [x] Fix the parsing of the monitored folders
- [x] Log the app version on startup
- [x] Wrap 'main' in a try/except/log/retry loop
- [ ] Confirm that monitored updates are prioritised over the deep scan
- [ ] Move my media server away from Windows
