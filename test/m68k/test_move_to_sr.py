# -*- coding: utf-8 -*-
"""
Test the MOVE to SR instruction of the 68k CPU.

Created on Mon Sep 25 18:54:06 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestMoveToSr(unittest.TestCase):

    def test_move_to_sr_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0, None, None,
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
            d=[None, 0, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=0, s=0, i=0,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.move_to_sr,
            program=test_cpu.int_list_to_str(
                [0b01000110, 0b11000001]),  # MOVE D1, SR
            method_args=(
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_move_to_ccr_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xFFFF, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=1, init_i=0,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0xFFFF, None, None,
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
            cpu_method=ins.move_to_sr,
            program=test_cpu.int_list_to_str(
                [0b01000110, 0b11000001]),  # MOVE D1, SR
            method_args=(
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_move_to_ccr_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x8105, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=1, init_v=1, init_c=0,
            init_t1=0, init_s=1, init_i=7,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0x8105, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=1,
            t1=1, s=0, i=1,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.move_to_sr,
            program=test_cpu.int_list_to_str(
                [0b01000110, 0b11000001]),  # MOVE D1, SR
            method_args=(
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)


if __name__ == "__main__":
    unittest.main()
