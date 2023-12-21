# -*- coding: utf-8 -*-
"""
Test the MOVEM instruction of the 68k CPU.

Created on Mon Sep 25 19:26:45 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestMovem(unittest.TestCase):

    def test_movem_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x11111111, 0x22222222, 0x33333333, 0x44444444,
                    0x55555555, 0x66666666, 0x77777777, 0x88888888],
            init_a=[0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
                    0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0x12345678],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x11111111, 0x22222222, 0x33333333, 0x44444444,
               0x55555555, 0x66666666, 0x77777777, 0x88888888],
            a=[0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
               0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0x12345678],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFFFF00, 0x1111),
                (0xFFFF02, 0x2222),
                (0xFFFF04, 0x3333),
                (0xFFFF06, 0x4444),
                (0xFFFF08, 0x5555),
                (0xFFFF0A, 0x6666),
                (0xFFFF0C, 0x7777),
                (0xFFFF0E, 0x8888),
                (0xFFFF10, 0x9999),
                (0xFFFF12, 0xAAAA),
                (0xFFFF14, 0xBBBB),
                (0xFFFF16, 0xCCCC),
                (0xFFFF18, 0xDDDD),
                (0xFFFF1A, 0xEEEE),
                (0xFFFF1C, 0xFFFF),
                (0xFFFF1E, 0x5678),
            ),

            # Instruction
            cpu_method=ins.movem,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b10111001,
                 0xFF, 0xFF,
                 0, 0xFF, 0xFF, 0]),  # MOVEM D0-D7/A0-A7, ($FFFF00).L
            method_args=(
                0,  # direction
                0,  # op_size
                7,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16 + 4*16)

    def test_movem_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x11111111, 0x22222222, 0x33333333, 0x44444444,
                    0x55555555, 0x66666666, 0x77777777, 0x88888888],
            init_a=[0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
                    0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0x12345678],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x11111111, 0x22222222, 0x33333333, 0x44444444,
               0x55555555, 0x66666666, 0x77777777, 0x88888888],
            a=[0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
               0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0x12345678],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFFFF00, 0x1111),
                (0xFFFF02, 0x1111),
                (0xFFFF04, 0x2222),
                (0xFFFF06, 0x2222),
                (0xFFFF08, 0x3333),
                (0xFFFF0A, 0x3333),
                (0xFFFF0C, 0x4444),
                (0xFFFF0E, 0x4444),
                (0xFFFF10, 0x5555),
                (0xFFFF12, 0x5555),
                (0xFFFF14, 0x6666),
                (0xFFFF16, 0x6666),
                (0xFFFF18, 0x7777),
                (0xFFFF1A, 0x7777),
                (0xFFFF1C, 0x8888),
                (0xFFFF1E, 0x8888),
                (0xFFFF20, 0x9999),
                (0xFFFF22, 0x9999),
                (0xFFFF24, 0xAAAA),
                (0xFFFF26, 0xAAAA),
                (0xFFFF28, 0xBBBB),
                (0xFFFF2A, 0xBBBB),
                (0xFFFF2C, 0xCCCC),
                (0xFFFF2E, 0xCCCC),
                (0xFFFF30, 0xDDDD),
                (0xFFFF32, 0xDDDD),
                (0xFFFF34, 0xEEEE),
                (0xFFFF36, 0xEEEE),
                (0xFFFF38, 0xFFFF),
                (0xFFFF3A, 0xFFFF),
                (0xFFFF3C, 0x1234),
                (0xFFFF3E, 0x5678),
            ),

            # Instruction
            cpu_method=ins.movem,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b11111001,
                 0xFF, 0xFF,
                 0, 0xFF, 0xFF, 0]),  # MOVEM.L D0-D7/A0-A7, ($FFFF00).L
            method_args=(
                0,  # direction
                1,  # op_size
                7,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16 + 8*16)

    def test_movem_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x11111111, 0x22222222, 0x33333333, 0x44444444,
                    0x55555555, 0x66666666, 0x77777777, 0x88888888],
            init_a=[0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
                    0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0x12345678],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x11111111, 0x22222222, 0x33333333, 0x44444444,
               0x55555555, 0x66666666, 0x77777777, 0x88888888],
            a=[0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
               0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0x12345678],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFFFF00, 0x1111),
                (0xFFFF02, 0x6666),
                (0xFFFF04, 0xBBBB),
                (0xFFFF06, 0x5678),
            ),

            # Instruction
            cpu_method=ins.movem,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b10111001,
                 0x84, 0x21,
                 0, 0xFF, 0xFF, 0]),  # MOVEM D0/D5/A2/A7, ($FFFF00).L
            method_args=(
                0,  # direction
                0,  # op_size
                7,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16 + 4*4)

    def test_movem_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x11111111, 0x22222222, 0x33333333, 0x44444444,
                    0x55555555, 0x66666666, 0x77777777, 0x88888888],
            init_a=[0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
                    0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0xFFFF8A],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x11111111, 0x22222222, 0x33333333, 0x44444444,
               0x55555555, 0x66666666, 0x77777777, 0x88888888],
            a=[0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
               0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0xFFFF7C],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(  # Order is reversed!
                (0xFFFF7C, 0x1111),
                (0xFFFF7E, 0x2222),
                (0xFFFF80, 0x3333),
                (0xFFFF82, 0x6666),
                (0xFFFF84, 0x9999),
                (0xFFFF86, 0xBBBB),
                (0xFFFF88, 0xFF8A),  # Unchanged value of A7!
            ),

            # Instruction
            cpu_method=ins.movem,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b10100111,
                 # Mask is reversed!
                 0xE4, 0xA1]),  # MOVEM D0-D2/D5/A0/A2/A7, -(A7)
            method_args=(
                0,  # direction
                0,  # op_size
                4,  # ea_mode
                7,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8 + 4*7)

    def test_movem_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0, 0, 0, 0,
                    0, 0, 0, 0],
            init_a=[0, 0, 0, 0,
                    0, 0, 0, 0],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFFFF00, 0x1111),
                (0xFFFF02, 0x2222),
                (0xFFFF04, 0x3333),
                (0xFFFF06, 0x4444),
                (0xFFFF08, 0x5555),
                (0xFFFF0A, 0x6666),
                (0xFFFF0C, 0x7777),
                (0xFFFF0E, 0x8888),
                (0xFFFF10, 0x9999),
                (0xFFFF12, 0xAAAA),
                (0xFFFF14, 0xBBBB),
                (0xFFFF16, 0xCCCC),
                (0xFFFF18, 0xDDDD),
                (0xFFFF1A, 0xEEEE),
                (0xFFFF1C, 0xFFFF),
                (0xFFFF1E, 0x5678),
            ),

            # Expected state
            d=[0x1111, 0x2222, 0x3333, 0x4444,
               0x5555, 0x6666, 0x7777, 0xFFFF8888],
            a=[0xFFFF9999, 0xFFFFAAAA, 0xFFFFBBBB, 0xFFFFCCCC,
               0xFFFFDDDD, 0xFFFFEEEE, 0xFFFFFFFF, 0x5678],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFFFF00, 0x1111),
                (0xFFFF02, 0x2222),
                (0xFFFF04, 0x3333),
                (0xFFFF06, 0x4444),
                (0xFFFF08, 0x5555),
                (0xFFFF0A, 0x6666),
                (0xFFFF0C, 0x7777),
                (0xFFFF0E, 0x8888),
                (0xFFFF10, 0x9999),
                (0xFFFF12, 0xAAAA),
                (0xFFFF14, 0xBBBB),
                (0xFFFF16, 0xCCCC),
                (0xFFFF18, 0xDDDD),
                (0xFFFF1A, 0xEEEE),
                (0xFFFF1C, 0xFFFF),
                (0xFFFF1E, 0x5678),
            ),

            # Instruction
            cpu_method=ins.movem,
            program=test_cpu.int_list_to_str(
                [0b01001100, 0b10111001,
                 0xFF, 0xFF,
                 0, 0xFF, 0xFF, 0]),  # MOVEM ($FFFF00).L, D0-D7/A0-A7
            method_args=(
                1,  # direction
                0,  # op_size
                7,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20 + 4*16)

    def test_movem_005(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0, 0, 0, 0,
                    0, 0, 0, 0],
            init_a=[0, 0xFFFF00, 0, 0,
                    0, 0, 0, 0],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFFFF00, 0x1111),
                (0xFFFF02, 0x2222),
                (0xFFFF04, 0x3333),
                (0xFFFF06, 0x4444),
                (0xFFFF08, 0x5555),
                (0xFFFF0A, 0x6666),
                (0xFFFF0C, 0x7777),
                (0xFFFF0E, 0x8888),
            ),

            # Expected state
            d=[0x11112222, 0, 0, 0,
               0, 0, 0x33334444, 0],
            a=[0, 0xFFFF10, 0, 0,
               0, 0, 0x77778888, 0],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFFFF00, 0x1111),
                (0xFFFF02, 0x2222),
                (0xFFFF04, 0x3333),
                (0xFFFF06, 0x4444),
                (0xFFFF08, 0x5555),
                (0xFFFF0A, 0x6666),
                (0xFFFF0C, 0x7777),
                (0xFFFF0E, 0x8888),
            ),

            # Instruction
            cpu_method=ins.movem,
            program=test_cpu.int_list_to_str(
                [0b01001100, 0b11011001,
                 0x42, 0x41]),  # MOVEM.L (A1)+, D0/D6/A1/A6
            method_args=(
                1,  # direction
                1,  # op_size
                3,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12 + 8*4)


if __name__ == "__main__":
    unittest.main()
