import logging

LOG_FORMATTER = "[%(asctime)s] [%(name)s] [%(levelname)s] : %(message)s"

logger = logging.getLogger("novel_notify")
logger.setLevel(logging.INFO)

_sHandler = logging.StreamHandler()
_sHandler.setLevel(logging.INFO)
_sHandler.setFormatter(logging.Formatter(LOG_FORMATTER))

logger.addHandler(_sHandler)
