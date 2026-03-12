import logging
from uvicorn.logging import DefaultFormatter


def setup_logging(level=logging.INFO) -> None:
    handler = logging.StreamHandler()

    handler.setFormatter(
        DefaultFormatter(
            fmt="%(levelprefix)-9s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
            use_colors=True
        )
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if not root_logger.handlers:
        root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)