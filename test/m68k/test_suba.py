# -*- coding: utf-8 -*-
"""
Test the SUBA instruction of the 68k CPU.

Created on Wed Sep 27 19:25:03 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestSuba(unittest.TestCase):

    def test_suba_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 2, None,
                    None, None, None, None],
            init_a=[None, 0xFF1234, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 2, None,
               None, None, None, None],
            a=[None, 0xFF1232, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.suba,
            program=test_cpu.int_list_to_str(
                [0b10010010, 0b11000010]),  # SUB.W D2, A1
            method_args=(
                1,  # register_index
                0,  # op_size
                0,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_suba_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x8000, None,
                    None, None, None, None],
            init_a=[None, 0xFFFF8234, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 0x8000, None,
               None, None, None, None],
            a=[None, 0x234, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.suba,
            program=test_cpu.int_list_to_str(
                [0b10010010, 0b11000010]),  # SUB.W D2, A1
            method_args=(
                1,  # register_index
                0,  # op_size
                0,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_suba_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0xF000, None,
                    None, None, None, None],
            init_a=[None, 0xFFF568, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 0xF000, None,
               None, None, None, None],
            a=[None, 0xFF0568, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.suba,
            program=test_cpu.int_list_to_str(
                [0b10010011, 0b11000010]),  # SUB.L D2, A1
            method_args=(
                1,  # register_index
                1,  # op_size
                0,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_suba_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFFF568, 0xFF09C2, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF09C2, 0xF),
                (0xFF09C4, 8),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0xF0F560, 0xFF09C2, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF09C2, 0xF),
                (0xFF09C4, 8),
            ),

            # Instruction
            cpu_method=ins.suba,
            program=test_cpu.int_list_to_str(
                [0b10010011, 0b11010010]),  # SUB.L (A2), A1
            method_args=(
                1,  # register_index
                1,  # op_size
                2,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=14)


if __name__ == "__main__":
    unittest.main()
