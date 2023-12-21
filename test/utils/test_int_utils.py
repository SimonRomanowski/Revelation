# -*- coding: utf-8 -*-
"""
Test the utils.int_utils module.

Created on Sun Sep 17 16:40:30 2023

@author: Simon Romanowski
"""

import unittest

from utils import int_utils

class TestTo32XString(unittest.TestCase):

    def _test_result(self, value):
        result = int_utils.to_32x_string(value)
        expected = "{:08X}".format(value)
        assert result == expected, ("Expected {} but got {}").format(
            expected, result)

    def test_00(self):
        self._test_result(0)

    def test_01(self):
        self._test_result(1)

    def test_02(self):
        self._test_result(0xFFFFFFFF)

    def test_03(self):
        self._test_result(0x1234)

    def test_04(self):
        self._test_result(0x12345678)

class TestTo16BString(unittest.TestCase):

    def _test_result(self, value):
        result = int_utils.to_16b_string(value)
        expected = "{:016b}".format(value)
        assert result == expected, ("Expected {} but got {}").format(
            expected, result)

    def test_00(self):
        self._test_result(0)

    def test_01(self):
        self._test_result(1)

    def test_02(self):
        self._test_result(0xFFFF)

    def test_03(self):
        self._test_result(0x1234)


class TestSignExtend8to16(unittest.TestCase):

    def _test(self, value, expected):
        result = int_utils.sign_extend_8_to_16(value)
        assert result == expected, (
            "16 bit sign-extended value of 8 bit value 0x{:X} was expected to "
            "be 0x{:X}, but was 0x{:X}.").format(value, expected, result)

    def test_00(self):
        self._test(0, 0)

    def test_01(self):
        self._test(0x7F, 0x7F)

    def test_02(self):
        self._test(0xFF, 0xFFFF)

    def test_03(self):
        self._test(0x80, 0xFF80)


class TestSignExtend8to32(unittest.TestCase):

    def _test(self, value, expected):
        result = int_utils.sign_extend_8_to_32(value)
        assert result == expected, (
            "32 bit sign-extended value of 8 bit value 0x{:X} was expected to "
            "be 0x{:X}, but was 0x{:X}.").format(value, expected, result)

    def test_00(self):
        self._test(0, 0)

    def test_01(self):
        self._test(0x7F, 0x7F)

    def test_02(self):
        self._test(0xFF, 0xFFFFFFFF)

    def test_03(self):
        self._test(0x80, 0xFFFFFF80)


class TestSignExtend16to32(unittest.TestCase):

    def _test(self, value, expected):
        result = int_utils.sign_extend_16_to_32(value)
        assert result == expected, (
            "32 bit sign-extended value of 16 bit value 0x{:X} was expected "
            "to be 0x{:X}, but was 0x{:X}.").format(value, expected, result)

    def test_00(self):
        self._test(0, 0)

    def test_01(self):
        self._test(0x7FFF, 0x7FFF)

    def test_02(self):
        self._test(0xFFFF, 0xFFFFFFFF)

    def test_03(self):
        self._test(0x8000, 0xFFFF8000)

    def test_04(self):
        self._test(0x80, 0x80)


class TestSelectBits(unittest.TestCase):

    def _test(self, value, from_, to, expected):
        result = int_utils.select_bits(value, from_, to)
        assert result == expected, (
            "Selecting bits ({} - {}) from {} was expected to give 0b{:b} "
            "but got 0b{:b}.").format(from_, to, value, expected, result)

    def test_00(self):
        self._test(
            value=0,
            from_=0,
            to=63,
            expected=0
        )

    def test_01(self):
        self._test(
            value=0b10110110101100,
            from_=2,
            to=5,
            expected=0b1011
        )
        self._test(
            value=0b10110110101100,
            from_=5,
            to=2,
            expected=0b1011
        )

    def test_02(self):
        self._test(
            value=0b11100,
            from_=2,
            to=-1,
            expected=0b1
        )
        self._test(
            value=0b11100,
            from_=2,
            to=2,
            expected=0b1
        )

    def test_03(self):
        self._test(
            value=0b11100,
            from_=0,
            to=2,
            expected=0b100
        )


if __name__ == "__main__":
    unittest.main()
