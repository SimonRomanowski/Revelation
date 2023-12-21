# -*- coding: utf-8 -*-
"""
Test the BCHG instruction of the 68k CPU.

Created on Sat Sep 23 14:45:39 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestBchg(unittest.TestCase):

    def test_bchg_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x12345678, 31, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0x92345678, 31, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bchg,
            program=test_cpu.int_list_to_str(
                [0b00000011, 0b01000000]),  # BCHG D1, D0
            method_args=(
                1,  # register_index
                1,  # use_register
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bchg_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x12345678, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0x52345678, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bchg,
            program=test_cpu.int_list_to_str(
                [0b00001000, 0b01000000,
                 0, 30]),  # BCHG #30, D0
            method_args=(
                4,  # register_index
                0,  # use_register
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_bchg_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x12345678, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0x12345670, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bchg,
            program=test_cpu.int_list_to_str(
                [0b00001000, 0b01000000,
                 0, 3]),  # BCHG #3, D0
            method_args=(
                4,  # register_index
                0,  # use_register
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_bchg_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, 8, None, None],
            init_a=[None, None, None, 0xFF79B2,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(
                (0xFF7AB2, 0x5628),
            ),

            # Expected state
            d=[None, None, None, None,
               None, 8, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(
                (0xFF7AB0, 0),
                (0xFF7AB2, 0x5728),
                (0xFF7AB4, 0),
            ),

            # Instruction
            cpu_method=ins.bchg,
            program=test_cpu.int_list_to_str(
                [0b00001001, 0b01101011,
                 1, 0]),  # BCHG D5, ($100, A3)
            method_args=(
                3,  # register_index
                1,  # use_register
                5,  # ea_mode
                3,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_bchg_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, 0xFF79B2,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(
                (0xFF7AB2, 0x5478),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(
                (0xFF7AB0, 0),
                (0xFF7AB2, 0x5678),
                (0xFF7AB4, 0),
            ),

            # Instruction
            cpu_method=ins.bchg,
            program=test_cpu.int_list_to_str(
                [0b00001000, 0b01101011,
                 0, 1,
                 1, 0]),  # BCHG #1, ($100, A3)
            method_args=(
                4,  # register_index
                0,  # use_register
                5,  # ea_mode
                3,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20)


if __name__ == "__main__":
    unittest.main()
