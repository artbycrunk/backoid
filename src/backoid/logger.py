import copy
import logging
import os
import sys

from . import helpers
from .helpers import MetaSingleton

class Logger(metaclass=MetaSingleton):
    def __repr__(self):
        return f'<Logger {hex(id(self))}>'

    def __init__(self, 
                 logging_level=logging.INFO,
                 logfile=None,
                 logger_name=None):
        self._logging_level = logging_level
        self._log_file = logfile
        self.setup_logging(logging_level=self._logging_level,
                           log_file=self._log_file,
                           logger_name=logger_name)

    @property
    def logging_level(self):
        return self._logging_level

    def debug(self, msg):
        Logger.logger.debug(msg)

    def warn(self, msg):
        Logger.logger.warning(msg)

    def info(self, msg):
        Logger.logger.info(msg)

    def err(self, msg):
        Logger.logger.error(msg)

    @classmethod
    def setup_logging(cls,
                      logging_level=logging.INFO,
                      log_file=None,
                      logger_name=None):
        if logger_name is None:
            (logger_name, _ext) = os.path.splitext(os.path.basename(__file__))

        Logger.logger = logging.getLogger(logger_name)
        Logger.logger.setLevel(logging_level)

        logdir = log_file
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        formatted_date = helpers.get_formatted_date()

        logging.basicConfig(
            filename=f"{logdir}/{logger_name}.{formatted_date}.log",
            level=logging.DEBUG,
            format="[%(asctime)s]: - %(name)s - %(levelname)s - %(message)s",
            datefmt="%H:%M:%S",
        )

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = ColoredFormatter(
            "%(asctime)s -  %(levelname)s - %(name)s - %(module)s - %(message)s"
        )

        Logger.logger.addHandler(handler)
        handler.setFormatter(formatter)


class Color(object):
    NONE = ""
    RESET = "\033[0m"
    RED = "\033[91m"
    RED_BG = "\033[41m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[0;90m"

    NOTSET = 0
    DEBUG = 10
    LOWINFO = 15
    INFO = 20
    WARNING = 30
    ERROR = 40

    @classmethod
    def get_reset(cls, colorized=True):
        if not colorized:
            return ""
        return Color.RESET

    @classmethod
    def get_color(cls, level, colorized=True, bg=False):
        level = self.get_level(level)
        if not colorized:
            return ""
        elif level < Color.DEBUG:
            return ""
        elif Color.DEBUG <= level < Color.LOWINFO:
            return Color.CYAN
        elif Color.LOWINFO <= level < Color.INFO:
            return Color.DARK_GRAY
        elif Color.INFO <= level < Color.WARNING:
            return Color.GREEN
        elif Color.WARNING <= level < Color.ERROR:
            return Color.YELLOW
        elif Color.ERROR <= level:
            return Color.RED if not bg else Color.RED_BG

    @classmethod
    def get_level(cls, level):
        if isinstance(level, int):
            return level
        level_dict = {
            "DEBUG": cls.DEBUG,
            "CRITICAL": cls.LOWINFO,
            "INFO": cls.INFO,
            "WARNING": cls.WARNING,
            "ERROR": cls.ERROR,
        }
        return level_dict.get(level)


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        record = copy.copy(record)
        levelname = record.levelname
        name = record.name
        if self.use_color:
            levelname_color = Color.get_color(levelname) + levelname + Color.get_reset()
            name_color = Color.get_color(levelname) + name + Color.get_reset()
            record.levelname = levelname_color
            record.name = name_color
        return logging.Formatter.format(self, record)
