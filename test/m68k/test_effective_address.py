# -*- coding: utf-8 -*-
"""
Test the effective address calculation.

Created on Wed Sep 20 14:29:32 2023

@author: Simon Romanowski
"""

import unittest

import m68k.effective_address as ea


class TestSplit(unittest.TestCase):

    def _test(self, value, expected):
        result = ea.split(value)
        assert result == expected, (
            "Expected effective address split of 0b{:06b} to be (0b{:03b}, "
            "0b{:03b}), but was (0b{:03b}, 0b{:03b}).").format(
                value, expected[0], expected[1], result[0], result[1])

    def test_00(self):
        self._test(0b110101, (0b110, 0b101))

    def test_01(self):
        self._test(0b001010, (0b001, 0b010))


class TestCategories(unittest.TestCase):

    def test_is_valid(self):
        for ea_mode in range(7):
            for ea_register in range(8):
                assert ea.is_valid(ea_mode, ea_register), (
                    "Expected (0b{:03b}, 0b{:03b}) to be valid").format(
                        ea_mode, ea_register)
                assert ea.is_valid((ea_mode << 3) | ea_register), (
                    "Got different result for (0b{:03b}, 0b{:03b})").format(
                        ea_mode, ea_register)
        ea_mode = 7
        for ea_register in range(5):
            assert ea.is_valid(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to be valid").format(
                    ea_mode, ea_register)
            assert ea.is_valid((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)

        for ea_register in range(5, 8):
            assert not ea.is_valid(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to be INVALID").format(
                    ea_mode, ea_register)
            assert not ea.is_valid((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)

    def test_is_data(self):
        ea_mode = 0
        for ea_register in range(8):
            assert ea.is_data(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to be data").format(
                    ea_mode, ea_register)
            assert ea.is_data((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)
        for ea_mode in range(2, 7):
            for ea_register in range(8):
                assert ea.is_data(ea_mode, ea_register), (
                    "Expected (0b{:03b}, 0b{:03b}) to be data").format(
                        ea_mode, ea_register)
                assert ea.is_data((ea_mode << 3) | ea_register), (
                    "Got different result for (0b{:03b}, 0b{:03b})").format(
                        ea_mode, ea_register)
        ea_mode = 7
        for ea_register in range(5):
            assert ea.is_data(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to be data").format(
                    ea_mode, ea_register)
            assert ea.is_data((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)

        ea_mode = 1
        for ea_register in range(8):
            assert not ea.is_data(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to NOT be data").format(
                    ea_mode, ea_register)
            assert not ea.is_data((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)
        ea_mode = 7
        for ea_register in range(5, 8):
            assert not ea.is_data(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to NOT be data").format(
                    ea_mode, ea_register)
            assert not ea.is_data((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)

    def test_is_memory(self):
        for ea_mode in range(2, 7):
            for ea_register in range(8):
                assert ea.is_memory(ea_mode, ea_register), (
                    "Expected (0b{:03b}, 0b{:03b}) to be memory").format(
                        ea_mode, ea_register)
                assert ea.is_memory((ea_mode << 3) | ea_register), (
                    "Got different result for (0b{:03b}, 0b{:03b})").format(
                        ea_mode, ea_register)
        ea_mode = 7
        for ea_register in range(5):
            assert ea.is_memory(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to be memory").format(
                    ea_mode, ea_register)
            assert ea.is_memory((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)

        for ea_mode in range(2):
            for ea_register in range(8):
                assert not ea.is_memory(ea_mode, ea_register), (
                    "Expected (0b{:03b}, 0b{:03b}) to NOT be memory").format(
                        ea_mode, ea_register)
                assert not ea.is_memory((ea_mode << 3) | ea_register), (
                    "Got different result for (0b{:03b}, 0b{:03b})").format(
                        ea_mode, ea_register)
        ea_mode = 7
        for ea_register in range(5, 8):
            assert not ea.is_memory(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to NOT be memory").format(
                    ea_mode, ea_register)
            assert not ea.is_memory((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)

    def test_is_control(self):
        ea_mode = 2
        for ea_register in range(8):
            assert ea.is_control(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to be control").format(
                    ea_mode, ea_register)
            assert ea.is_control((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)
        for ea_mode in range(5, 7):
            for ea_register in range(8):
                assert ea.is_control(ea_mode, ea_register), (
                    "Expected (0b{:03b}, 0b{:03b}) to be control").format(
                        ea_mode, ea_register)
                assert ea.is_control((ea_mode << 3) | ea_register), (
                    "Got different result for (0b{:03b}, 0b{:03b})").format(
                        ea_mode, ea_register)
        ea_mode = 7
        for ea_register in range(4):
            assert ea.is_control(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to be control").format(
                    ea_mode, ea_register)
            assert ea.is_control((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)

        for ea_mode in range(2):
            for ea_register in range(8):
                assert not ea.is_control(ea_mode, ea_register), (
                    "Expected (0b{:03b}, 0b{:03b}) to NOT be control").format(
                        ea_mode, ea_register)
                assert not ea.is_control((ea_mode << 3) | ea_register), (
                    "Got different result for (0b{:03b}, 0b{:03b})").format(
                        ea_mode, ea_register)
        for ea_mode in range(3, 5):
            for ea_register in range(8):
                assert not ea.is_control(ea_mode, ea_register), (
                    "Expected (0b{:03b}, 0b{:03b}) to NOT be control").format(
                        ea_mode, ea_register)
                assert not ea.is_control((ea_mode << 3) | ea_register), (
                    "Got different result for (0b{:03b}, 0b{:03b})").format(
                        ea_mode, ea_register)
        ea_mode = 7
        for ea_register in range(4, 8):
            assert not ea.is_control(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to NOT be control").format(
                    ea_mode, ea_register)
            assert not ea.is_control((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)

    def test_is_alterable(self):
        for ea_mode in range(7):
            for ea_register in range(8):
                assert ea.is_alterable(ea_mode, ea_register), (
                    "Expected (0b{:03b}, 0b{:03b}) to be alterable").format(
                        ea_mode, ea_register)
                assert ea.is_alterable((ea_mode << 3) | ea_register), (
                    "Got different result for (0b{:03b}, 0b{:03b})").format(
                        ea_mode, ea_register)
        ea_mode = 7
        for ea_register in range(8):
            assert not ea.is_alterable(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to NOT be alterable").format(
                    ea_mode, ea_register)
            assert not ea.is_alterable((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)

    def test_is_data_alterable(self):
        ea_mode = 0
        for ea_register in range(8):
            assert ea.is_data_alterable(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to be data alterable").format(
                    ea_mode, ea_register)
            assert ea.is_data_alterable((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)
        for ea_mode in range(2, 7):
            for ea_register in range(8):
                assert ea.is_data_alterable(ea_mode, ea_register), (
                    "Expected (0b{:03b}, 0b{:03b}) to be data "
                    "alterable").format(
                        ea_mode, ea_register)
                assert ea.is_data_alterable((ea_mode << 3) | ea_register), (
                    "Got different result for (0b{:03b}, 0b{:03b})").format(
                        ea_mode, ea_register)
        ea_mode = 7
        for ea_register in range(2):
            assert ea.is_data_alterable(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to be data alterable").format(
                    ea_mode, ea_register)
            assert ea.is_data_alterable((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)

        ea_mode = 1
        for ea_register in range(8):
            assert not ea.is_data_alterable(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to NOT be data "
                "alterable").format(
                    ea_mode, ea_register)
            assert not ea.is_data_alterable((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)
        ea_mode = 7
        for ea_register in range(2, 8):
            assert not ea.is_data_alterable(ea_mode, ea_register), (
                "Expected (0b{:03b}, 0b{:03b}) to NOT be data "
                "alterable").format(
                    ea_mode, ea_register)
            assert not ea.is_data_alterable((ea_mode << 3) | ea_register), (
                "Got different result for (0b{:03b}, 0b{:03b})").format(
                    ea_mode, ea_register)


if __name__ == "__main__":
    unittest.main()
