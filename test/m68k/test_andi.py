# -*- coding: utf-8 -*-
"""
Test the ANDI instruction of the 68k CPU.

Created on Fri Sep 22 14:05:26 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestAndi(unittest.TestCase):

    def test_andi_000(self):
        test_cpu.test_instruction(
            init_d=[0xEFFFFFFF, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0xE00FFF00, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.andi,
            program=test_cpu.int_list_to_str(
                [0b00000010, 0b10000000,
                 0xF0, 0x0F, 0xFF, 0]),  # ANDI.L #$F00FFF0, D0
            method_args=(
                2,  # op_size
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=14)

    def test_andi_001(self):
        test_cpu.test_instruction(
            init_d=[0x12345678, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x12345608, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.andi,
            program=test_cpu.int_list_to_str(
                [0b00000010, 0b00000000,
                 0xF0, 0x0F]),  # ANDI.B #$F, D0
            method_args=(
                0,  # op_size
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_andi_002(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, 0xFF5678, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF5678, 0xEFFF),
                (0xFF567A, 0xFFFF),
            ),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, 0xFF5678, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(
                (0xFF5676, 0),
                (0xFF5678, 0xE00F),
                (0xFF567A, 0xFF00),
                (0xFF567C, 0),
            ),
            cpu_method=ins.andi,
            program=test_cpu.int_list_to_str(
                [0b00000010, 0b10010110,
                 0xF0, 0x0F, 0xFF, 0]),  # ANDI.L #$F00FFF0, (A6)
            method_args=(
                2,  # op_size
                2,  # ea_mode
                6,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=28)


if __name__ == "__main__":
    unittest.main()
