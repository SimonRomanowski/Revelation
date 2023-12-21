# -*- coding: utf-8 -*-
"""
Tests the 'cpu_utils.register' module.

Created on Fri Sep 15 20:01:49 2023

@author: Simon Romanowski
"""

import unittest

import cpu_utils.register as reg


class TestRegister8(unittest.TestCase):

    def test_init(self):
        r0 = reg.Register8()
        r1 = reg.Register8(1)
        r2 = reg.Register8(value=0x1C)
        r3 = reg.Register8(value=0x1234)

        assert r0.get() == 0
        assert r1.get() == 1
        assert r2.get() == 0x1C
        # Only lower byte is kept
        assert r3.get() == 0x34

    def test_get_bit(self):
        r0 = reg.Register8()
        r1 = reg.Register8(0xFF)
        r2 = reg.Register8(0b11001010)

        # List of (register, list_of_expected_bits) values
        values = [
            [r0, [0] * 8],
            [r1, [1] * 8],
            [r2, [0, 1, 0, 1, 0, 0, 1, 1]]
        ]

        for reg_index, pair in enumerate(values):
            r, bits = pair
            full_value = r.get()
            assert len(bits) == 8
            for index, ex_bit in enumerate(bits):
                bit = r.get_bit(index)
                assert bit == ex_bit, (
                    "Expected register {} to contain a {} bit at index {}, "
                    "but got a {} bit. Full value: 0x{:X}").format(
                        reg_index,
                        ex_bit,
                        index,
                        bit,
                        full_value)

    def test_set(self):
        r0 = reg.Register8(123)

        r0.set(42)
        assert r0.get() == 42

        r0.set(0xABCD)
        # Only lower byte is kept
        assert r0.get() == 0xCD

    def test_set_bits(self):
        # tuples of (mask, v_old, v_new, ex_res)
        values = [
            (0b11110000,
             0b11001100,
             0b10100101,
             0b10101100),
            (0b00110011,
             0b01000011,
             0b11010110,
             0b01010010),
            (0b10101010,
             0b10111001,
             0b10001111,
             0b10011011),
            # Only lower byte is kept
            (0b1111111100001111,
             0b0000000000110110,
             0b1101010111010010,
             0b0000000000110010)
        ]

        for i, vs in enumerate(values):
            mask, v_old, v_new, ex_res = vs
            r = reg.Register8(v_old)
            r.set_bits(mask, v_new)
            value = r.get()
            assert value == ex_res, (
                "{}:\n"
                "expected\n"
                "reg.Register8(0x{:X}).set_bits(0x{:X}, 0x{:X}).get()\n"
                "to be equal to 0x{:X}\n"
                "but was 0x{:X}").format(i, v_old, mask, v_new, ex_res, value)


class TestRegister16(unittest.TestCase):

    def test_init(self):
        r0 = reg.Register16()
        r1 = reg.Register16(12345)
        r2 = reg.Register16(value=9999)
        r3 = reg.Register16(0xE1ABCD)

        assert r0.get() == 0
        assert r1.get() == 12345
        assert r2.get() == 9999
        # Only lower word is kept
        assert r3.get() == 0xABCD

    def test_get_bit(self):
        r0 = reg.Register16()
        r1 = reg.Register16(0xFFFF)
        r2 = reg.Register16(0b0100101111001010)

        # List of (register, list_of_expected_bits) values
        values = [
            [r0, [0] * 16],
            [r1, [1] * 16],
            [r2, list(reversed(
                [0, 1, 0, 0, 1, 0, 1, 1,
                 1, 1, 0, 0, 1, 0, 1, 0]))]
        ]

        for reg_index, pair in enumerate(values):
            r, bits = pair
            full_value = r.get()
            assert len(bits) == 16
            for index, ex_bit in enumerate(bits):
                bit = r.get_bit(index)
                assert bit == ex_bit, (
                    "Expected register {} to contain a {} bit at index {}, "
                    "but got a {} bit. Full value: 0x{:X}").format(
                        reg_index,
                        ex_bit,
                        index,
                        bit,
                        full_value)

    def test_set(self):
        r0 = reg.Register16(1337)

        r0.set(12345)
        assert r0.get() == 12345

        r0.set(0xFFFF)
        assert r0.get() == 0xFFFF

        r0.set(0x123456)
        # Only lower word is kept
        assert r0.get() == 0x3456

    def test_set_bits(self):
        # tuples of (mask, v_old, v_new, ex_res)
        values = [
            (0xFF00,
             0xABCD,
             0x5910,
             0x59CD),
            (0x0F0F,
             0xF4B7,
             0xA01C,
             0xF0BC),
            (0xF0F0,
             0x9876,
             0x54AE,
             0x58A6),
            # Only lower word is kept
            (0xFFFF00FF,
             0x0000FEAC,
             0x79AB0615,
             0x0000FE15)
        ]

        for i, vs in enumerate(values):
            mask, v_old, v_new, ex_res = vs
            r = reg.Register16(v_old)
            r.set_bits(mask, v_new)
            value = r.get()
            assert value == ex_res, (
                "{}:\n"
                "expected\n"
                "reg.Register16(0x{:X}).set_bits(0x{:X}, 0x{:X}).get()\n"
                "to be equal to 0x{:X}\n"
                "but was 0x{:X}").format(i, v_old, mask, v_new, ex_res, value)

    def test_get_byte(self):
        r0 = reg.Register16(0xABCD)
        r1 = reg.Register16(0x1234)
        r2 = reg.Register16(0)
        r3 = reg.Register16(0x9172)

        r3.set(0x59C4)

        assert r0.get_byte() == 0xCD
        assert r1.get_byte() == 0x34
        assert r2.get_byte() == 0
        assert r3.get_byte() == 0xC4

    def test_set_byte(self):
        r0 = reg.Register16(0xABCD)
        r1 = reg.Register16(0x1234)
        r2 = reg.Register16(0)
        r3 = reg.Register16(0x9172)

        r0.set_byte(0x9E)
        r1.set_byte(0x56)
        r2.set_byte(0xFF)
        # Only lower byte is kept
        r3.set_byte(0xB609)

        assert r0.get() == 0xAB9E
        assert r1.get() == 0x1256
        assert r2.get() == 0xFF
        assert r3.get() == 0x9109


class TestRegister32(unittest.TestCase):

    def test_init(self):
        r0 = reg.Register32()
        r1 = reg.Register32(87132)
        r2 = reg.Register32(value=714535)
        r3 = reg.Register32(0xABCD12345678)

        assert r0.get() == 0
        assert r1.get() == 87132
        assert r2.get() == 714535
        # Only lower 32 bit are kept
        assert r3.get() == 0x12345678

    def test_get_bit(self):
        r0 = reg.Register32()
        r1 = reg.Register32(0xFFFFFFFF)
        r2 = reg.Register32(0b10100010011101010100101111001010)

        # List of (register, list_of_expected_bits) values
        values = [
            [r0, [0] * 32],
            [r1, [1] * 32],
            [r2, list(reversed(
                [1, 0, 1, 0, 0, 0, 1, 0,
                 0, 1, 1, 1, 0, 1, 0, 1,
                 0, 1, 0, 0, 1, 0, 1, 1,
                 1, 1, 0, 0, 1, 0, 1, 0]))]
        ]

        for reg_index, pair in enumerate(values):
            r, bits = pair
            full_value = r.get()
            assert len(bits) == 32
            for index, ex_bit in enumerate(bits):
                bit = r.get_bit(index)
                assert bit == ex_bit, (
                    "Expected register {} to contain a {} bit at index {}, "
                    "but got a {} bit. Full value: 0x{:X}").format(
                        reg_index,
                        ex_bit,
                        index,
                        bit,
                        full_value)

    def test_set(self):
        r0 = reg.Register32(1354762)

        r0.set(813971)
        assert r0.get() == 813971

        r0.set(0xAB12CD34)
        assert r0.get() == 0xAB12CD34

        r0.set(0x1234567890)
        # Only lower 32 bit are kept
        assert r0.get() == 0x34567890

    def test_set_bits(self):
        # tuples of (mask, v_old, v_new, ex_res)
        values = [
            (0xFFFF0000,
             0x98213740,
             0x645F38C8,
             0x645F3740),
            (0xF0F0F0F0,
             0x4387231E,
             0xA604F153,
             0xA307F35E),
            (0x00FF00FF,
             0xC8723F15,
             0x0738B048,
             0xC8383F48),
            # Only lower 32 bit are kept
            (0xFFFF0000FFFF,
             0x0000A834C270,
             0x387434287986,
             0x0000A8347986),
        ]

        for i, vs in enumerate(values):
            mask, v_old, v_new, ex_res = vs
            r = reg.Register32(v_old)
            r.set_bits(mask, v_new)
            value = r.get()
            assert value == ex_res, (
                "{}:\n"
                "expected\n"
                "reg.Register32(0x{:X}).set_bits(0x{:X}, 0x{:X}).get()\n"
                "to be equal to 0x{:X}\n"
                "but was 0x{:X}").format(i, v_old, mask, v_new, ex_res, value)

    def test_get_byte(self):
        r0 = reg.Register32(0xABCDEF01)
        r1 = reg.Register32(0x12345678)
        r2 = reg.Register32(0)
        r3 = reg.Register32(0x74278438)

        r3.set(0xF098BE57)

        assert r0.get_byte() == 1
        assert r1.get_byte() == 0x78
        assert r2.get_byte() == 0
        assert r3.get_byte() == 0x57

    def test_set_byte(self):
        r0 = reg.Register32(0x87654321)
        r1 = reg.Register32(0x358FA038)
        r2 = reg.Register32(0)
        r3 = reg.Register32(0xF987AE60)

        r0.set_byte(0x12)
        r1.set_byte(0x46)
        r2.set_byte(0xFF)
        # Only lower byte is kept
        r3.set_byte(0x8793)

        assert r0.get() == 0x87654312
        assert r1.get() == 0x358FA046
        assert r2.get() == 0xFF
        assert r3.get() == 0xF987AE93

    def test_get_word(self):
        r0 = reg.Register32(0xABCDEF01)
        r1 = reg.Register32(0x12340678)
        r2 = reg.Register32(0)
        r3 = reg.Register32(0x74278438)

        r3.set(0xF098BE57)

        assert r0.get_word() == 0xEF01
        assert r1.get_word() == 0x678
        assert r2.get_word() == 0
        assert r3.get_word() == 0xBE57

    def test_set_word(self):
        r0 = reg.Register32(0x87654321)
        r1 = reg.Register32(0x358FA038)
        r2 = reg.Register32(0)
        r3 = reg.Register32(0xF987AE60)

        r0.set_word(0x1234)
        r1.set_word(0x387E)
        r2.set_word(0xFFFF)
        # Only lower word is kept
        r3.set_word(0xFFFF7532)

        assert r0.get() == 0x87651234
        assert r1.get() == 0x358F387E
        assert r2.get() == 0xFFFF
        assert r3.get() == 0xF9877532


if __name__ == "__main__":
    unittest.main()
