"""Logging configuration for Midna"""

import logging
from pathlib import Path


def setup_logging(
    verbose: bool = False, enable_file_logging: bool = False
) -> logging.Logger:
    """Set up logging for Midna with optional file and console output.

    Args:
        verbose: If True, enable console logging at INFO level (default: False)
        enable_file_logging: If True, enable file logging at DEBUG level (default: False)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("midna")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # File handler only if explicitly requested
    if enable_file_logging:
        log_dir = Path.cwd() / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "midna.log"

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Console handler for verbose mode
    if verbose:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(
            logging.Formatter("%(levelname)s: %(message)s")
        )
        logger.addHandler(console_handler)

    return logger
