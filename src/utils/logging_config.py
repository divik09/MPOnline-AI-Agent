"""Structured logging configuration using structlog."""
import sys
import logging
import structlog
from pathlib import Path
from src import config


def setup_logging():
    """Configure structlog for production-quality logging."""
    
    # Ensure log directory exists
    log_file = Path(config.LOG_FILE_PATH)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure structlog processors
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    # Add JSON formatting for production
    if config.LOG_LEVEL == "DEBUG":
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.INFO if config.LOG_LEVEL == "INFO" else
            logging.DEBUG if config.LOG_LEVEL == "DEBUG" else
            logging.WARNING if config.LOG_LEVEL == "WARNING" else
            logging.ERROR if config.LOG_LEVEL == "ERROR" else
            logging.INFO
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=open(log_file, "a")),
        cache_logger_on_first_use=True,
    )
    
    # Also log to console
    console_handler = structlog.PrintLoggerFactory(file=sys.stdout)
    
    return structlog.get_logger()


# Global logger instance
logger = setup_logging()
