# -*- coding: utf-8 -*-
"""
Test the MOVE from SR instruction of the 68k CPU.

Created on Mon Sep 25 17:44:41 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestMoveFromSr(unittest.TestCase):

    def test_move_from_sr_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xFFFFFFFF, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=1, init_s=1, init_i=7,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0xFFFFA71F, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            t1=1, s=1, i=7,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.move_from_sr,
            program=test_cpu.int_list_to_str(
                [0b01000000, 0b11000000]),  # MOVE SR, D0
            method_args=(
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_move_from_sr_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=1, init_z=1, init_v=1, init_c=0,
            init_t1=1, init_s=0, init_i=4,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x840E, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=1, v=1, c=0,
            t1=1, s=0, i=4,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.move_from_sr,
            program=test_cpu.int_list_to_str(
                [0b01000000, 0b11000000]),  # MOVE SR, D0
            method_args=(
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_move_from_sr_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, 0xFF1234,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=1, init_z=1, init_v=1, init_c=0,
            init_t1=1, init_s=0, init_i=4,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 0),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, 0xFF1234,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=1, v=1, c=0,
            t1=1, s=0, i=4,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1232, 0),
                (0xFF1234, 0x840E),
                (0xFF1236, 0),
            ),

            # Instruction
            cpu_method=ins.move_from_sr,
            program=test_cpu.int_list_to_str(
                [0b01000000, 0b11010011]),  # MOVE SR, (A3)
            method_args=(
                2,  # ea_mode
                3,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)


if __name__ == "__main__":
    unittest.main()
