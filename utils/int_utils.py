# -*- coding: utf-8 -*-
"""
Contains some utility functions for integers in RPython.

Created on Sun Sep 17 16:39:39 2023

@author: Simon Romanowski
"""


def to_16b_string(value):
    """Convert to a 0-padded 16 bit binary string."""
    chars = []
    for _ in range(16):
        chars.insert(0, chr(48 + (value & 1)))
        value = value >> 1
    return "".join(chars)


def to_32x_string(value):
    """Convert to a 0-padded 32 bit hexadecimal string."""
    chars = []
    for _ in range(8):
        low_bits = value & 0xF
        chars.insert(0, chr(48 + low_bits if low_bits < 10
                            else 65 + low_bits - 10))
        value = value >> 4
    return "".join(chars)


def to_64x_string(value):
    """Convert to a 0-padded 64 bit hexadecimal string."""
    chars = []
    for _ in range(16):
        low_bits = value & 0xF
        chars.insert(0, chr(48 + low_bits if low_bits < 10
                            else 65 + low_bits - 10))
        value = value >> 4
    return "".join(chars)


def sign_extend_8_to_32(value):
    """Sign-extend an 8-bit value to 32-bit."""
    if value & 0x80:
        return  value | 0xFFFFFF00
    return value


def sign_extend_8_to_16(value):
    """Sign-extend an 8-bit value to 16-bit."""
    if value & 0x80:
        return  value | 0xFF00
    return value


def sign_extend_16_to_32(value):
    """Sign-extend a 16-bit value to 32-bit."""
    if value & 0x8000:
        return  value | 0xFFFF0000
    return value


def select_bits(value, from_, to=-1):
    """
    Select a certain range of bits from the given value.

    The result will be shifted such that the bit with index ``from_`` now has
    index 0.

    Parameters
    ----------
    value: int
        The value whose bits will be selected.

    from_: int
        Index of the first bit to select.

    to: int, optional
        Index of the last bit to select (inclusive). If not given, this has the
        same value as ``from_``. If this is given and larger than ``from_``,
        their roles are reversed.
    """
    if to == -1:
        to = from_
    elif from_ > to:
        from_, to = to, from_
    diff = to - from_
    mask = ((1 << (diff + 1)) - 1) << from_
    return (value & mask) >> from_
