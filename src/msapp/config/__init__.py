import logging.config
from .loggingProvider import LoggingProvider


logging.config.fileConfig(LoggingProvider.logConfig())
