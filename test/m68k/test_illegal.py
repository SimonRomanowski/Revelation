# -*- coding: utf-8 -*-
"""
Test the ILLEGAL instruction of the 68k CPU.

Created on Mon Sep 25 09:32:26 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestIllegal(unittest.TestCase):

    def test_illegal_000(self):
        program = [0] * 16 \
            + [0, 1, 0x56, 0x78]  # Illegal instruction vector
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFFF488],
            init_pc=20,
            init_x=1, init_n=1, init_z=0, init_v=1, init_c=1,
            init_t1=1, init_s=0, init_i=7,
            init_usp=0xFFF488,
            init_ssp=0xFF100A,
            init_mem=(
                (0xFF100A, 0xABCD),
                (0xFFF488, 0x1234),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFF1004],
            pc=0x15678,
            x=1, n=1, z=0, v=1, c=1,
            t1=0, s=1, i=7,
            usp=0xFFF488,
            ssp=0xFF1004,
            memory_values=(
                (0xFF1002, 0),
                (0xFF1004, 0x871B),
                (0xFF1006, 0),
                (0xFF1008, 22),
                (0xFF100A, 0xABCD),
                (0xFF100C, 0),
                (0xFFF488, 0x1234),
            ),

            # Instruction
            cpu_method=ins.illegal,
            program=test_cpu.int_list_to_str(
                program + [0b01001010, 0b11111100]),  # ILLEGAL
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=34)


if __name__ == "__main__":
    unittest.main()
