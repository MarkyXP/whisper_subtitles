import sys

import loguru

from . import CONFIG


def init_logging() -> None:
    """
    Configure `loguru` based on `CONFIG.LOGGING_LEVEL`.

    Valid LOGGING_LEVEL values:
    """
    # Remove the default sink.
    loguru.logger.remove()
    level = CONFIG.LOGGING_LEVEL if getattr(CONFIG, "LOGGING_LEVEL", None) else "INFO"
    if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"Invalid LOGGING_LEVEL: {level}")
    # Add 'level' sink.
    loguru.logger.add(sys.stderr, level=level)
