# -*- coding: utf-8 -*-
"""
Test the EXG instruction of the 68k CPU.

Created on Mon Sep 25 08:54:55 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestExg(unittest.TestCase):

    def test_exg_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x12345678, 0xABCDEF12, None, None,
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
            d=[0xABCDEF12, 0x12345678, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.exg,
            program=test_cpu.int_list_to_str(
                [0b11000001, 0b01000001]),  # EXG D1, D0
            method_args=(
                0,  # register_x
                1,  # register_y
                8,  # op_type
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_exg_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[0xABCDEF12, 0x12345678, None, None,
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
            a=[0x12345678, 0xABCDEF12, None, None,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.exg,
            program=test_cpu.int_list_to_str(
                [0b11000001, 0b01001001]),  # EXG A1, A0
            method_args=(
                0,  # register_x
                1,  # register_y
                9,  # op_type
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_exg_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xABCDEF12, None, None, None,
                    None, None, None, None],
            init_a=[None, 0x12345678, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x12345678, None, None, None,
               None, None, None, None],
            a=[None, 0xABCDEF12, None, None,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.exg,
            program=test_cpu.int_list_to_str(
                [0b11000001, 0b10001001]),  # EXG A1, D0
            method_args=(
                0,  # register_x
                1,  # register_y
                17,  # op_type
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)


if __name__ == "__main__":
    unittest.main()
