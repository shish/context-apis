from __future__ import print_function, absolute_import
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
        log_start("Profiling init", bookmark=True)
        sys.setprofile(_profile)
    else:
        sys.setprofile(None)
        log_endok("Profiling exit")


_profile_decorator_level = 0

def profile():
    """Decorator to enable profiling for a function

    Can be used recursively:

        @ctx.profile()
        def a():
            b()

        @ctx.profile()
        def b():
            print "moo"

        a()

    will turn on profiling from the start of a() to the end of a()
    """
    @decorator
    def _profile(function, *args, **kwargs):
        global _profile_decorator_level
        try:
            if _profile_decorator_level == 0:
                set_profile(True)
            _profile_decorator_level += 1

            d = function(*args, **kwargs)
        finally:
            _profile_decorator_level -= 1
            if _profile_decorator_level == 0:
                set_profile(False)

        return d
    return _profile


#######################################################################
# Lock Debugging
#######################################################################

class LockWrapper(object):
    """
    A class which adds lock wait / acquire / release events to the
    event stream.

    Regular code:

       foo = threading.Lock()
       foo.acquire()
       foo.release()

    Annotated code:

       foo = ctx.LockWrapper(threading.Lock())
       foo.acquire()
       foo.release()
    """
    def __init__(self, lock, name):
        self.lock = lock
        self.lock_id = id(lock)
        self.name = name
        self.counters = threading.local()

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def acquire(self, blocking=1):
        if not hasattr(self.counters, "counter"):
            self.counters.counter = 0
        if blocking and self.counters.counter == 0:
            log_msg(self.lock_id, self.name, "LOCKW")
        ret = self.lock.acquire(blocking)
        if ret and self.counters.counter == 0:
            log_msg(self.lock_id, self.name, "LOCKA")
        self.counters.counter += 1
        return ret

    def release(self):
        self.counters.counter -= 1
        if self.counters.counter == 0:
            log_msg(self.lock_id, self.name, "LOCKR")
        return self.lock.release()
