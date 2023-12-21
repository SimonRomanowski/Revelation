# -*- coding: utf-8 -*-
"""
Test the ROXL/ROXR instruction of the 68k CPU.

Created on Wed Sep 27 12:49:51 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestRoxlToData(unittest.TestCase):

    def test_roxl_to_data_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, 0b01101001, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, 0b11010011, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.roxl_roxr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100011, 0b00010101]),  # ROXL.B #1, D5
            method_args=(
                5,  # register_index
                1,  # rotate_amount
                0,  # op_type
                0,  # op_size
                1,  # direction
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6+2*1)

    def test_roxl_to_data_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, 0b0110100101110010, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, 0b0100101110010001, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=0, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.roxl_roxr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100111, 0b01010101]),  # ROXL.W #3, D5
            method_args=(
                5,  # register_index
                3,  # rotate_amount
                0,  # op_type
                1,  # op_size
                1,  # direction
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6+2*3)

    def test_roxl_to_data_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 6, None,
                    None, 0b01001011100100110100101110010011, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 6, None,
               None, 0b11100100110100101110010011101001, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.roxl_roxr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100101, 0b10110101]),  # ROXL.L D2, D5
            method_args=(
                5,  # register_index
                2,  # rotate_amount
                1,  # op_type
                2,  # op_size
                1,  # direction
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8+2*6)

    def test_roxl_to_data_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0, None, None, None,
                    None, 0xB5, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0, None, None, None,
               None, 0xB5, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.roxl_roxr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100001, 0b00110101]),  # ROXL.B D0, D5
            method_args=(
                5,  # register_index
                0,  # rotate_amount
                1,  # op_type
                0,  # op_size
                1,  # direction
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_roxl_to_data_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, 0, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, 1, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.roxl_roxr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100011, 0b00010101]),  # ROXL.B #1, D5
            method_args=(
                5,  # register_index
                1,  # rotate_amount
                0,  # op_type
                0,  # op_size
                1,  # direction
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6+2*1)


class TestRoxrToData(unittest.TestCase):

    def test_roxr_to_data_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, 0b01101000, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, 0b10110100, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.roxl_roxr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100010, 0b00010101]),  # ROXR.B #1, D5
            method_args=(
                5,  # register_index
                1,  # rotate_amount
                0,  # op_type
                0,  # op_size
                0,  # direction
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6+2*1)

    def test_roxr_to_data_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, 0b0110100101110010, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, 0b1010110100101110, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.roxl_roxr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100110, 0b01010101]),  # ROXR.W #3, D5
            method_args=(
                5,  # register_index
                3,  # rotate_amount
                0,  # op_type
                1,  # op_size
                0,  # direction
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6+2*3)

    def test_roxr_to_data_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 6, None,
                    None, 0b01001011100100110100101110010011, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, 6, None,
               None, 0b10011101001011100100110100101110, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.roxl_roxr_to_data,
            program=test_cpu.int_list_to_str(
                [0b11100100, 0b10110101]),  # ROXR.L D2, D5
            method_args=(
                5,  # register_index
                2,  # rotate_amount
                1,  # op_type
                2,  # op_size
                0,  # direction
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8+2*6)


class TestRoxlToMem(unittest.TestCase):

    def test_roxl_to_mem_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    0xFF1234, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 0b0001110010110100),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1234, 0b0011100101101001),
            ),
            # Instruction
            cpu_method=ins.roxl_roxr_to_mem,
            program=test_cpu.int_list_to_str(
                [0b11100101, 0b11010100]),  # ROXL (A4)
            method_args=(
                1,  # direction
                2,  # ea_mode
                4,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_roxl_to_mem_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    0xFF1234, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 0b1101110010110100),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1234, 0b1011100101101001),
            ),
            # Instruction
            cpu_method=ins.roxl_roxr_to_mem,
            program=test_cpu.int_list_to_str(
                [0b11100101, 0b11010100]),  # ROXL (A4)
            method_args=(
                1,  # direction
                2,  # ea_mode
                4,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)


class TestRoxrToMem(unittest.TestCase):

    def test_roxr_to_mem_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    0xFF1234, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 0b1001110010110100),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1234, 0b1100111001011010),
            ),
            # Instruction
            cpu_method=ins.roxl_roxr_to_mem,
            program=test_cpu.int_list_to_str(
                [0b11100100, 0b11010100]),  # ROXR (A4)
            method_args=(
                0,  # direction
                2,  # ea_mode
                4,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_roxr_to_mem_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    0xFF1234, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 0b1101110010110100),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1234, 0b1110111001011010),
            ),
            # Instruction
            cpu_method=ins.roxl_roxr_to_mem,
            program=test_cpu.int_list_to_str(
                [0b11100100, 0b11010100]),  # ROXR (A4)
            method_args=(
                0,  # direction
                2,  # ea_mode
                4,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)


if __name__ == "__main__":
    unittest.main()
