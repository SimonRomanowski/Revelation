# -*- coding: utf-8 -*-
"""
Test the JSR instruction of the 68k CPU.

Created on Mon Sep 25 10:42:04 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestJsr(unittest.TestCase):

    def test_jsr_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0x1234, None, None,
                    None, None, None, 0xFFF558],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFFF558, 0x6789),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0x1234, None, None,
               None, None, None, 0xFFF554],
            pc=0x1234,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFFF554, 0),
                (0xFFF556, 2),
                (0xFFF558, 0x6789),
            ),

            # Instruction
            cpu_method=ins.jsr,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b10010001]),  # JSR (A1)
            method_args=(
                2,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_jsr_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFFF558],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFFF558, 0x6789),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFFF554],
            pc=0x1234,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFFF554, 0),
                (0xFFF556, 6),
                (0xFFF558, 0x6789),
            ),

            # Instruction
            cpu_method=ins.jsr,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b10111001,
                 0, 0, 0x12, 0x34]),  # JSR ($1234).L
            method_args=(
                7,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20)


if __name__ == "__main__":
    unittest.main()
