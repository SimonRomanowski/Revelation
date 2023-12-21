# -*- coding: utf-8 -*-
"""
Test the ADDX instruction of the 68k CPU.

Created on Fri Sep 22 10:13:40 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestAddx(unittest.TestCase):

    def test_addx_000(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    0x10203040, 0x0A0B0C0D, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[None, None, None, None,
               0x10203040, 0x1A2B3C4E, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.addx,
            program=test_cpu.int_list_to_str(
                [0b11011011, 0b10000100]),  # ADDX D4, D5
            method_args=(
                4,  # register_src
                5,  # register_dst
                0,  # op_type
                2,  # op_size
            ),
            method_kwargs={},
            cycle=8)

    def test_addx_001(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFF3006, None, None,
                    None, None, None, 0xFF4006],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF3004, 0xFFFF),
                (0xFF4004, 2),
            ),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0xFF3004, None, None,
               None, None, None, 0xFF4004],
            pc=None,
            x=1, n=0, z=0, v=0, c=1,
            memory_values=(
                (0xFF3002, 0),
                (0xFF3004, 2),
                (0xFF3006, 0),
                (0xFF4002, 0),
                (0xFF4004, 2),
                (0xFF4006, 0),
            ),
            cpu_method=ins.addx,
            program=test_cpu.int_list_to_str(
                [0b11010011, 0b01001111]),  # ADDX -(A7), -(A1)
            method_args=(
                7,  # register_src
                1,  # register_dst
                1,  # op_type
                1,  # op_size
            ),
            method_kwargs={},
            cycle=18)


if __name__ == "__main__":
    unittest.main()
