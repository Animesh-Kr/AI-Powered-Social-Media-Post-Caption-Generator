"""
Secure Logging Configuration

This module sets up secure logging that:
1. Logs detailed errors (including URLs) to private log files
2. Prevents sensitive information from appearing in console/UI
3. Rotates log files to prevent disk space issues
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_secure_logging(
    log_dir: str = "logs",
    log_level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5
):
    """
    Configure secure logging with file rotation.
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        max_bytes: Maximum size of each log file before rotation
        backup_count: Number of backup files to keep
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler for all logs (detailed)
    all_logs_file = log_path / "app.log"
    file_handler = RotatingFileHandler(
        all_logs_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # File handler for errors only (detailed)
    error_logs_file = log_path / "errors.log"
    error_handler = RotatingFileHandler(
        error_logs_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    
    # Console handler (simple, no sensitive data)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(simple_formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)
    
    # Log startup message
    logging.info("="*60)
    logging.info("Secure logging initialized")
    logging.info(f"Log directory: {log_path.absolute()}")
    logging.info(f"All logs: {all_logs_file}")
    logging.info(f"Error logs: {error_logs_file}")
    logging.info("="*60)
    
    return root_logger


class SensitiveDataFilter(logging.Filter):
    """
    Filter to remove sensitive data from log messages.
    Masks API keys, tokens, and other sensitive information.
    """
    
    SENSITIVE_PATTERNS = [
        # API keys (common formats)
        (r'key=[A-Za-z0-9_-]{20,}', 'key=***REDACTED***'),
        (r'apikey=[A-Za-z0-9_-]{20,}', 'apikey=***REDACTED***'),
        (r'api_key=[A-Za-z0-9_-]{20,}', 'api_key=***REDACTED***'),
        
        # Tokens
        (r'token=[A-Za-z0-9_-]{20,}', 'token=***REDACTED***'),
        (r'bearer [A-Za-z0-9_-]{20,}', 'bearer ***REDACTED***'),
        
        # Passwords
        (r'password=[^\s&]+', 'password=***REDACTED***'),
        (r'pwd=[^\s&]+', 'pwd=***REDACTED***'),
    ]
    
    def filter(self, record):
        """Filter sensitive data from log record"""
        import re
        
        # Apply pattern replacements to message
        message = record.getMessage()
        for pattern, replacement in self.SENSITIVE_PATTERNS:
            message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)
        
        # Update record
        record.msg = message
        record.args = ()
        
        return True


def add_sensitive_data_filter():
    """Add sensitive data filter to all handlers"""
    sensitive_filter = SensitiveDataFilter()
    
    for handler in logging.getLogger().handlers:
        # Only add filter to console handlers (not file handlers)
        if isinstance(handler, logging.StreamHandler) and not isinstance(handler, RotatingFileHandler):
            handler.addFilter(sensitive_filter)
    
    logging.info("Sensitive data filter added to console output")


# Example usage
if __name__ == "__main__":
    # Setup logging
    setup_secure_logging()
    add_sensitive_data_filter()
    
    # Test logging
    logger = logging.getLogger(__name__)
    
    logger.info("This is a normal log message")
    logger.warning("This is a warning")
    logger.error("This is an error with API key=AIzaSyDnRO9YsFSeSL38o5g6SGCIePcAmAdKDPQ")
    logger.debug("Debug message with token=abc123def456ghi789")
    
    print("\nCheck the logs/ directory for output files!")
