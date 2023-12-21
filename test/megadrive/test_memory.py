# -*- coding: utf-8 -*-
"""
Test the megadrive.memory module.

Created on Sat Sep 16 00:50:09 2023

@author: Simon Romanowski
"""

import unittest

import megadrive.memory as mem


class TestMemory(unittest.TestCase):

    # TODO add negative tests

    def test_init(self):
        mem.Memory()

    def test_read_ram(self):
        m = mem.Memory()

        for i in range(0x10000):
            value = m._ram.read(i)
            assert value == 0, (
                "Value at ram address 0x{:X} was expected to be 0 "
                "but was {}".format(i, value))

    def test_write_ram(self):
        m = mem.Memory()

        set_values = {
            0: 0xABCD,
            0x123: 0x5678,
            0xFFFF: 0x1234,
        }

        expect_values = {
            0: 0xABCD,
            1: 0xCD00,

            0x122: 0x56,
            0x123: 0x5678,
            0x124: 0x7800,

            0xFFFE: 0x12,
            # Note that the lower byte has been ignored
            0xFFFF: 0x1200,
        }

        for address, value in set_values.items():
            m._ram.write(address, value)

        for address in range(0x10000):
            ex_value = expect_values.get(address, 0)
            value = m._ram.read(address)
            assert value == ex_value, (
                "Expected RAM address 0x{:X} to return 0x{:X}, "
                "but got 0x{:X}.\n"
                "Memory:\n"
                "_ram.read(address - 1) = 0x{:X}\n"
                "_ram.read(    address) = 0x{:X}\n"
                "_ram.read(address - 1) = 0x{:X}\n"
                ).format(address,
                         ex_value,
                         value,
                         m._ram.read(address - 1) if address > 1 else 0,
                         value,
                         m._ram.read(address + 1) if address < 0xFFFF else 0)

    def test_get(self):
        m = mem.Memory()

        # Access RAM
        for i in range(0xFF0000, 0x1000000):
            value = m.read(i)
            assert value == 0, (
                "Value at address 0x{:X} was expected to be 0 "
                "but was {}".format(i, value))

    def test_set_0(self):
        # TODO expand with other memory-mapped devices
        m = mem.Memory()

        set_values = {
            # RAM
            0xFF0000: 0xABCD,
            0xFF0123: 0x5678,
            0xFFFFFF: 0x1234,
        }

        expect_values = {
            # RAM
            0xFF0000: 0xABCD,
            0xFF0001: 0xCD00,

            0xFF0122: 0x56,
            0xFF0123: 0x5678,
            0xFF0124: 0x7800,

            0xFFFFFE: 0x12,
            # Note that the lower byte has been ignored
            0xFFFFFF: 0x1200,
        }

        for address, value in set_values.items():
            m.write(address, value)

        # Test RAM
        for address in range(0xFF0000, 0x1000000):
            ex_value = expect_values.get(address, 0)
            value = m.read(address)
            assert value == ex_value, (
                "Expected RAM address 0x{:X} to return 0x{:X}, "
                "but got 0x{:X}.\n"
                "Memory:\n"
                "get(address - 1) = 0x{:X}\n"
                "get(    address) = 0x{:X}\n"
                "get(address - 1) = 0x{:X}\n"
                ).format(address,
                         ex_value,
                         value,
                         m.read(address - 1) if address > 0xFF0000 else 0,
                         value,
                         m.read(address + 1) if address < 0xFFFFFF else 0)

    def test_read_rom(self):
        m = mem.Memory()

        for address in range(0, 0x400000):
            value = m._rom.read(address)
            assert value == 0xFFFF, (
                "Expected ROM address 0x{:X} to contain the value 0xFFFF, but "
                "found value 0x{:X}.").format(address, value)

    def test_init_rom(self):
        m = mem.Memory("\x00\x00\x12\x34\xFF\xFF\xAB\xCD\x56")

        values = {
            0: 0,
            1: 0x12,
            2: 0x1234,
            3: 0x34FF,
            4: 0xFFFF,
            5: 0xFFAB,
            6: 0xABCD,
            7: 0xCD56,
            # Should be filled with 0xFF
            8: 0x56FF,
        }

        for address in range(0, 0x400000):
            ex_value = values.get(address, 0xFFFF)
            value = m._rom.read(address)
            assert value == ex_value, (
                "Expected ROM address 0x{:X} to contain the value 0x{:X}, but "
                "found value 0x{:X}.").format(address, ex_value, value)


if __name__ == "__main__":
    unittest.main()
