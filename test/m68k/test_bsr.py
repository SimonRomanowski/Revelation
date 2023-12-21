# -*- coding: utf-8 -*-
"""
Test the BSR instruction of the 68k CPU.

Created on Sat Sep 23 21:03:19 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestBsr(unittest.TestCase):

    def test_bsr_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFFFF68],
            init_pc=0x100,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(
                (0xFFFF64, 0),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFFFF64],
            pc=0x11A,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(
                (0xFFFF62, 0),
                (0xFFFF64, 0),
                (0xFFFF66, 0x102),
                (0xFFFF68, 0),
            ),

            # Instruction
            cpu_method=ins.bsr,
            program=test_cpu.int_list_to_str(
                [0xFF]*0x100 + [0b01100001, 0x18]),  # BSR <+$18>
            method_args=(
                0x18,  # offset
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=18)

    def test_bsr_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFFFF68],
            init_pc=0x1000,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(
                (0xFFFF64, 0),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFFFF64],
            pc=0x1146,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(
                (0xFFFF62, 0),
                (0xFFFF64, 0),
                (0xFFFF66, 0x1004),
                (0xFFFF68, 0),
            ),

            # Instruction
            cpu_method=ins.bsr,
            program=test_cpu.int_list_to_str(
                [0xFF]*0x1000 + [0b01100001, 0, 0x01, 0x44]),  # BSR <+$144>
            method_args=(
                0,  # offset
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=18)


if __name__ == "__main__":
    unittest.main()
