# -*- coding: utf-8 -*-
"""
Contains registers of various sizes.

Created on Fri Sep 15 20:01:49 2023

@author: Simon Romanowski
"""

from utils import int_utils


class Register8(object):
    """
    An 8-bit register.

    Parameters
    ----------
    value: int, optional
        The start value of the register. Only the lower 8 bits will be used.
        Default is 0.
    """

    def __init__(self, value=0):
        self._value = value & 0xFF

    def get(self):
        """Get the value of this register."""
        return self._value

    def get_bit(self, index):
        """Get the bit at the given index. 0 is the least significant bit."""
        return int_utils.select_bits(self.get(), index)

    def set(self, value):
        """
        Set this register's value.

        Parameters
        ----------
        value: int
            The new value of the register. Only the lower 8 bits will be used.
        """
        self._value = value & 0xFF

    def set_bits(self, mask, value):
        """
        Set the value of certain bits to the given value.

        The bit at a position will be set to the bit at that position in
        ``value`` if that bit in ``mask`` is 1. Else no change happens.

        Paramters
        ---------
        mask: int
            The bits that should be set equal to the ones in ``value``.

        value: int
            The new values of the bits where ``mask`` is 1.
        """
        self.set((self.get() & ~mask) | (value & mask))


class Register16(Register8):
    """
    A 16-Bit register.

    Parameters
    ---------
    value: int
        The start value of the register. Only the lower 16 bits will be used.
        Default is 0.
    """

    def __init__(self, value=0):
        self._value = value & 0xFFFF

    def set(self, value):
        """
        Set this register's value.

        Parameters
        ----------
        value: int
            The new value of the register. Only the lower 16 bits will be used.
        """
        self._value = value & 0xFFFF

    def get_byte(self):
        """Get the lower-order byte value of this register."""
        return self.get() & 0xFF

    def set_byte(self, value):
        """
        Set this register's lower-order byte value.

        The higher 8 bits remain unchanged.

        Parameters
        ----------
        value: int
            The new value of the lower-order byte of the register. Only the
            lower 8 bits will be used.
        """
        self.set_bits(0xFF, value)


class Register32(Register16):
    """
    A 32-Bit register.

    Parameters
    ---------
    value: int
        The start value of the register. Only the lower 32 bits will be used.
        Default is 0.
    """

    def __init__(self, value=0):
        self._value = value & 0xFFFFFFFF

    def set(self, value):
        """
        Set this register's value.

        Parameters
        ----------
        value: int
            The new value of the register. Only the lower 32 bits will be used.
        """
        self._value = value & 0xFFFFFFFF

    def get_word(self):
        """Get the lower-order word value of this register."""
        return self.get() & 0xFFFF

    def set_word(self, value):
        """
        Set this register's lower-order word value.

        The higher 16 bits remain unchanged.

        Parameters
        ----------
        value: int
            The new value of the lower-order word of the register. Only the
            lower 16 bits will be used.
        """
        self.set_bits(0xFFFF, value)
