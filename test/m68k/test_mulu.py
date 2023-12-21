# -*- coding: utf-8 -*-
"""
Test the MULU instruction of the 68k CPU.

Created on Tue Sep 26 16:37:26 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestMulu(unittest.TestCase):

    def test_mulu_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0b101, 0b11, None, None,
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
            d=[0b1111, 0b11, None, None,
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
            cpu_method=ins.mulu,
            program=test_cpu.int_list_to_str(
                [0b11000000, 0b11000001]),  # MULU D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            # 38+2n; n = number of "1"s in x
            cycle=38+2*2)

    def test_muls_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[2, 0x5555, None, None,
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
            d=[0xAAAA, 0x5555, None, None,
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
            cpu_method=ins.mulu,
            program=test_cpu.int_list_to_str(
                [0b11000000, 0b11000001]),  # MULU D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            # 38+2n; n = number of "1"s in x
            cycle=38+2*8)

    def test_muls_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[2, 0xFFFF, None, None,
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
            d=[0x1FFFE, 0xFFFF, None, None,
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
            cpu_method=ins.mulu,
            program=test_cpu.int_list_to_str(
                [0b11000000, 0b11000001]),  # MULU D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            # 38+2n; n = number of "1"s in x
            cycle=38+2*16)

    def test_muls_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x1234, 0, None, None,
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
            d=[0, 0, None, None,
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
            cpu_method=ins.mulu,
            program=test_cpu.int_list_to_str(
                [0b11000000, 0b11000001]),  # MULU D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            # 38+2n; n = number of "1"s in x
            cycle=38+2*0)

    def test_muls_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xFFFF, 0x1234, None, None,
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
            d=[0x1233EDCC, 0x1234, None, None,
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
            cpu_method=ins.mulu,
            program=test_cpu.int_list_to_str(
                [0b11000000, 0b11000001]),  # MULU D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            # 38+2n; n = number of "1"s in x
            cycle=38+2*5)


if __name__ == "__main__":
    unittest.main()
