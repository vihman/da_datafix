import logging
from datetime import datetime


def get_version():
    dt = datetime.now()
    return f"{dt.year}.{dt.month}.{dt.day}"


__version__ = get_version()

logging.basicConfig(level=logging.INFO)
