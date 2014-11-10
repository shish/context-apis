import unittest
import threading
from StringIO import StringIO
import sys
sys.path.append("../../")

import context.wsgi as w


class RealWSGIApp(object):
    def __call__(self, environ, start_response):
        self.func_to_find()
        start_response()

    def func_to_find(self):
        pass


class TestContextMiddleware(unittest.TestCase):
    def setUp(self):
        self.buf = StringIO()
        self.app = RealWSGIApp()
        self.m = w.ContextMiddleware(self.app, self.buf)

    def tearDown(self):
        pass

    def test_basic(self):
        environ = {}
        def start_response():
            pass

        self.m(environ, start_response)

        self.assertIn("func_to_find", self.buf.getvalue())

    def test_ignore_static(self):
        environ = {
            "PATH_INFO": "/static/foo.png",
        }
        def start_response():
            pass

        self.m(environ, start_response)

        self.assertNotIn("func_to_find", self.buf.getvalue())
