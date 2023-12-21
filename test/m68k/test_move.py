# -*- coding: utf-8 -*-
"""
Test the MOVE instruction of the 68k CPU.

Created on Mon Sep 25 14:13:40 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestMove(unittest.TestCase):

    def test_move_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xDEADBEEF, 0x12345678, None, None,
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
            d=[0xDEADBE78, 0x12345678, None, None,
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
            cpu_method=ins.move,
            program=test_cpu.int_list_to_str(
                [0b00010000, 0b00000001]),  # MOVE.B D1, D0
            method_args=(
                0,  # dst_mode
                0,  # dst_register
                0,  # src_mode
                1,  # src_register
                1,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_move_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xDEADBEEF, 0x12345678, None, None,
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
            d=[0xDEAD5678, 0x12345678, None, None,
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
            cpu_method=ins.move,
            program=test_cpu.int_list_to_str(
                [0b00110000, 0b00000001]),  # MOVE.W D1, D0
            method_args=(
                0,  # dst_mode
                0,  # dst_register
                0,  # src_mode
                1,  # src_register
                3,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_move_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xDEADBEEF, 0x12345678, None, None,
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
            d=[0x12345678, 0x12345678, None, None,
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
            cpu_method=ins.move,
            program=test_cpu.int_list_to_str(
                [0b00100000, 0b00000001]),  # MOVE.L D1, D0
            method_args=(
                0,  # dst_mode
                0,  # dst_register
                0,  # src_mode
                1,  # src_register
                2,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_move_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    0xFF3456, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
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
               0xFF3456, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF3454, 0),
                (0xFF3456, 0xFFFF),
                (0xFF3458, 0),
            ),

            # Instruction
            cpu_method=ins.move,
            program=test_cpu.int_list_to_str(
                [0b00111000, 0b10111100, 0xFF, 0xFF]),  # MOVE.W #$FFFF, (A4)
            method_args=(
                2,  # dst_mode
                4,  # dst_register
                7,  # src_mode
                4,  # src_register
                3,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_move_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    0xFF3456, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
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
               0xFF345A, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF3454, 0),
                (0xFF3456, 0x8172),
                (0xFF3458, 0xFFFF),
                (0xFF345A, 0),
            ),

            # Instruction
            cpu_method=ins.move,
            program=test_cpu.int_list_to_str(
                [0b00101000, 0b11111100,
                 0x81, 0x72, 0xFF, 0xFF]),  # MOVE.L #$8172FFFF, (A4)+
            method_args=(
                3,  # dst_mode
                4,  # dst_register
                7,  # src_mode
                4,  # src_register
                2,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_move_005(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF04A0, 0xABCD),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF04A0, 0x1234),
            ),

            # Instruction
            cpu_method=ins.move,
            program=test_cpu.int_list_to_str(
                [0b00110011, 0b11111100,
                 0x12, 0x34,
                 0, 0xFF, 0x04, 0xA0]),  # MOVE.W #$1234, ($FF04A0).L
            method_args=(
                7,  # dst_mode
                1,  # dst_register
                7,  # src_mode
                4,  # src_register
                3,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20)


if __name__ == "__main__":
    unittest.main()
