# -*- coding: utf-8 -*-
"""
Test the SWAP instruction of the 68k CPU.

Created on Wed Sep 27 23:40:21 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestSwap(unittest.TestCase):

    def test_swap_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x12345678, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=0, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 0x56781234, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.swap,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b01000010]),  # SWAP D2
            method_args=(
                2,  # register_index
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_swap_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0xFFFF, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=0, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 0xFFFF0000, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.swap,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b01000010]),  # SWAP D2
            method_args=(
                2,  # register_index
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_swap_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=0, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 0, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.swap,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b01000010]),  # SWAP D2
            method_args=(
                2,  # register_index
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)


if __name__ == "__main__":
    unittest.main()
