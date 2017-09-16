import os
import sys
import inspect


def getdir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def printinfo(value):
    print "call from " + inspect.stack()[1][1] + "'s function " + inspect.stack()[1][3] + " at line " + str(inspect.stack()[1][2]) + ":" + str(value)


HOME_DIR = getdir()
