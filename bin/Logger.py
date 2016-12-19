#!/usr/bin/env python

import sys
import logging


# Singleton Logger
class Logger(object):
    filename = ''
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Logger, cls)
            cls._instance = orig.__new__(cls)
            
            # init console logger
            cls.logtoconsole = logging.getLogger('logtoconsole')
            cls.logtoconsole.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            fmt = logging.Formatter('[%(asctime)s] %(levelname)-5s %(message)s')
            ch.setFormatter(fmt)
            cls.logtoconsole.addHandler(ch)

            # if init with filename, set log file handler
            if len(args) > 0 and args[0]:
                # init file logger
                cls.filename = args[0]
                cls.logtofile = logging.getLogger('logtofile')
                cls.logtofile.setLevel(logging.DEBUG)
                fh = logging.FileHandler(cls.filename)
                fh.setFormatter(fmt)
                cls.logtofile.addHandler(fh)
                msg = '<--------- Init logger --------->'
                cls.logtoconsole.info(msg)
                cls.logtofile.info(msg)
        return cls._instance

    @classmethod
    def getinstance(cls):
        return Logger()

    def SetConsoleLogLevel(self, levelname):
        """
        Log Level: 'CRITICAL' > 'ERROR' > 'WARNING' > 'INFO' > 'DEBUG' > 'NOTSET'
        """
        level = logging.getLevelName(levelname)
        if level:
            self.logtoconsole.setLevel(level)
    
    def SetFileLogLevel(self, levelname):
        """
        Log Level: 'CRITICAL' > 'ERROR' > 'WARNING' > 'INFO' > 'DEBUG' > 'NOTSET'
        """
        level = logging.getLevelName(levelname)
        if level and self.filename:
            self.logtofile.setLevel(level)


def INIT_LOGGER(filename = None):
    return Logger(filename)

def LOG_DEBUG(msg):
    log = Logger.getinstance()
    log.logtoconsole.debug(msg)
    if log.filename:
        log.logtofile.debug(msg)

def LOG_INFO(msg):
    log = Logger.getinstance()
    log.logtoconsole.info(msg)
    if log.filename:
        log.logtofile.info(msg)

def LOG_WARNING(msg):
    log = Logger.getinstance()
    log.logtoconsole.warning(msg)
    if log.filename:
        log.logtofile.warning(msg)

def LOG_ERROR(msg):
    log = Logger.getinstance()
    log.logtoconsole.error(msg)
    if log.filename:
        log.logtofile.error(msg)

def LOG_CRITICAL(msg):
    log = Logger.getinstance()
    log.logtoconsole.critical(msg)
    if log.filename:
        log.logtofile.critical(msg)


if __name__ == '__main__':
    logger = INIT_LOGGER('../log/test.log')
    logger.SetConsoleLogLevel('DEBUG')
    logger.SetFileLogLevel('DEBUG')
    
    LOG_CRITICAL('critical message test...')
    LOG_ERROR('error message test...')
    LOG_WARNING('warning message test...')
    LOG_INFO('info message test...')
    LOG_DEBUG('debug message test...')
