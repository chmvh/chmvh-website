from contextlib import contextmanager
import logging


@contextmanager
def disable_logging(level=logging.ERROR):
    logging.disable(level)
    yield
    logging.disable(logging.NOTSET)
