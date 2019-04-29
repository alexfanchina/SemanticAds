import pprint
import textwrap
import datetime

class Logger:
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

    def i(self, msg):
        prefix = Logger.get_prefix('I')
        print(Logger.get_log_hang(prefix, msg))

    def d(self, key, value):
        prefix = Logger.get_prefix('D')
        prefix += '%-10s = ' % key
        value_str = str(value)
        log = Logger.get_log_hang(prefix, value_str)
        print(log)


logger = Logger()
