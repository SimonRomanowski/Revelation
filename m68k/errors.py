# -*- coding: utf-8 -*-
"""
Contains error classes for the M68000 emulation.

Created on Fri Thu Sep 21 23:14:23 2023

@author: Simon Romanowski
"""

from utils import rpython_utils


class IllegalInstruction(rpython_utils.ExceptionWithMessage):
    """Raised when an instruction is not part of the instruction set."""


class PrivilegeError(rpython_utils.ExceptionWithMessage):
    """Raised when a priviliged instruction is executed in user mode."""
