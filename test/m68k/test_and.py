# -*- coding: utf-8 -*-
"""
Test the AND instruction of the 68k CPU.

Created on Wed Sep 20 15:15:31 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestAnd(unittest.TestCase):

    def test_and_000(self):
        test_cpu.test_instruction(
            init_d=None,
            init_a=None,
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0]*8,
            a=None,
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            memory_values=(),
            cpu_method=ins.and_,
            program=test_cpu.int_list_to_str(
                [0b11000000, 0b01000001]),  # AND D0, D1
            method_args=(
                0,  # register_index
                0,  # op_type
                1,  # op_size
                0,  # ea_mode
                1),  # ea_register
            method_kwargs={},
            cycle=4)

    def test_and_001(self):
        test_cpu.test_instruction(
            init_d=[0b1001011011110001, 0b1010010101101111, None, None,
                    None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0b1000010001100001, 0b1010010101101111, None, None,
               None, None, None, None],
            a=None,
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.and_,
            program=test_cpu.int_list_to_str(
                [0b11000000, 0b01000001]),  # AND D0, D1
            method_args=(
                0,  # register_index
                0,  # op_type
                1,  # op_size
                0,  # ea_mode
                1),  # ea_register
            method_kwargs={},
            cycle=4)

    def test_and_002(self):
        test_cpu.test_instruction(
            init_d=[0b1001011011110001, None, None, None,
                    None, None, None, None],
            init_a=[0, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFFFFFE, 0xFF),
            ),
            d=[0b1001011011110001, None, None, None,
               None, None, None, None],
            a=[0xFFFFFFFE, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(
                (0xFFFFFE, 0b11110001),
            ),
            cpu_method=ins.and_,
            program=test_cpu.int_list_to_str(
                [0b11000001, 0b01100000]),  # AND D0, -(A0)
            method_args=(
                0,  # register_index
                1,  # op_type
                1,  # op_size
                4,  # ea_mode
                0),  # ea_register
            method_kwargs={},
            cycle=14)


if __name__ == "__main__":
    unittest.main()
