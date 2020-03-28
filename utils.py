import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler


def set_logger(logger, log_path="log/audio-visualization.log"):
    logger.setLevel(logging.INFO)
    formatter = Formatter("[%(levelname)s] %(asctime)s - %(name)s - %(message)s")

    file_handler = RotatingFileHandler(
        log_path, maxBytes=512 * 1024 * 1024, backupCount=10
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
