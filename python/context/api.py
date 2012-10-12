from __future__ import print_function
from decorator import decorator
from urlparse import urlparse
import time
import platform
import threading
import os
import sys


#######################################################################
# Library API
#######################################################################

_output = None


def set_log(url, append=True):
    """
    set where to log to
    """
    global _output

    if not url:
        _output = None

    elif isinstance(url, basestring):
        mode = "a" if append else "w"

        p = urlparse(url)
        if p.scheme == "file":
            _output = open(p.netloc + p.path, mode, 1)
        else:
            raise NotImplementedError("Python API currently only supports file:// logs")

    else:
        _output = url


def log_msg(function, text, io):
    """
    Log a bit of text with a given type
    """
    tn = threading.current_thread().name.replace(" ", "-")
    if _output:
        print("%f %s %d %s %s %s %s\n" % (
            time.time(),
            platform.node(), os.getpid(), tn,
            io, function, text or ''
        ), file=_output, end='')


def log(text, bookmark=False, exceptions=True, clear=False):
    """Decorator to log event-start at the start of a function
    call and event-end at the end, optionally with a bookmark
    at the start"""
    @decorator
    def _log(function, *args, **kwargs):
        if callable(text):
            _text = text(function, args, kwargs)
        else:
            _text = text
        try:
            if clear:
                log_msg(function.func_name, None, "CLEAR")
            if bookmark:
                log_msg(function.func_name, _text, "BMARK")
            log_msg(function.func_name, _text, "START")
            d = function(*args, **kwargs)
            log_msg(function.func_name, None, "ENDOK")
            return d
        except Exception as e:
            if exceptions:
                log_msg(function.func_name, str(e), "ENDER")
            else:
                log_msg(function.func_name, None, "ENDOK")
            raise
    return _log


#######################################################################
# Library Convenience
#######################################################################

def log_bmark(text=None, function="-"):
    """Shortcut to log some text with the bookmark type"""
    log_msg(function, text, "BMARK")


def log_start(text=None, function="-", bookmark=False, clear=False):
    """Shortcut to log some text with the event-start type"""
    if clear:
        log_msg(function, text, "CLEAR")
    if bookmark:
        log_msg(function, text, "BMARK")
    log_msg(function, text, "START")


def log_endok(text=None, function="-"):
    """Shortcut to log some text with the event-end (success) type"""
    log_msg(function, text, "ENDOK")


def log_ender(text=None, function="-"):
    """Shortcut to log some text with the event-end (error) type"""
    log_msg(function, text, "ENDER")


def log_clear(text=None, function="-"):
    """Shortcut to log some text with the event-clear type"""
    log_msg(function, text, "CLEAR")


#######################################################################
# Automatic Profiling Mode
#######################################################################

def _profile(frame, action, params):
    if action == 'call' and log_msg:
        log_msg(
            "%s:%d" % (frame.f_code.co_filename, frame.f_code.co_firstlineno),
            frame.f_code.co_name,
            "START"
        )
    if action == 'return' and log_msg:
        log_msg(
            "%s:%d" % (frame.f_code.co_filename, frame.f_code.co_firstlineno),
            frame.f_code.co_name,
            "ENDOK"
        )

def set_profile(active=False):
    if active:
        log_start("Profiling init", True)
        sys.setprofile(_profile)
    else:
        sys.setprofile(None)
        log_endok("Profiling exit")
