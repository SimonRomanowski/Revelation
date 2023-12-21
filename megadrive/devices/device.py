# -*- coding: utf-8 -*-
"""
Contains the base class for all devices.

Created on Sat Sep 30 10:20:57 2023

@author: Simon Romanowski
"""

from utils import int_utils, rpython_utils


class ReadOnlyError(Exception):
    """Raised when read-only memory is attempted to be written."""


class Device(object):
    """Base class for a memory-mapped device."""

    def read(self, address):
        """Read the word at the given address."""
        raise rpython_utils.RRuntimeError(
            "Device.read was called with 0x%s"
            % int_utils.to_32x_string(address))

    def write(self, address, value):
        """Write the word at the given address."""
        raise rpython_utils.RRuntimeError(
            "Device.write was called with address 0x%s and value 0x%s"
            % (int_utils.to_32x_string(address),
               int_utils.to_32x_string(value)))


class NullDevice(Device):
    """Device that ignores all read- and write operations."""

    def read(self, address):
        """Always returns 0."""
        return 0

    def write(self, address, value):
        """Does nothing."""
        pass
