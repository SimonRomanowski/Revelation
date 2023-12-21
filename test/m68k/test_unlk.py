# -*- coding: utf-8 -*-
"""
Test the UNLK instruction of the 68k CPU.

Created on Thu Sep 28 13:33:44 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestUnlk(unittest.TestCase):

    def test_unlk_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, 0xFF5006, 0xFF4004],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF4004, 0x1234),
                (0xFF5006, 0xFF),
                (0xFF5008, 0x800A),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, 0xFF800A, 0xFF500A],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF4004, 0x1234),
                (0xFF5006, 0xFF),
                (0xFF5008, 0x800A),
            ),

            # Instruction
            cpu_method=ins.unlk,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b01011110]),  # UNLK A6
            method_args=(
                6,  # register_index
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_unlk_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, 0xFF5006, None,
                    None, None, None, 0xFF4004],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF4004, 0x1234),
                (0xFF5006, 0xFF),
                (0xFF5008, 0x856A),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, 0xFF856A, None,
               None, None, None, 0xFF500A],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF4004, 0x1234),
                (0xFF5006, 0xFF),
                (0xFF5008, 0x856A),
            ),

            # Instruction
            cpu_method=ins.unlk,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b01011010]),  # UNLK A2
            method_args=(
                2,  # register_index
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)


if __name__ == "__main__":
    unittest.main()
