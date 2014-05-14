import unittest
import threading
from StringIO import StringIO
import sys
sys.path.append("../../")

import context.api as c


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.buf = StringIO()
        c.set_log(self.buf)

    def tearDown(self):
        pass

    def test_basic(self):
        pass

    def test_set_log(self):
        c.set_log("file://test.ctxt")  # relative
        c.set_log("file:///tmp/test.ctxt")  # absolute
        self.assertRaises(NotImplementedError, c.set_log, "tcp://localhost:123")
        self.assertRaises(NotImplementedError, c.set_log, "udp://localhost:123")
        c.set_log(None)  # turn off logging

    def test_log_msg(self):
        c.log_msg("func", "message", "WAFFLE")

    def test_log(self):
        @c.log("Doing a Thing", clear=True, bookmark=True, exceptions=True)
        def funcy():
            pass
        funcy()

    def test_log_bmark(self):
        c.log_bmark("boooookmark")

    def test_log_start(self):
        c.log_start("starto")
        c.log_start("starto", clear=True)
        c.log_start("starto", bookmark=True)

    def test_log_endok(self):
        c.log_endok("ended ok")

    def test_log_ender(self):
        c.log_ender("ended with error")

    def test_log_clear(self):
        c.log_clear()

    def test_set_profile(self):
        try:
            c.set_profile(True)
            def funcy2():
                pass
            funcy2()
        finally:
            c.set_profile(False)

    def test_profile(self):
        @c.profile()
        def funcy():
            pass
        funcy()

    def test_lock(self):
        lock = c.LockWrapper(threading.Lock(), "My Lock")

        self.assertTrue(lock.acquire(False))
        lock.release()

        self.assertTrue(lock.acquire(True))    # blocking
        self.assertFalse(lock.acquire(False))  # non-blocking, return fail immediately
        lock.release()
