import io

class LoggingProvider:
    LOG_CONFIG_FILE = io.StringIO()

    @staticmethod
    def logConfig() -> io.StringIO:
        #noinspection PyTypeChecker
        fo = LoggingProvider.LOG_CONFIG_FILE
        fo.write("""
[loggers]
keys=root

[handlers]
keys=console

[formatters]
keys=generic

[logger_root]
level=DEBUG
handlers=console

[handler_console]
class=StreamHandler
formatter=generic
args=(sys.stdout, )

[handler_logfile]
class=logging.handlers.TimedRotatingFileHandler
formatter=generic
kwargs={'filename': "/var/lib/msapp/msapp.log", 'when': "midnight", 'backupCount': 7, 'encoding': "utf-8"}

[formatter_generic]
format=[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s
datefmt=
class=logging.Formatter
""")
        fo.seek(0)
        return LoggingProvider.LOG_CONFIG_FILE
