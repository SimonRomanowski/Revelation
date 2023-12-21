# -*- coding: utf-8 -*-
"""
Contains the ROM device.

Created on Sat Sep 30 10:25:48 2023

@author: Simon Romanowski
"""

import sys
import os

from utils import int_utils, rpython_utils

from megadrive.devices.device import Device


class Rom64(Device):
    """
    16-bit ROM for 64-bit machines.

    Parameters
    ----------
    program: None | str, optional
        Optional sequence of bytes that represent the program to load into ROM.
        Maximum allowed size is 4MB.
    """

    def __init__(self, program=None):
        self._qwords = []

        if program is not None:
            prog_len = len(program)
            if prog_len > (1024 * 1024 * 4):
                raise rpython_utils.RValueError("Program exceeds maximum size")
            p_index = 0
            shifts = range(56, -1, -8)
            while p_index < prog_len:
                # Combine 8 chars to one integer
                value = 0
                for shift in shifts:
                    if p_index < prog_len:
                        p_value = ord(program[p_index])
                        p_index += 1
                    else:
                        p_value = 0xFF  # Illegal instruction 0xFF to fill rest
                    value |= p_value << shift
                self._qwords.append(value)

    def get_rom_list(self):
        """Get a list of all Quad Words in ROM."""
        return self._qwords

    def read(self, address):
        """
        Read the word at the given address from program memory.

        Parameters
        ----------
        address: int
            A value from 0 to 0x3F_FFFF that indicates the internal address
            of the requested word.
        """
        # Index of the integer that contains the upper byte of the requested
        # word.
        index = address >> 3

        if index < len(self._qwords):
            # The lower-order 2 bits are indices into the actual integers in
            # 'self._qwords'.
            lower = address & 0b111
            raw_value = self._qwords[index]

            if lower == 7:
                # Need to combine the lowes byte with the highest byte from the
                # integer at the next index.
                value = (raw_value & 0xFF) << 8
                if index < len(self._qwords) - 1:  # Avoid index errors
                    raw_next = self._qwords[index + 1]
                else:
                    raw_next = 0xFFFFFFFFFFFFFFFF
                value += raw_next >> 56
            else:
                # Mask selects the bytes to use from 'raw_value'
                shift = 8 * (6 - lower)
                value = (raw_value >> shift) & 0xFFFF
        else:
            # Out-of-bounds access just returns an illegal instruction
            value = 0xFFFF

        return value

    def write(self, address, value):
        pass  # Ignore write

    def dump(self):
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
        address_offset = 0
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


if sys.maxint > ((1<<32) - 1):
    # 64-bit
    Rom = Rom64
else:
    raise RuntimeError("Only 64-bit is supported")