import sys
from datetime import datetime
from pathlib import Path
from loguru import logger as _logger


PROJECT_ROOT = Path(__file__).resolve().parent

_print_level = "INFO"

def define_log_level(print_level="INFO", logfile_level="DEBUG", name: str =None):
    """Adjust the log level to the above level"""
    global _print_level
    _print_level = print_level

    current_date = datetime.now()
    format_date = current_date.strftime("%Y%m%d%H%M%S")
    log_name = f"{name}_{format_date}" if name else format_date  # name a log with prefix name

    _logger.remove()
    _logger.add(sys.stderr, level=print_level)
    _logger.add(PROJECT_ROOT/f"logs/{log_name}.log", level=logfile_level)
    return _logger

logger = define_log_level(print_level="DEBUG", logfile_level="ERROR", name="app")

logger.info("Starting application")
logger.error("This is an error!!!")
logger.trace("trace the application") #no print, because the trace is lower than debug


@logger.catch
def catch_error(x):
    50/x


catch_error(0)




