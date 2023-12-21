# -*- coding: utf-8 -*-
"""
Test the BCLR instruction of the 68k CPU.

Created on Sat Sep 23 18:55:53 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestBclr(unittest.TestCase):

    def test_bclr_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xF2345678, 31, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0x72345678, 31, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bclr,
            program=test_cpu.int_list_to_str(
                [0b00000011, 0b10000000]),  # BCLR D1, D0
            method_args=(
                1,  # register_index
                1,  # use_register
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bclr_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x72345678, 31, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0x72345678, 31, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bclr,
            program=test_cpu.int_list_to_str(
                [0b00000011, 0b10000000]),  # BCLR D1, D0
            method_args=(
                1,  # register_index
                1,  # use_register
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bclr_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xF2345678, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0xF2345670, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bclr,
            program=test_cpu.int_list_to_str(
                [0b00001000, 0b10000000,
                 0, 3]),  # BCLR #3, D0
            method_args=(
                4,  # register_index
                0,  # use_register
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=14)

    def test_bclr_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[2, None, None, None,
                    None, None, None, None],
            init_a=[None, None, 0xFF0004, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(
                (0xFF0004, 0x5FF),
            ),

            # Expected state
            d=[2, None, None, None,
               None, None, None, None],
            a=[None, None, 0xFF0004, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(
                (0xFF0004, 0x1FF),
            ),

            # Instruction
            cpu_method=ins.bclr,
            program=test_cpu.int_list_to_str(
                [0b00000001, 0b10010010]),  # BCLR D0, (A2)
            method_args=(
                0,  # register_index
                1,  # use_register
                2,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=12)


if __name__ == "__main__":
    unittest.main()
