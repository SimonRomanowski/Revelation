# -*- coding: utf-8 -*-
"""
Test the megadrive.memory module.

Created on Sat Nov  4 15:59:41 2023

@author: Simon Romanowski
"""

import unittest

from megadrive.devices import ram


class TestRam(unittest.TestCase):

    def test_init_00(self):
        m = ram.Ram(1024)

        for address in range(0, 1024, 2):
            assert m.read(address) == 0

    def test_fill_bytes_00(self):
        m = ram.Ram(1024)

        for address in range(0, 1024, 2):
            m.write(address, 0x75B1)

        m.fill_bytes(0, 1024, 0xAB)

        for address in range(0, 1024, 2):
            value = m.read(address)
            expected_value = 0xABAB
            assert value == expected_value, (
                "Expected value 0x{:04X} at 0x{:04X}, but got 0x{:04X}."
            ).format(
                expected_value,
                address,
                value)

    def test_fill_bytes_01(self):
        m = ram.Ram(1024)

        for address in range(0, 1024, 2):
            m.write(address, 0x75B1)

        m.fill_bytes(0, 8, 0xEC)

        for address in range(0, 8, 2):
            value = m.read(address)
            expected_value = 0xECEC
            assert value == expected_value, (
                "Expected value 0x{:04X} at 0x{:04X}, but got 0x{:04X}."
            ).format(
                expected_value,
                address,
                value)

        for address in range(8, 1024, 2):
            value = m.read(address)
            expected_value = 0x75B1
            assert value == expected_value, (
                "Expected value 0x{:04X} at 0x{:04X}, but got 0x{:04X}."
            ).format(
                expected_value,
                address,
                value)

    def test_fill_bytes_02(self):
        m = ram.Ram(1024)

        for address in range(0, 1024, 2):
            m.write(address, 0x75B1)

        m.fill_bytes(1, 7, 0xEC)

        for address in range(0, 8, 2):
            value = m.read(address)
            expected_value = 0x75EC if address == 0 else 0xECEC
            assert value == expected_value, (
                "Expected value 0x{:04X} at 0x{:04X}, but got 0x{:04X}."
            ).format(
                expected_value,
                address,
                value)

        for address in range(8, 1024, 2):
            value = m.read(address)
            expected_value = 0x75B1
            assert value == expected_value, (
                "Expected value 0x{:04X} at 0x{:04X}, but got 0x{:04X}."
            ).format(
                expected_value,
                address,
                value)

    def test_fill_bytes_03(self):
        m = ram.Ram(1024)

        for address in range(0, 1024, 2):
            m.write(address, 0x75B1)

        m.fill_bytes(1, 8, 0xEC)

        for address in range(0, 10, 2):
            value = m.read(address)
            if address == 0:
                expected_value = 0x75EC
            elif address == 8:
                expected_value = 0xECB1
            else:
                expected_value = 0xECEC
            assert value == expected_value, (
                "Expected value 0x{:04X} at 0x{:04X}, but got 0x{:04X}."
            ).format(
                expected_value,
                address,
                value)

        for address in range(10, 1024, 2):
            value = m.read(address)
            expected_value = 0x75B1
            assert value == expected_value, (
                "Expected value 0x{:04X} at 0x{:04X}, but got 0x{:04X}."
            ).format(
                expected_value,
                address,
                value)

    def test_fill_bytes_04(self):
        m = ram.Ram(0x4000)

        for address in range(0, 0x4000, 2):
            m.write(address, 0x75B1)

        m.fill_bytes(0x2002, 4, 0x40)

        for address in range(0, 0x4000, 2):
            value = m.read(address)
            if address < 0x2002:
                expected_value = 0x75B1
            elif address < 0x2006:
                expected_value = 0x4040
            else:
                expected_value = 0x75B1
            assert value == expected_value, (
                "Expected value 0x{:04X} at 0x{:04X}, but got 0x{:04X}."
            ).format(
                expected_value,
                address,
                value)


if __name__ == "__main__":
    unittest.main()
