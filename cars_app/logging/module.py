import logging


def init_logger(name: str) -> None:
    """Init logger."""
    logger = logging.getLogger(name)
    logging_template = '%(levelname)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(logging_template))
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)


init_logger(__name__)
logger = logging.getLogger(__name__)
