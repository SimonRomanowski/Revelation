# -*- coding: utf-8 -*-
"""
Test the OR instruction of the 68k CPU.

Created on Tue Sep 26 22:06:55 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestOri(unittest.TestCase):

    def test_ori_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, 0x12340F,
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
            d=[None, None, None, 0x12341F,
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
            cpu_method=ins.ori,
            program=test_cpu.int_list_to_str(
                [0b00000000, 0b00000011,
                 0, 0x11]),  # OR.B #$11, D3
            method_args=(
                0,  # op_size
                0,  # ea_mode
                3,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_ori_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, 0xFF762A,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF762A, 0xD19),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, 0xFF762C,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF762A, 0xFF59),
            ),
            # Instruction
            cpu_method=ins.ori,
            program=test_cpu.int_list_to_str(
                [0b00000000, 0b01011011,
                 0xF2, 0x41]),  # OR.W #$F241, (A3)+
            method_args=(
                1,  # op_size
                3,  # ea_mode
                3,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_ori_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, 0xFF762A,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF762A, 0xEDB7),
                (0xFF762C, 0x0D19),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, 0xFF762E,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF762A, 0xFFFF),
                (0xFF762C, 0xFF59),
            ),
            # Instruction
            cpu_method=ins.ori,
            program=test_cpu.int_list_to_str(
                [0b00000000, 0b10011011,
                 0x12, 0x48, 0xF2, 0x41]),  # OR.L #$1248F241, (A3)+
            method_args=(
                2,  # op_size
                3,  # ea_mode
                3,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=28)


if __name__ == "__main__":
    unittest.main()
