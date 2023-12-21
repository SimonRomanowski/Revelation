# -*- coding: utf-8 -*-
"""
Test the TST instruction of the 68k CPU.

Created on Thu Sep 28 13:12:42 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestTst(unittest.TestCase):

    def test_tst_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, 0x12345684, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, 0x12345684, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.tst,
            program=test_cpu.int_list_to_str(
                [0b01001010, 0b00000101]),  # TST.B D5
            method_args=(
                0,  # op_size
                0,  # ea_mode
                5,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_tst_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, 0x12340000, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, 0x12340000, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.tst,
            program=test_cpu.int_list_to_str(
                [0b01001010, 0b01000101]),  # TST.W D5
            method_args=(
                1,  # op_size
                0,  # ea_mode
                5,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_tst_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, 0x12340000, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, 0x12340000, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.tst,
            program=test_cpu.int_list_to_str(
                [0b01001010, 0b10000101]),  # TST.L D5
            method_args=(
                2,  # op_size
                0,  # ea_mode
                5,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_tst_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFF784A, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF7848, 0x8234),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0xFF7848, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF7848, 0x8234),
            ),

            # Instruction
            cpu_method=ins.tst,
            program=test_cpu.int_list_to_str(
                [0b01001010, 0b01100001]),  # TST.W -(A1)
            method_args=(
                1,  # op_size
                4,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=10)

    def test_tst_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFF784A, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF7846, 0x7234),
                (0xFF7848, 0x8234),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0xFF7846, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF7846, 0x7234),
                (0xFF7848, 0x8234),
            ),

            # Instruction
            cpu_method=ins.tst,
            program=test_cpu.int_list_to_str(
                [0b01001010, 0b10100001]),  # TST.L -(A1)
            method_args=(
                2,  # op_size
                4,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=14)


if __name__ == "__main__":
    unittest.main()
