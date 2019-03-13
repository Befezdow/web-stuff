import logging
from enum import Enum


class LogLevel(Enum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG


class Logger:
    instance = None

    def __call__(self):
        if not self.instance:
            self.instance = Logger()
        return self.instance

    def __init__(self, log_level=LogLevel.DEBUG.value):
        logging.basicConfig(level=log_level, format='%(asctime)s %(processName)s: %(levelname)s: %(message)s')
        self.logger = logging.getLogger('settings-tool')

    def add_log_handler(self, handler):
        fmt = logging.Formatter('%(asctime)s %(processName)s: %(name)s %(levelname)s: %(message)s', None, "%")
        handler.setFormatter(fmt)
        self.logger.addHandler(handler)

    def critical_message(self, message, prefix=''):
        self.logger.critical(message if not prefix else prefix + message)

    def error_message(self, message, prefix=''):
        self.logger.error(message if not prefix else prefix + message)

    def warning_message(self, message, prefix=''):
        self.logger.warning(message if not prefix else prefix + message)

    def info_message(self, message, prefix=''):
        self.logger.info(message if not prefix else prefix + message)

    def debug_message(self, message, prefix=''):
        self.logger.debug(message if not prefix else prefix + message)