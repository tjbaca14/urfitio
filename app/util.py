import logging


def get_logger(name: str) -> logging.Logger:
    """Creates and configures a console-only logger for the application.

    Args:
        name (str): The module path to use as the logger's name.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        return logger

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(log_format)

    logger.addHandler(console_handler)

    return logger
