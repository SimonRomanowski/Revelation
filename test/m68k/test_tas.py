# -*- coding: utf-8 -*-
"""
Test the TAS instruction of the 68k CPU.

Created on Thu Sep 28 11:47:10 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestTas(unittest.TestCase):

    def test_tas_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x12345678, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 0x123456F8, None,
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
            cpu_method=ins.tas,
            program=test_cpu.int_list_to_str(
                [0b01001010, 0b11000010]),  # TAS D2
            method_args=(
                0,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_tas_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x12345600, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 0x12345680, None,
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
            cpu_method=ins.tas,
            program=test_cpu.int_list_to_str(
                [0b01001010, 0b11000010]),  # TAS D2
            method_args=(
                0,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_tas_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x123456E3, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 0x123456E3, None,
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
            cpu_method=ins.tas,
            program=test_cpu.int_list_to_str(
                [0b01001010, 0b11000010]),  # TAS D2
            method_args=(
                0,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_tas_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, 0xFF1234,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 0x2480),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, 0xFF1234,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1234, 0xA480),
            ),

            # Instruction
            cpu_method=ins.tas,
            program=test_cpu.int_list_to_str(
                [0b01001010, 0b11010011]),  # TAS (A3)
            method_args=(
                2,  # ea_mode
                3,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=18)


if __name__ == "__main__":
    unittest.main()
