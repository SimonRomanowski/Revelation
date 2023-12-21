# -*- coding: utf-8 -*-
"""
Test the SUBX instruction of the 68k CPU.

Created on Wed Sep 27 22:19:21 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestSubx(unittest.TestCase):

    def test_subx_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 5, 0xFFFFFF10, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=1, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 5, 0xFFFFFF0A, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.subx,
            program=test_cpu.int_list_to_str(
                [0b10010101, 0b00000001]),  # SUBX.B D1, D2
            method_args=(
                2,  # register_dst
                1,  # register_src
                0,  # op_type
                0,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_subx_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xFFFE, 0x7FFF, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=1, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0xFFFE, 0x8000, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.subx,
            program=test_cpu.int_list_to_str(
                [0b10010101, 0b01000001]),  # SUBX.W D1, D2
            method_args=(
                2,  # register_dst
                1,  # register_src
                0,  # op_type
                1,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_subx_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x1234, 0x12345678, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=1, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0x1234, 0x12344443, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.subx,
            program=test_cpu.int_list_to_str(
                [0b10010101, 0b10000001]),  # SUBX.L D1, D2
            method_args=(
                2,  # register_dst
                1,  # register_src
                0,  # op_type
                2,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_subx_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFF5008, 0xFF800A, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=0, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF5004, 0xDEAD),
                (0xFF5006, 0xBEED),
                (0xFF8006, 0xDEAD),
                (0xFF8008, 0xBEEE),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0xFF5004, 0xFF8006, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF5004, 0xDEAD),
                (0xFF5006, 0xBEED),
                (0xFF8006, 0),
                (0xFF8008, 0),
            ),

            # Instruction
            cpu_method=ins.subx,
            program=test_cpu.int_list_to_str(
                [0b10010101, 0b10001001]),  # SUBX.L -(A1), -(A2)
            method_args=(
                2,  # register_dst
                1,  # register_src
                1,  # op_type
                2,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=30)


if __name__ == "__main__":
    unittest.main()
