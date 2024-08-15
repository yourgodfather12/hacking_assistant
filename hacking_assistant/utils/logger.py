import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """Setup a logger with the specified name, file, and log level."""
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        logger.setLevel(level)
        logger.addHandler(handler)
    return logger
