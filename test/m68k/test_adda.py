# -*- coding: utf-8 -*-
"""
Test the ADDA instruction of the 68k CPU.

Created on Thu Sep 21 12:56:28 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestAdda(unittest.TestCase):

    def test_adda_000(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    0x44332211, None, None, None],
            init_a=[None, None, None, 0x11223344,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[None, None, None, None,
               0x44332211, None, None, None],
            a=[None, None, None, 0x55555555,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.adda,
            program=test_cpu.int_list_to_str(
                [0b11010111, 0b11000100]),  # ADDA D4, A3
            method_args=(
                3, # register_index
                1, # op_size
                0, # ea_mode
                4, # ea_register
            ),
            method_kwargs={},
            cycle=8)

    def test_adda_001(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    0x8000, None, None, None],
            init_a=[None, None, None, 0x123,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[None, None, None, None,
               0x8000, None, None, None],
            a=[None, None, None, 0xFFFF8123,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.adda,
            program=test_cpu.int_list_to_str(
                [0b11010110, 0b11000100]),  # ADDA D4, A3
            method_args=(
                3, # register_index
                0, # op_size
                0, # ea_mode
                4, # ea_register
            ),
            method_kwargs={},
            cycle=8)

    def test_adda_002(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    1, None, None, None],
            init_a=[None, None, None, 0xFFFFFFFF,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[None, None, None, None,
               1, None, None, None],
            a=[None, None, None, 0,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.adda,
            program=test_cpu.int_list_to_str(
                [0b11010110, 0b11000100]),  # ADDA D4, A3
            method_args=(
                3, # register_index
                1, # op_size
                0, # ea_mode
                4, # ea_register
            ),
            method_kwargs={},
            cycle=8)


if __name__ == "__main__":
    unittest.main()
