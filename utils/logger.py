import logging

def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """Setup a logger with the specified name, file, and log level."""
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        logger.setLevel(level)
        logger.addHandler(handler)
    return logger
