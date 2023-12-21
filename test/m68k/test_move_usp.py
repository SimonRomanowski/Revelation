# -*- coding: utf-8 -*-
"""
Test the MOVE USP instruction of the 68k CPU.

Created on Mon Sep 25 19:03:31 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestMoveUsp(unittest.TestCase):

    def test_move_usp_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, 0x8736412E,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=1, init_i=None,
            init_usp=0xFF9752,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, 0xFF9752,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=1, i=None,
            usp=0xFF9752,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.move_usp,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b01101011]),  # MOVE USP, A3
            method_args=(
                3,  # register_index
                1,  # direction
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_move_usp_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, 0x8736412E,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=1, init_i=None,
            init_usp=0xFF9752,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, 0x8736412E,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=1, i=None,
            usp=0x8736412E,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.move_usp,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b01100011]),  # MOVE A3, USP
            method_args=(
                3,  # register_index
                0,  # direction
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)


if __name__ == "__main__":
    unittest.main()
