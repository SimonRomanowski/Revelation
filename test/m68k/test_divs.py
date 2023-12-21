# -*- coding: utf-8 -*-
"""
Test the DIVS instruction of the 68k CPU.

Created on Sun Sep 24 18:31:15 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestDivs(unittest.TestCase):

    def test_divs_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[16, 2, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x00000008, 2, None, None,
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
            cpu_method=ins.divs,
            program=test_cpu.int_list_to_str(
                [0b10000001, 0b11000001]),  # DIVS D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=158)

    def test_divs_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[17, 2, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x00010008, 2, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.divs,
            program=test_cpu.int_list_to_str(
                [0b10000001, 0b11000001]),  # DIVS D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=158)

    def test_divs_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[9, 10, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x00090000, 10, None, None,
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
            cpu_method=ins.divs,
            program=test_cpu.int_list_to_str(
                [0b10000001, 0b11000001]),  # DIVS D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=158)

    def test_divs_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[100, 0xFFFB, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x0000FFEC, 0xFFFB, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.divs,
            program=test_cpu.int_list_to_str(
                [0b10000001, 0b11000001]),  # DIVS D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=158)

    def test_divs_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xFFFFFF9A, 5, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0xFFFEFFEC, 5, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.divs,
            program=test_cpu.int_list_to_str(
                [0b10000001, 0b11000001]),  # DIVS D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=158)

    def test_divs_005(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x12345, 1, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=0, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x12345, 1, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=1, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.divs,
            program=test_cpu.int_list_to_str(
                [0b10000001, 0b11000001]),  # DIVS D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=158)


if __name__ == "__main__":
    unittest.main()
