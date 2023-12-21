# -*- coding: utf-8 -*-
"""
Test the LEA instruction of the 68k CPU.

Created on Mon Sep 25 12:44:26 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestLea(unittest.TestCase):

    def test_lea_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, 0x12345678, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, 0x12345678, 0x12345678,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.lea,
            program=test_cpu.int_list_to_str(
                [0b01000111, 0b11010010]),  # LEA (A2), A3
            method_args=(
                3,  # register_index
                2,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_lea_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, 0xFF1234,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.lea,
            program=test_cpu.int_list_to_str(
                [0b01000111, 0b11111001,
                 0, 0xFF, 0x12, 0x34]),  # LEA ($FF1234).L, A3
            method_args=(
                3,  # register_index
                7,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_lea_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, 0x138,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.lea,
            program=test_cpu.int_list_to_str(
                [0b01000111, 0b11111010,
                 1, 0x36]),  # LEA ($136, PC), A3
            method_args=(
                3,  # register_index
                7,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)


if __name__ == "__main__":
    unittest.main()
