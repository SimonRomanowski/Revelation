# -*- coding: utf-8 -*-
"""
Test the LSd instruction of the 68k CPU.

Created on Mon Sep 25 13:26:05 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestLslToData(unittest.TestCase):

    def test_lsl_to_data_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[1, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[4, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.lsl_lsr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100101, 0b01001000]),  # LSL #2, D0
            method_args=(
                0,  # register_index
                2,  # shift_amount
                0,  # op_type
                1,  # op_size
                1,  # direction
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_lsl_to_data_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xFFFF8000, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=0, init_i=None,
            init_mem=(),

            # Expected state
            d=[0xFFFF0000, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=1, v=1, c=1,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.lsl_lsr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100011, 0b01001000]),  # LSL #1, D0
            method_args=(
                0,  # register_index
                1,  # shift_amount
                0,  # op_type
                1,  # op_size
                1,  # direction
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_lsl_to_data_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xFFFF8000, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0xFFFE0000, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=1,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.lsl_lsr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100101, 0b10001000]),  # LSL #2, D0
            method_args=(
                0,  # register_index
                2,  # shift_amount
                0,  # op_type
                2,  # op_size
                1,  # direction
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=12)

    def test_lsl_to_data_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xF7FF8000, None, 6, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0xFFE00000, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=1, c=1,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.lsl_lsr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100101, 0b10101000]),  # LSL D2, D0
            method_args=(
                0,  # register_index
                2,  # shift_amount
                1,  # op_type
                2,  # op_size
                1,  # direction
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=20)

    def test_lsl_to_data_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[1, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0x100, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.lsl_lsr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100001, 0b01001000]),  # LSL #8, D0
            method_args=(
                0,  # register_index
                0,  # shift_amount
                0,  # op_type
                1,  # op_size
                1,  # direction
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=22)


class TestLsrToData(unittest.TestCase):

    def test_lsr_to_data_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[8, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[2, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.lsl_lsr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100100, 0b01001000]),  # LSR #2, D0
            method_args=(
                0,  # register_index
                2,  # shift_amount
                0,  # op_type
                1,  # op_size
                0,  # direction
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_lsr_to_data_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[8, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=1, v=0, c=1,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.lsl_lsr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11101000, 0b01001000]),  # LSR #4, D0
            method_args=(
                0,  # register_index
                4,  # shift_amount
                0,  # op_type
                1,  # op_size
                0,  # direction
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=14)

    def test_lsr_to_data_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xFFFFFF81, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[0xFFFF7FC0, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=1, c=1,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.lsl_lsr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100010, 0b01001000]),  # LSR #1, D0
            method_args=(
                0,  # register_index
                1,  # shift_amount
                0,  # op_type
                1,  # op_size
                0,  # direction
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)


class TestLslToMem(unittest.TestCase):

    def test_lsl_to_mem_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFFAB44, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(
                (0xFFAB44, 2),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0xFFAB44, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(
                (0xFFAB42, 0),
                (0xFFAB44, 4),
                (0xFFAB46, 0),
            ),

            # Instruction
            cpu_method=ins.lsl_lsr_to_mem,
            program=test_cpu.int_list_to_str(
                [0b11100011, 0b11010001]),  # LSL (A1)
            method_args=(
                1,  # direction
                2,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=12)

    def test_lsl_to_mem_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFFAB44, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(
                (0xFFAB44, 0xA000),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0xFFAB46, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=1, c=1,
            t1=None, s=None, i=None,
            memory_values=(
                (0xFFAB42, 0),
                (0xFFAB44, 0x4000),
                (0xFFAB46, 0),
            ),

            # Instruction
            cpu_method=ins.lsl_lsr_to_mem,
            program=test_cpu.int_list_to_str(
                [0b11100011, 0b11011001]),  # LSL (A1)+
            method_args=(
                1,  # direction
                3,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=12)


class TestLsrToMem(unittest.TestCase):

    def test_lsr_to_mem_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFFAB44, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(
                (0xFFAB44, 2),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0xFFAB44, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            memory_values=(
                (0xFFAB42, 0),
                (0xFFAB44, 1),
                (0xFFAB46, 0),
            ),

            # Instruction
            cpu_method=ins.lsl_lsr_to_mem,
            program=test_cpu.int_list_to_str(
                [0b11100010, 0b11010001]),  # LSR (A1)
            method_args=(
                0,  # direction
                2,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=12)

    def test_lsr_to_mem_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFFAB44, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(
                (0xFFAB44, 0x8003),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0xFFAB44, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=1, c=1,
            t1=None, s=None, i=None,
            memory_values=(
                (0xFFAB42, 0),
                (0xFFAB44, 0x4001),
                (0xFFAB46, 0),
            ),

            # Instruction
            cpu_method=ins.lsl_lsr_to_mem,
            program=test_cpu.int_list_to_str(
                [0b11100010, 0b11010001]),  # LSR (A1)
            method_args=(
                0,  # direction
                2,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=12)


if __name__ == "__main__":
    unittest.main()
