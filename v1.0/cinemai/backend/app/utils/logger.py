import logging
from uvicorn.logging import DefaultFormatter


def setup_logging():
    logger = logging.getLogger()

    if logger.handlers:
        return logger

    handler = logging.StreamHandler()
    handler.setFormatter(
        DefaultFormatter(
            fmt="%(levelprefix)-9s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            use_colors=True,
        )
    )

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger