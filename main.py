import loguru
import watchfiles

# Load the config
from app.core import CONFIG

# Download the models
from app.video.add_subtitles import download_tool
from app.video.check_subtitles import download_tool

# Load the libraries needed
from app import speech_to_text
from app import video


def check_and_add_subtitles(video_path: str):
    """
    Check if the video has subtitles and add them if not.
    """
    # Skip if the video already has subtitles
    if video.has_subtitles(video_path):
        loguru.logger.info(
            f"Video file already has subtitles - No action required: {video_path}"
        )
        return
    # Extract the audio & run whisper on it
    with video.extract_audio(video_path) as audio_path:
        transcript = speech_to_text.transcribe(audio_path)
    with transcript.as_tempfile() as transcript_path:
        video.add_subtitles(video_path, transcript_path)


def main():
    for changes in watchfiles.watch(CONFIG.MONITORING_FOLDER):
        for change in changes:
            change_type = change[0]
            filepath = change[1]
            if change_type == watchfiles.Change.added:
                loguru.logger.debug(f"Saw a file added to: {filepath}\n\t- Processing")
                check_and_add_subtitles(filepath)
            elif change_type == watchfiles.Change.deleted:
                loguru.logger.debug(
                    f"Detected a file deleted from: {filepath}\n\t- No action required."
                )
            elif change_type == watchfiles.Change.modified:
                loguru.logger.debug(
                    f"Detected a file modified: {filepath}\n\t- No action required"
                )


if __name__ == "__main__":
    main()
