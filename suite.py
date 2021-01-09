from __future__ import absolute_import, with_statement, print_function

import os
import sys
import unittest
from contextlib import contextmanager

CURRENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
PARENT_REPO_DIR = os.path.join(CURRENT_DIR, "..")
TEST_DIR = os.path.join(PARENT_REPO_DIR, "tests")


def session_setup():
    import maya.standalone

    maya.standalone.initialize(name="python")


def session_teardown():
    import maya.standalone

    maya.standalone.uninitialize()


@contextmanager
def mayapy_session():
    session_setup()
    yield
    session_teardown()


def main():
    runner = unittest.TextTestRunner()
    loader = unittest.TestLoader()

    with mayapy_session():
        suite = loader.discover(TEST_DIR)
        return bool(runner.run(suite).errors)


if __name__ == "__main__":
    sys.exit(main())
