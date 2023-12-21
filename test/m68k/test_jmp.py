# -*- coding: utf-8 -*-
"""
Test the JMP instruction of the 68k CPU.

Created on Mon Sep 25 09:54:11 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestJmp(unittest.TestCase):

    def test_jmp_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, 0x1234,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, 0x1234,
               None, None, None, None],
            pc=0x1234,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.jmp,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b11010011]),  # JMP (A3)
            method_args=(
                2,  # ea_mode
                3,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_jmp_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, 0x1000,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF2144, 0),
                (0xFF2146, 0xFEAB),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, 0x1000,
               None, None, None, None],
            pc=0x1144,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.jmp,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b11101011, 1, 0x44]),  # JMP ($144, A3)
            method_args=(
                5,  # ea_mode
                3,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=10)


if __name__ == "__main__":
    unittest.main()
