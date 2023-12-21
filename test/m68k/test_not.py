# -*- coding: utf-8 -*-
"""
Test the NOT instruction of the 68k CPU.

Created on Tue Sep 26 20:30:41 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestNot(unittest.TestCase):

    def test_not_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0, None, None,
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
            d=[None, 0xFF, None, None,
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
            cpu_method=ins.not_,
            program=test_cpu.int_list_to_str(
                [0b01000110, 0b00000001]),  # NOT.B D1
            method_args=(
                0,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_not_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xFFFFFFFF, None, None,
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
            d=[None, 0xFFFFFF00, None, None,
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
            cpu_method=ins.not_,
            program=test_cpu.int_list_to_str(
                [0b01000110, 0b00000001]),  # NOT.B D1
            method_args=(
                0,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_not_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xFFFFFFFF, None, None,
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
            d=[None, 0xFFFF0000, None, None,
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
            cpu_method=ins.not_,
            program=test_cpu.int_list_to_str(
                [0b01000110, 0b01000001]),  # NOT.W D1
            method_args=(
                1,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_not_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFF0010, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF0010, 0x1234),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0xFF0012, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF0010, 0xEDCB),
            ),
            # Instruction
            cpu_method=ins.not_,
            program=test_cpu.int_list_to_str(
                [0b01000110, 0b01011001]),  # NOT.W (A1)+
            method_args=(
                1,  # op_size
                3,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_not_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFF0010, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF0010, 0x1234),
                (0xFF0012, 0x5678),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0xFF0014, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF0010, 0xEDCB),
                (0xFF0012, 0xA987),
            ),
            # Instruction
            cpu_method=ins.not_,
            program=test_cpu.int_list_to_str(
                [0b01000110, 0b10011001]),  # NOT.L (A1)+
            method_args=(
                2,  # op_size
                3,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_not_005(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xABCDEF01, None, None,
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
            d=[None, 0x543210FE, None, None,
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
            cpu_method=ins.not_,
            program=test_cpu.int_list_to_str(
                [0b01000110, 0b10000001]),  # NOT.L D1
            method_args=(
                2,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)


if __name__ == "__main__":
    unittest.main()
