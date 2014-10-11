#!/usr/bin/python

import context.api as c
import time

c.set_log("file://output.py-profile.ctxt")
c.set_profile(True)

BOARD_SIZE = 8

class BailOut(Exception):
    pass

def validate(queens):
    time.sleep(0.01)

    left = right = col = queens[-1]
    for r in reversed(queens[:-1]):
        left, right = left - 1, right + 1
        if r in (left, col, right):
            raise BailOut

def add_queen(queens):
    for i in range(BOARD_SIZE):
        test_queens = queens + [i]
        try:
            validate(test_queens)
            if len(test_queens) == BOARD_SIZE:
                return test_queens
            else:
                return add_queen(test_queens)
        except BailOut:
            pass
    raise BailOut

queens = add_queen([])
print queens
print "\n".join(". "*q + "Q " + ". "*(BOARD_SIZE - q - 1) for q in queens)
