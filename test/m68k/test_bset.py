# -*- coding: utf-8 -*-
"""
Test the BSET instruction of the 68k CPU.

Created on Sat Sep 23 21:03:19 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestBset(unittest.TestCase):

    def test_bset_000(self):
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
            d=[0xF2345678, 31, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bset,
            program=test_cpu.int_list_to_str(
                [0b00000011, 0b11000000]),  # BSET D1, D0
            method_args=(
                1,  # register_index
                1,  # use_register
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bset_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x82345678, 31, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0x82345678, 31, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bset,
            program=test_cpu.int_list_to_str(
                [0b00000011, 0b11000000]),  # BSET D1, D0
            method_args=(
                1,  # register_index
                1,  # use_register
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bset_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x82345678, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0x823456F8, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bset,
            program=test_cpu.int_list_to_str(
                [0b00001000, 0b11000000,
                 0, 7]),  # BSET #7, D0
            method_args=(
                4,  # register_index
                0,  # use_register
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_bset_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, 0,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(
                (0xFF1234, 0x5400),
            ),

            # Expected state
            d=[None, None, None, 0,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(
                (0xFF1232, 0),
                (0xFF1234, 0x5500),
                (0xFF1236, 0),
            ),

            # Instruction
            cpu_method=ins.bset,
            program=test_cpu.int_list_to_str(
                [0b00000111, 0b11111001,
                 0x00, 0xFF, 0x12, 0x34]),  # BSET D3, ($FF1234).L
            method_args=(
                3,  # register_index
                1,  # use_register
                7,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_bset_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(
                (0xFF1234, 0x5455),
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
                (0xFF1232, 0),
                (0xFF1234, 0x7455),
                (0xFF1236, 0),
            ),

            # Instruction
            cpu_method=ins.bset,
            program=test_cpu.int_list_to_str(
                [0b00001000, 0b11111001,
                 0, 5,
                 0x00, 0xFF, 0x12, 0x34]),  # BSET #5, ($FF1234).L
            method_args=(
                4,  # register_index
                0,  # use_register
                7,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=24)


if __name__ == "__main__":
    unittest.main()
