# -*- coding: utf-8 -*-
"""
Contains the RAM device.

Created on Sat Sep 30 10:23:37 2023

@author: Simon Romanowski
"""

import sys
import os

from utils import rpython_utils

from megadrive.devices.device import Device
from utils import int_utils

try:
    from rpython.rlib.objectmodel import we_are_translated
except ImportError:
    def we_are_translated():
        return False


class Ram64(Device):
    """
    16-bit RAM for 64-bit machines.

    Parameters
    ----------
    size: int
        Amount of bytes that the memory should at least support.
    """

    def __init__(self, size):
        self._qwords = [0] * ((size // 8) + (0 if size % 8 == 0 else 1))

    def read(self, address):
        """
        Read the word at the given address from main memory.

        Parameters
        ----------
        address: int
            The address of the word to read. The value is returned in
            Big-Endian format, meaning that the byte at address ``address``
            will be the higher-order byte of the resulting word.
        """
        # Index of the integer that contains the upper byte of the requested
        # word.
        index = address >> 3
        # The lower-order 2 bits are indices into the actual integers in
        # 'self._qwords'.
        lower = address & 0b111

        if index >= len(self._qwords):
            raise rpython_utils.RIndexError(
                "index: 0x%s, address: 0x%s"
                % (int_utils.to_32x_string(index),
                   int_utils.to_32x_string(address)))
        raw_value = self._qwords[index]

        if lower == 7:
            # Need to combine the lowes byte with the highest byte from the
            # integer at the next index.
            value = (raw_value & 0xFF) << 8
            if index < (len(self._qwords) - 1):  # Avoid index errors
                raw_next = self._qwords[index + 1]
                # !!! In translated version, this causes an issue, if the
                # highest byte of 'raw_next' has its MSB set, since '>>' is
                # arithmetic shifting (sign-extension).
                raw_next_is_neg = raw_next < 0
                if raw_next_is_neg:
                    raw_next = ~raw_next
                shifted_next = (raw_next >> 56)
                if raw_next_is_neg:
                    shifted_next = ~shifted_next & 0xFF
                value += shifted_next
        else:
            # Mask selects the bytes to use from 'raw_value'
            shift = 8 * (6 - lower)
            value = (raw_value >> shift) & 0xFFFF

        return value

    def write(self, address, value):
        """
        Write the word at the given address to the given value.

        Parameters
        ----------
        address: int
            The address of the word to write. The value is interpreted in
            Big-Endian format, meaning that the byte at address ``address``
            will be the higher-order byte of ``value``.

        value: int
            The new value of the word at the given address.
            Only the lower 16 bit are considered.
        """
        # Index of the integer that contains the upper byte of the requested
        # word.
        index = address >> 3
        # The lower-order 2 bits are indices into the actual integers in
        # 'self._qwords'.
        lower = address & 0b111

        if index >= len(self._qwords):
            raise rpython_utils.RIndexError(
                "index: 0x%s, address: 0x%s"
                % (int_utils.to_32x_string(index),
                   int_utils.to_32x_string(address)))
        raw_value = self._qwords[index]

        if lower == 7:
            # Need to set the lowest byte here and the highest byte of the
            # integer at the next index
            new_value = (raw_value & 0xFFFFFF00) + (value >> 8)
            if index < (len(self._qwords) - 1):  # Avoid index errors
                next_value = self._qwords[index + 1]
                self._qwords[index + 1] = \
                    (next_value & 0xFFFFFFFFFFFFFF) + ((value & 0xFF) << 56)
        else:
            # Mask selects the bytes to use from 'raw_value'
            shift = 8 * (6 - lower)
            mask = 0xFFFF << shift
            new_value = (raw_value & ~mask) + (value << shift)

        self._qwords[index] = new_value

    def fill_bytes(self, start, amount, value):
        """
        Fill a certain RAM area with the given byte.

        Parameters
        ----------
        start: int
            The start address of the fill operation.

        amount: int
            The amount of bytes to fill.

        value: int
            The byte value to use when filling.
        """
        if amount < 1:
            return

        value = value & 0xFF

        start_index = start >> 3
        start_lower = start & 0b111

        if start_index >= len(self._qwords):
            return

        # End inclusive
        end = start + (amount - 1)
        end_index = end >> 3
        end_lower = end & 0b111

        if we_are_translated():
            only_ones = -1
        else:
            only_ones = 0xFFFFFFFFFFFFFFFF
        # Bit mask for the first quad word
        if start_lower == 0:
            # Special case, since RPython uses arithmetic shifting and r_uint
            # can't be converted to r_int
            start_mask = only_ones
        else:
            start_mask = 0xFFFFFFFFFFFFFF >> ((start_lower - 1) * 8)
        # Bit mask for the last quad word
        # Handle python overflowing to long
        end_mask = only_ones & (only_ones << ((7 - end_lower) * 8))

        # Repeat 'value' over 8 bytes
        fill_value = value | (value << 32)
        fill_value = fill_value | (fill_value << 16)
        fill_value = fill_value | (fill_value << 8)

        if start_index == end_index:
            # Special case:
            # The fill happens entirely in one quad word
            mask = start_mask & end_mask
            orig_value = self._qwords[start_index]
            new_value = (fill_value & mask) | (orig_value & ~mask)
            self._qwords[start_index] = new_value
        else:
            # Handle first and last quad words seperately
            orig_value = self._qwords[start_index]
            new_value = (fill_value & start_mask) | (orig_value & ~start_mask)
            self._qwords[start_index] = new_value

            # Fill everything inbetween to 'fill_value'
            for i in range(start_index + 1, min(end_index, len(self._qwords))):
                self._qwords[i] = fill_value

            if end_index < len(self._qwords):
                orig_value = self._qwords[end_index]
                new_value = (fill_value & end_mask) | (orig_value & ~end_mask)
                self._qwords[end_index] = new_value

    def dump(self, start_address=0):
        """Print this registers content in rows of 16 bytes."""
        # We print 16 bytes per line
        # Print header:
        os.write(
            1,
            "         "
            "| _0 | _1 | _2 | _3 | _4 | _5 | _6 | _7 "
            "| _8 | _9 | _A | _B | _C | _D | _E | _F |\n"
            "---------"
            "|----|----|----|----|----|----|----|----"
            "|----|----|----|----|----|----|----|----|\n")
        print_newline = False
        print_offset = True
        address_offset = start_address
        for qword in self._qwords:
            if print_offset:
                os.write(1, int_utils.to_32x_string(address_offset))
                os.write(1, " | ")
            shift = 56
            while shift >= 0:
                current_byte = (qword >> shift) & 0xFF
                qword_hex = int_utils.to_32x_string(current_byte)[6:8]
                os.write(1, qword_hex)
                os.write(1, " | ")
                shift -= 8
            if print_newline:
                os.write(1, "\n")
            print_newline = not print_newline
            print_offset = not print_offset
            address_offset += 8



class Ram8Bit64(Ram64):
    """
    8-bit RAM for 64-bit machines.

    Parameters
    ----------
    size: int
        Amount of bytes that the memory should at least support.
    """

    def read(self, address):
        """
        Read the byte at the given address from main memory.

        Parameters
        ----------
        address: int
            The address of the byte to read.
        """
        # Index of the integer that contains the upper byte of the requested
        # byte.
        index = address >> 3
        # The lower-order 2 bits are indices into the actual integers in
        # 'self._qwords'.
        lower = address & 0b111

        if index >= len(self._qwords):
            raise rpython_utils.RIndexError(
                "index: 0x%s, address: 0x%s"
                % (int_utils.to_32x_string(index),
                   int_utils.to_32x_string(address)))
        raw_value = self._qwords[index]

        # Mask selects the bytes to use from 'raw_value'
        shift = 8 * (7 - lower)
        value = (raw_value >> shift) & 0xFF

        return value

    def write(self, address, value):
        """
        Write the byte at the given address to the given value.

        Parameters
        ----------
        address: int
            The address of the byte to write. The value is interpreted in

        value: int
            The new value of the byte at the given address.
            Only the lower 8 bit are considered.
        """
        value = value & 0xFF
        # Index of the integer that contains the upper byte of the requested
        # word.
        index = address >> 3
        # The lower-order 2 bits are indices into the actual integers in
        # 'self._qwords'.
        lower = address & 0b111

        if index >= len(self._qwords):
            raise rpython_utils.RIndexError(
                "index: 0x%s, address: 0x%s"
                % (int_utils.to_32x_string(index),
                   int_utils.to_32x_string(address)))
        raw_value = self._qwords[index]

        # Mask selects the bytes to use from 'raw_value'
        shift = 8 * (7 - lower)
        mask = 0xFF << shift
        new_value = (raw_value & ~mask) + (value << shift)

        self._qwords[index] = new_value


if sys.maxint > ((1<<32) - 1):
    # 64-bit
    Ram = Ram64
    Ram8Bit = Ram8Bit64
else:
    raise RuntimeError("Only 64-bit is supported")
