'''
Logger util
:author: Stefan-Gabriel CHITIC
'''
from datetime import datetime
import os
import logging

_logger = None


def LogCreator(logFilename=None):
    global _logger
    if _logger is None:
        _logger = LogCreatorSingleton(logFilename=logFilename)
    return _logger


class LogCreatorSingleton:

    def __init__(self, logFilename=None):
        self.file = None
        if logFilename:
            self.filename = logFilename
        elif os.environ.get('GARAGE_LOG'):
            self.filename = os.environ.get('GARAGE_LOG')
        else:
            raise IOError("Please specify a log filename")
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as _:
                pass
        self.log = logging.getLogger()

    def write(self, line, status, component_id=None):
        # Format message
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if component_id is None:
            file_line = '[%s] [%s] %s' % (date_now, status, line)
            self.log.info('[%s] %s' % (status, line))

        else:
            file_line = '[%s] [%s-%s] %s' % (date_now, status, component_id,
                                             line)
            self.log.info('[%s-%s] %s' % (status, component_id, line))

        # Append \n for file if there isn't any
        if file_line[-1] != '\n':
            file_line = "%s\n" % file_line

        # We need to open the file each time because this is the only file
        # that may be used by 2 concurrent processes but we still want to
        # write the time when this tentative happened.
        self.file = open(self.filename, 'a+')
        self.file.write(file_line)
        self.file.close()

    def close(self):
        if self.file:
            self.file.close()
