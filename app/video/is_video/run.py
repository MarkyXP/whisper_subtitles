import mimetypes


def is_video(file_path):
    """
    Determine whether a given file is a video.

    Checks the MIME type of the file to see if it starts with the string
    ``video``. This is a quick, lightweight test that works for most common
    video formats (mp4, mkv, avi, etc.) as long as the file has a recognised
    extension.

    Args:
        file_path (str): The path to the file that should be examined.

    Returns:
        bool: ``True`` if the file is a video; ``False`` otherwise.

    Usage:
        >>> is_video('tests/Assets/1.mp4')
        True
        >>> is_video('main.py')
        False
        >>> is_video('uv.lock')
        False
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("video")
