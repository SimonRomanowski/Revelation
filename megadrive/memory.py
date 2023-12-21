# -*- coding: utf-8 -*-
"""
Emulates the Mega Drive memory access.

Created on Fri Sep 15 23:45:24 2023

@author: Simon Romanowski
"""

from utils import rpython_utils

from megadrive.devices import ram, rom, other, device
from utils import int_utils


class MappingError(rpython_utils.ExceptionWithMessage):
    """
    Raised when an address is attempted to be accessed that is not mapped.
    """


class Memory(device.Device):
    """
    Interface to the console's memory access.

    This class considers all memory-mappings.
    The memory uses Big Endian.

    Parameters
    ----------
    program: str | None, optional
        The program to be executed. Is either a string, containing the 68k
        machine code as a sequence of bytes or ``None``, meaning that no
        program will be loaded.

    display_device: None | megadrive.devices.display.Display, optional
        The display device to map to to show graphics. Default is ``None``,
        causing no graphics to be displayed.
        If this is ``None``, it will also cause an error if attempting to
        write to the VDP.
    """

    def __init__(self,
                 program=None,
                 display_device=None,
                 verbose=False,
                 fail_on_invalid=False):
        # Main memory is 64KB (68k memory)
        self._ram = ram.Ram(64*1024)

        self._rom = rom.Rom(program)

        self._io_registers = other.IoRegisters()

        self._tmss = other.TmssRegister()

        self._display = display_device

        self._sound_ram = ram.Ram(1024 * 8)

        self._z80_reset = other.Z80ResetRegister()

        self._z80_bus_request = other.Z80RequestRegister()

        self._verbose = verbose

        self._null_dev = device.NullDevice()

        self._fail_on_invalid = fail_on_invalid

    def get_rom_list(self):
        """Get a list of all Long Words in ROM."""
        return self._rom.get_rom_list()

    def _get_device(self, address):
        """
        Get the device that the given memory address maps to.

        Parameters
        ----------
        address: int
            Value from 0x0 to 0xFF_FFFF that will be mapped to one of the
            console's devices.

        Returns
        -------
        device: megadrive.devices.device.Device
            The I/O device that the address maps to.

        mapped_address: int
            The address to use for the ``read`` method of the given device.
        """
        address &= 0xFFFFFF
        # Cartridge ROM
        if address < 0x400000:
            return (self._rom, address)

        # 68k RAM
        if address >= 0xFF0000:
            return (self._ram, address & 0xFFFF)

        # VDP (display controller)
        if address >= 0xC00000 and address <= 0xC0001F:
            return (self._display, address & 0x1F)

        # IO registers (Controllers etc.)
        if address >= 0xA10000 and address <= 0xA1001F:
            return (self._io_registers, address & 0b11111)

        # Z80 RAM
        if address >= 0xA00000 and address <= 0xA0FFFF:
            return (self._sound_ram, address & 0x1FFF)

        # Z80 bus request
        if address >= 0xA11100 and address <= 0xA11101:
            return (self._z80_bus_request, 0)

        # Z80 reset
        if address >= 0xA11200 and address <= 0xA11201:
            return (self._z80_reset, 0)

        # TMSS register (for licensing check)
        if address >= 0xA14000 and address <= 0xA14003:
            return (self._tmss, 0)

        if self._fail_on_invalid:
            raise MappingError("Memory address 0x%s is not supported."
                               % int_utils.to_32x_string(address))
        return (self._null_dev, 0)

    def get_z80_reset(self):
        """Returns ``True`` iff the Z80 should be reset."""
        return not (self._z80_reset.read(0) & 0x100)

    def get_z80_request(self):
        """Returns ``True`` iff the Z80 bus has been requested."""
        return bool(self._z80_bus_request.read(0) & 0x100)

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
        self._io_registers.set_buttons(player_index,
                                       up, down, left, right,
                                       a, b, c,
                                       start)

    def set_verbose(self, verbose):
        self._verbose = bool(verbose)

    def read(self, address):
        """
        Read the word at the given address in memory.

        Parameters
        ----------
        address: int
            A value from 0x000000 to 0xFFFFFF that indicates the address of the
            requested word. Only the lower 24 bits are considered.
        """
        if self._verbose:
            print("### Mem: reading 0x%s" % int_utils.to_32x_string(address))
        # Address space is 24-bit
        address = address & 0xFFFFFF
        device, adj_address = self._get_device(address)

        result = device.read(adj_address)

        if self._verbose:
            print("### Mem: value 0x%s" % int_utils.to_32x_string(result))

        return result

    def write(self, address, value):
        """
        Write the word at the given address to the given value.

        Parameters
        ----------
        address: int
            The address of the word to be written.

        value: int
            The new value of the word at the given address.
            Only the lower 16 bit are considered.
        """
        if self._verbose:
            print("### Mem: writing 0x%s to 0x%s"
                  % (int_utils.to_32x_string(value),
                     int_utils.to_32x_string(address)))
        # Address space is 24-bit
        address = address & 0xFFFFFF
        value &= 0xFFFF
        device, adj_address = self._get_device(address)
        return device.write(adj_address, value)
