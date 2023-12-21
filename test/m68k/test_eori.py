# -*- coding: utf-8 -*-
"""
Test the EORI instruction of the 68k CPU.

Created on Sun Sep 24 20:35:27 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestEori(unittest.TestCase):

    def test_eori_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0, None, None,
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
            d=[None, 0, None, None,
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
            cpu_method=ins.eori,
            program=test_cpu.int_list_to_str(
                [0b00001010, 0b01000001, 0, 0]),  # EOR #0, D1
            method_args=(
                1,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_eori_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xFFFF, None, None,
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
            d=[None, 0xFFFF, None, None,
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
            cpu_method=ins.eori,
            program=test_cpu.int_list_to_str(
                [0b00001010, 0b01000001, 0, 0]),  # EOR #0, D1
            method_args=(
                1,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_eori_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xFFFF, None, None,
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
            d=[None, 0, None, None,
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
            cpu_method=ins.eori,
            program=test_cpu.int_list_to_str(
                [0b00001010, 0b01000001, 0xFF, 0xFF]),  # EOR #$FFFF, D1
            method_args=(
                1,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_eori_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xCCCC, None, None,
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
            d=[None, 0xFFFF, None, None,
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
            cpu_method=ins.eori,
            program=test_cpu.int_list_to_str(
                [0b00001010, 0b01000001, 0x33, 0x33]),  # EOR #$3333, D1
            method_args=(
                1,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_eori_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xFFFFF0F0, None, None,
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
            d=[None, 0xFFFF0F0F, None, None,
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
            cpu_method=ins.eori,
            program=test_cpu.int_list_to_str(
                [0b00001010, 0b01000001, 0xFF, 0xFF]),  # EOR #$FFFF, D1
            method_args=(
                1,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_eori_005(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xFFFFF0F0, None, None,
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
            d=[None, 0xF0F00F0F, None, None,
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
            cpu_method=ins.eori,
            program=test_cpu.int_list_to_str(
                [0b00001010, 0b10000001,
                 0x0F, 0x0F, 0xFF, 0xFF]),  # EOR.L #$F0FFFFF, D1
            method_args=(
                2,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16)


if __name__ == "__main__":
    unittest.main()
