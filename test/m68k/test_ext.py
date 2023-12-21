# -*- coding: utf-8 -*-
"""
Test the EXT instruction of the 68k CPU.

Created on Mon Sep 25 09:11:01 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestExt(unittest.TestCase):

    def test_ext_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x12, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 0x12, None,
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
            cpu_method=ins.ext,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b10000010]),  # EXT.W D2
            method_args=(
                2,  # register_index
                0,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_ext_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x82, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 0xFF82, None,
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
            cpu_method=ins.ext,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b10000010]),  # EXT.W D2
            method_args=(
                2,  # register_index
                0,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_ext_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x1234, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 0x1234, None,
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
            cpu_method=ins.ext,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b11000010]),  # EXT.L D2
            method_args=(
                2,  # register_index
                1,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_ext_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0xFFFF, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 0xFFFFFFFF, None,
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
            cpu_method=ins.ext,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b11000010]),  # EXT.L D2
            method_args=(
                2,  # register_index
                1,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_ext_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
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
            cpu_method=ins.ext,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b11000010]),  # EXT.L D2
            method_args=(
                2,  # register_index
                1,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)


if __name__ == "__main__":
    unittest.main()
