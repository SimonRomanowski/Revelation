# -*- coding: utf-8 -*-
"""
Test the Scc instruction of the 68k CPU.

Created on Wed Sep 27 17:51:08 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestScc(unittest.TestCase):

    def test_scc_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, 0x1234, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, 0x12FF, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.scc,
            program=test_cpu.int_list_to_str(
                [0b01010101, 0b11000101]),  # SCS D5
            method_args=(
                5,  # condition
                0,  # ea_mode
                5,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_scc_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, 0x1234, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, 0x1200, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.scc,
            program=test_cpu.int_list_to_str(
                [0b01010100, 0b11000101]),  # SCC D5
            method_args=(
                4,  # condition
                0,  # ea_mode
                5,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_scc_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, 0xFF4568, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=1, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF4568, 0x1234),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, 0xFF4569, None, None],
            pc=None,
            x=None, n=None, z=1, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF4568, 0xFF34),
            ),

            # Instruction
            cpu_method=ins.scc,
            program=test_cpu.int_list_to_str(
                [0b01010111, 0b11011101]),  # SCC (A5)+
            method_args=(
                7,  # condition
                3,  # ea_mode
                5,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)


if __name__ == "__main__":
    unittest.main()
