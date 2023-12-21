# -*- coding: utf-8 -*-
"""
Contains some utilities for working with RPython.

Created on Mon Oct 23 20:37:46 2023

@author: Simon Romanowski
"""

try:
    from rpython.rlib.objectmodel import we_are_translated
except ImportError:
    def we_are_translated():
        return False


class ExceptionWithMessage(Exception):

    def __init__(self, message=""):
        if not we_are_translated():
            Exception.__init__(self, message)
        self._message = message


class RRuntimeError(ExceptionWithMessage):
    pass


class RValueError(ExceptionWithMessage):
    pass


class RIndexError(ExceptionWithMessage):
    pass
