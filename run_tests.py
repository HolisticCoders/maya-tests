"""
Heavily based on Chad Vernon's unit testing setup:
https://www.chadvernon.com/blog/unit-testing-in-maya/

Command-line unit test runner for mayapy.

This can be used to run tests from a commandline environment like on a build server.

Usage:
python runmayatests.py -m 2020
"""
from __future__ import absolute_import

import argparse
import os
import platform
import shutil
import stat
import sys
import tempfile
import uuid

from subprocess import CalledProcessError, call

CURRENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
PARENT_REPO_MODULE_PATH = os.path.join(CURRENT_DIR, "..", "modules")


def main():

    parser = argparse.ArgumentParser(description="Runs unit tests for a Maya module")
    parser.add_argument("-m", "--maya", help="Maya version", type=int, default=2020)

    pargs = parser.parse_args()

    env = os.environ.copy()
    mayapy = get_mayapy_executable(pargs.maya)
    command = [
        mayapy,
        os.path.join(CURRENT_DIR, "suite.py"),
    ]

    maya_app_dir = create_clean_maya_app_dir()

    env.update(
        {
            # Create clean prefs
            "MAYA_APP_DIR": maya_app_dir,
            # Clear out any MAYA_SCRIPT_PATH value so we know we're in a clean env.
            "MAYA_SCRIPT_PATH": "",
            # Run the tests in this module.
            "MAYA_MODULE_PATH": ";".join([PARENT_REPO_MODULE_PATH, CURRENT_DIR]),
        }
    )

    try:
        sys.exit(call(command, env=env))
    except CalledProcessError:
        pass
    finally:
        shutil.rmtree(maya_app_dir)


def create_clean_maya_app_dir():
    """Creates a copy of the clean Maya preferences so we can create predictable results.

    @return: The path to the clean MAYA_APP_DIR folder.
    """
    app_dir = os.path.join(CURRENT_DIR, "clean_maya_app_dir")
    temp_dir = tempfile.gettempdir()
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    maya_app_dir = os.path.join(temp_dir, "maya_app_dir{0}".format(str(uuid.uuid4())))

    if os.path.exists(maya_app_dir):
        shutil.rmtree(maya_app_dir, ignore_errors=False, onerror=remove_read_only)
    shutil.copytree(app_dir, maya_app_dir)

    return maya_app_dir


def remove_read_only(func, path, exc):
    """Called by shutil.rmtree when it encounters a readonly file.

    :param func:
    :param path:
    :param exc:
    """
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise RuntimeError("Could not remove {0}".format(path))


def get_maya_location(maya_version):
    """Get the location where Maya is installed."""
    location = None
    if "MAYA_LOCATION" in os.environ.keys():
        location = os.environ["MAYA_LOCATION"]
    else:
        if platform.system() == "Windows":
            location = "C:/Program Files/Autodesk/Maya{0}".format(maya_version)

        elif platform.system() == "Darwin":
            location = "/Applications/Autodesk/maya{0}/Maya.app/Contents".format(
                maya_version
            )

        else:

            location = "/usr/autodesk/maya{0}".format(maya_version)
            if maya_version < 2016:
                # Starting Maya 2016, the default install directory name changed.
                location += "-x64"

    if location is None or not os.path.exists(location):
        raise RuntimeError(
            "Maya {0} is not installed on this system.".format(maya_version)
        )

    return location


def get_mayapy_executable(maya_version):
    """Get the mayapy executable path."""
    python_exe = "{0}/bin/mayapy".format(get_maya_location(maya_version))

    if platform.system() == "Windows":
        python_exe += ".exe"

    return python_exe


if __name__ == "__main__":
    main()
