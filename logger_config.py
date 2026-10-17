import logging
from pathlib import Path


def setup_logger(log_path):
    """Configure a logger that writes to integrity.log and the console."""
    log_path = Path(log_path)
    logger = logging.getLogger("file_integrity_monitor")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Avoid duplicate handlers if this function is called more than once.
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
