import logging
from logging.handlers import RotatingFileHandler


def get_logger():
    log = logging.getLogger("app_logger")
    log.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        "app.log", maxBytes=5_000_000, backupCount=5
    )
    file_handler.setFormatter(formatter)

    log.addHandler(console_handler)
    log.addHandler(file_handler)
    return log


logger = get_logger()
