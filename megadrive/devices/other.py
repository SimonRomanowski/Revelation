# -*- coding: utf-8 -*-
"""
Contains various less complicated device.

Created on Sat Sep 30 10:25:48 2023

@author: Simon Romanowski
"""

from megadrive.devices.device import Device, ReadOnlyError
from megadrive.devices.ram import Ram


VERSION_REGISTER = 0b10100000


class IoRegisters(Device):
    """Memory-mapped version register device."""

    def __init__(self):
        # IO register memory is 32 bytes

        # Mask for reading/writing to the data port
        # 1 = bit is included in reading, 0 = bit is included in writing
        # This mask is reversed from the value written to the control port,
        # since the controllers are read most of the time, meaning that we
        # would have to invert the mask every time.
        self._mask_p1 = 0xFF
        self._mask_p2 = 0xFF
        self._mask_modem = 0xFF

        self._value_p1 = 0xFF
        self._value_p2 = 0xFF
        self._value_modem = 0

        # If set, return the buttons C, B and D-pad. Otherwise, return A and
        # start buttons.
        self._mode_p1 = False
        self._mode_p2 = False

        # Set initial values
        self._version_register = VERSION_REGISTER

    def read(self, address):
        value = 0
        value_shift = 8 if address & 1 else 0

        if address < 2:
            # Version register
            value = self._version_register
        elif address < 4:
            # Player 1 data port
            if self._mode_p1:
                value = self._value_p1 & 0x3F
            else:
                value = (self._value_p1 & 3) | ((self._value_p1 & 0xC0) >> 2)
            value &= self._mask_p1
        elif address < 6:
            # Player 2 data port
            if self._mode_p2:
                value = self._value_p2 & 0x3F
            else:
                value = (self._value_p2 & 3) | ((self._value_p2 & 0xC0) >> 2)
            value &= self._mask_p2
        elif address < 8:
            # Modem data port
            value = self._value_modem & self._mask_modem
        elif address < 0xA:
            # Player 1 control port
            value = ~self._mask_p1 & 0xFF
        elif address < 0xC:
            # Player 2 control port
            value = ~self._mask_p2 & 0xFF
        elif address < 0xE:
            # Modem control port
            value = ~self._mask_modem & 0xFF

        # TODO support the other registers

        return (value << value_shift) & 0xFFFF

    def write(self, address, value):
        if address & 1:
            value = value >> 8
        if address < 2:
            # Version register
            pass
        elif address < 4:
            # Player 1 data port
            self._mode_p1 = bool(value & 0x40)
        elif address < 6:
            # Player 2 data port
            self._mode_p2 = bool(value & 0x40)
        elif address < 8:
            # Modem data port
            pass
        elif address < 10:
            # Player 1 control port
            self._mask_p1 = ~value & 0xFF
        elif address < 12:
            # Player 2 control port
            self._mask_p2 = ~value & 0xFF
        elif address < 14:
            # Modem control port
            self._mask_modem = ~value & 0xFF

    def set_buttons(self,
                    player_index,
                    up, down, left, right,
                    a, b, c,
                    start):
        """
        Set the buttons of the controller for the given player.

        Parameters
        ----------
        player_index: int
            The index of the player to set the buttons for.
            1 means player 1, 2 means player 2.

        up, down, left, right, a, b, c, start: bool
            The value for each button on the controller.
            ``True`` means the button is pressed.
        """
        # We use the "SACBRLDU" scheme
        # A 0 bit means the button is pressed.
        value = ~(
            (start << 7)
            | (a << 6)
            | (c << 5)
            | (b << 4)
            | (right << 3)
            | (left << 2)
            | (down << 1)
            | up) & 0xFF
        if player_index == 1:
            self._value_p1 = value
        else:
            self._value_p2 = value


class TmssRegister(Device):
    """Simulates the TMSS"""

    def read(self, address):
        return 0  # Don't care


    def write(self, address, value):
        # In the actual console, this is used as copyright protection
        # Usually "SEGA" is written to this
        pass  # Don't care


class Z80ResetRegister(Device):
    """Simulates the reset register for the Z80 CPU."""

    def __init__(self):
        Device.__init__(self)
        self._is_resetting = False

    def read(self, address):
        return 0 if self._is_resetting else 0x100

    def write(self, address, value):
        self._is_resetting = not (value & 0x100)


class Z80RequestRegister(Device):
    """Simulate the Z80 bus request."""

    def __init__(self):
        Device.__init__(self)
        self._accessible = True

    def read(self, address):
        return 0 if self._accessible else 0x100

    def write(self, address, value):
        self._accessible = bool(value & 0x100)
