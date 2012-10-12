#!/usr/bin/env python

from time import sleep
import context.api as c

@c.log("Printing hello")
def function_a():
    print "hello",
    sleep(0.5)

@c.log("Printing world")
def function_b():
    print "world"
    sleep(0.1)

@c.log("Running program", bookmark=True)
def main():
    function_a()
    function_b()

if __name__ == "__main__":
    c.set_log("file://output.py-decorator.ctxt")
    main()
