# Copyright (c) Alibaba, Inc. and its affiliates.

import logging

_logger = logging.getLogger('nls')

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

_logger.addHandler(NullHandler())
_traceEnabled = False
__LOG_FORMAT__ = '%(asctime)s - %(levelname)s - %(message)s'

__all__=['enableTrace', 'dump', 'error', 'warning', 'debug', 'trace',
        'isEnabledForError', 'isEnabledForDebug', 'isEnabledForTrace']

def enableTrace(traceable, handler=logging.StreamHandler()):
    """
    enable log print

    Parameters
    ----------
    traceable: bool
        whether enable log print, default log level is logging.DEBUG
    handler: Handler object
        handle how to print out log, default to stdio
    """
    global _traceEnabled
    _traceEnabled = traceable
    if traceable:
        _logger.addHandler(handler)
        _logger.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(__LOG_FORMAT__))

def dump(title, message):
    if _traceEnabled:
        _logger.debug('### ' + title + ' ###')
        _logger.debug(message)
        _logger.debug('########################################')

def error(msg):
    _logger.error(msg)

def warning(msg):
    _logger.warning(msg)

def debug(msg):
    _logger.debug(msg)

def trace(msg):
    if _traceEnabled:
        _logger.debug(msg)

def isEnabledForError():
    return _logger.isEnabledFor(logging.ERROR)

def isEnabledForDebug():
    return _logger.isEnabledFor(logging.Debug)

def isEnabledForTrace():
    return _traceEnabled
