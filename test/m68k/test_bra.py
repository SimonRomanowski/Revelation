# -*- coding: utf-8 -*-
"""
Test the BRA instruction of the 68k CPU.

Created on Sat Sep 23 20:09:41 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestBra(unittest.TestCase):

    def test_bra_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=22,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bra,
            program=test_cpu.int_list_to_str(
                [0b01100000, 20]),  # BRA <+20>
            method_args=(
                20,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bra_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=2,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=0,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bra,
            program=test_cpu.int_list_to_str(
                [0xFF, 0xFF,
                 0b01100000, 0xFC]),  # BRA <-4>
            method_args=(
                0xFC,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)


if __name__ == "__main__":
    unittest.main()
