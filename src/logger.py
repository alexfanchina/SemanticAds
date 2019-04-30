import pprint
import textwrap
import datetime
from termcolor import colored

class Logger:
    LEVEL_DEBUG = 'd'
    LEVEL_INFO = 'i'
    LEVEL_ERROR = 'e'

    def __init__(self):
        self.level = Logger.LEVEL_DEBUG

    @staticmethod
    def get_prefix(level):
        str_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
        return '[%s %s] ' % (level, str_time)
    
    @staticmethod
    def get_log_hang(prefix, string):
        log = str()
        for i, line in enumerate(string.splitlines(True)):
            if i == 0:
                log += '%s%s' % (prefix, line)
            else:
                log += '%s%s' % (' ' * len(prefix), line)
        return log
    
    def e(self, msg):
        prefix = Logger.get_prefix('E')
        log = Logger.get_log_hang(prefix, msg)
        print(colored(log, 'red'))

    def i(self, msg):
        if self.level not in [Logger.LEVEL_DEBUG, Logger.LEVEL_INFO]:
            return
        prefix = Logger.get_prefix('I')
        print(Logger.get_log_hang(prefix, msg))

    def _d(self, key, value):
        prefix = Logger.get_prefix('D')
        prefix += '%-16s = ' % key
        value_str = str(value)
        log = Logger.get_log_hang(prefix, value_str)
        print(log)
    
    def d(self, *args):
        if self.level not in [Logger.LEVEL_DEBUG]:
            return
        if len(args) == 1:
            msg = args[0]
            prefix = Logger.get_prefix('D')
            print(Logger.get_log_hang(prefix, msg))
        elif len(args) == 2:
            key = args[0]
            value = args[1]
            self._d(key, value)

    def set_level(self, level):
        self.level = level


logger = Logger()
