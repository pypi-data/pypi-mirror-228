# -*- coding: utf-8 -*-

"""

serializable_trees.__main__

Command line interface

Copyright (C) 2023 Rainer Schwarzbach

This file is part of serializable_trees.

serializable_trees is free software:
you can redistribute it and/or modify it under the terms of the MIT License.

serializable_trees is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import sys

from serializable_trees import __version__


def main() -> int:
    """Print the version number"""
    print(__version__)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # NOT TESTABLE


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
