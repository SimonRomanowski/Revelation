# -*- coding: utf-8 -*-
"""
Test the PEA instruction of the 68k CPU.

Created on Tue Sep 26 22:31:23 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestPea(unittest.TestCase):

    def test_pea_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0x567800, None, None,
                    None, None, None, 0xFF1234],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 0xABCD),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0x567800, None, None,
               None, None, None, 0xFF1230],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1230, 0x56),
                (0xFF1232, 0x7800),
                (0xFF1234, 0xABCD),
            ),
            # Instruction
            cpu_method=ins.pea,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b01010001]),  # PEA (A1)
            method_args=(
                2,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_pea_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0x567800, None, None,
                    None, None, None, 0xFF1234],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 0xABCD),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0x567800, None, None,
               None, None, None, 0xFF1230],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1230, 0x56),
                (0xFF1232, 0x7956),
                (0xFF1234, 0xABCD),
            ),
            # Instruction
            cpu_method=ins.pea,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b01101001,
                 0x01, 0x56]),  # PEA ($156, A1)
            method_args=(
                5,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_pea_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFF1234],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 0xABCD),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFF1230],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1230, 0xFF),
                (0xFF1232, 0xB002),
                (0xFF1234, 0xABCD),
            ),
            # Instruction
            cpu_method=ins.pea,
            program=test_cpu.int_list_to_str(
                [0b01001000, 0b01111001,
                 0x00, 0xFF, 0xB0, 0x02]),  # PEA ($FFB002).L
            method_args=(
                7,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20)


if __name__ == "__main__":
    unittest.main()
