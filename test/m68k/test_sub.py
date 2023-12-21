# -*- coding: utf-8 -*-
"""
Test the SUB instruction of the 68k CPU.

Created on Wed Sep 27 19:25:03 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestSub(unittest.TestCase):

    def test_sub_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x10, 1, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0xF, 1, None,
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
            cpu_method=ins.sub,
            program=test_cpu.int_list_to_str(
                [0b10010010, 0b00000010]),  # SUB.B D2, D1
            method_args=(
                1,  # register_index
                0,  # op_type
                0,  # op_size
                0,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_sub_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x12340000, 2, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0x1234FFFE, 2, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.sub,
            program=test_cpu.int_list_to_str(
                [0b10010010, 0b01000010]),  # SUB.W D2, D1
            method_args=(
                1,  # register_index
                0,  # op_type
                1,  # op_size
                0,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_sub_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x12345678, 0x12345678, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0, 0x12345678, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.sub,
            program=test_cpu.int_list_to_str(
                [0b10010010, 0b10000010]),  # SUB.L D2, D1
            method_args=(
                1,  # register_index
                0,  # op_type
                2,  # op_size
                0,  # ea_mode
                2,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_sub_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 1, None,
                    None, None, None, None],
            init_a=[None, 0xFF5678, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF5678, 0x8000),
                (0xFF567A, 0),
            ),

            # Expected state
            d=[None, None, 1, None,
               None, None, None, None],
            a=[None, 0xFF5678, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=1, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF5678, 0x7FFF),
                (0xFF567A, 0xFFFF),
            ),

            # Instruction
            cpu_method=ins.sub,
            program=test_cpu.int_list_to_str(
                [0b10010101, 0b10010001]),  # SUB.L D2, (A1)
            method_args=(
                2,  # register_index
                1,  # op_type
                2,  # op_size
                2,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_sub_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x8000, None,
                    None, None, None, None],
            init_a=[None, 0xFF5678, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF5678, 0),
            ),

            # Expected state
            d=[None, None, 0x8000, None,
               None, None, None, None],
            a=[None, 0xFF5678, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF5678, 0x8000),
            ),

            # Instruction
            cpu_method=ins.sub,
            program=test_cpu.int_list_to_str(
                [0b10010101, 0b01010001]),  # SUB.W D2, (A1)
            method_args=(
                2,  # register_index
                1,  # op_type
                1,  # op_size
                2,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)


if __name__ == "__main__":
    unittest.main()
