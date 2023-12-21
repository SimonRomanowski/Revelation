# -*- coding: utf-8 -*-
"""
Test the MOVEA instruction of the 68k CPU.

Created on Mon Sep 25 16:18:09 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestMovea(unittest.TestCase):

    def test_movea_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x12345678, None, None,
                    None, None, None, None],
            init_a=[0xDEADBEEF, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0x12345678, None, None,
               None, None, None, None],
            a=[0x5678, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.movea,
            program=test_cpu.int_list_to_str(
                [0b00110000, 0b01000001]),  # MOVEA.W D1, A0
            method_args=(
                0,  # dst_register
                0,  # src_mode
                1,  # src_register
                3,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_movea_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x12345678, None, None,
                    None, None, None, None],
            init_a=[0xDEADBEEF, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0x12345678, None, None,
               None, None, None, None],
            a=[0x12345678, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.movea,
            program=test_cpu.int_list_to_str(
                [0b00100000, 0b01000001]),  # MOVE.L D1, A0
            method_args=(
                0,  # dst_register
                0,  # src_mode
                1,  # src_register
                2,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_movea_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    0xFF3456, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF3456, 0x2345),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               0xFFFFFFFF, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.movea,
            program=test_cpu.int_list_to_str(
                [0b00111000, 0b01111100, 0xFF, 0xFF]),  # MOVE.W #$FFFF, A4
            method_args=(
                4,  # dst_register
                7,  # src_mode
                4,  # src_register
                3,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_movea_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    0xFF3456, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=1, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               0x8172FFFF, None, None, None],
            pc=None,
            x=1, n=0, z=1, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.movea,
            program=test_cpu.int_list_to_str(
                [0b00101000, 0b01111100,
                 0x81, 0x72, 0xFF, 0xFF]),  # MOVEA.L #$8172FFFF, A4
            method_args=(
                4,  # dst_register
                7,  # src_mode
                4,  # src_register
                2,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)


if __name__ == "__main__":
    unittest.main()
