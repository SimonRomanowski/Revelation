# -*- coding: utf-8 -*-
"""
Test the NEGX instruction of the 68k CPU.

Created on Tue Sep 26 19:40:37 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestNegx(unittest.TestCase):

    def test_negx_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=None, init_z=0, init_v=None, init_c=None,
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
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.negx,
            program=test_cpu.int_list_to_str(
                [0b01000000, 0b00000001]),  # NEGX.B D1
            method_args=(
                0,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_negx_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=None, init_z=1, init_v=None, init_c=None,
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
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.negx,
            program=test_cpu.int_list_to_str(
                [0b01000000, 0b00000001]),  # NEGX.B D1
            method_args=(
                0,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_negx_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xFF, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=1, init_v=None, init_c=None,
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
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.negx,
            program=test_cpu.int_list_to_str(
                [0b01000000, 0b00000001]),  # NEGX.B D1
            method_args=(
                0,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_negx_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x8000, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=1, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0x7FFF, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=0, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.negx,
            program=test_cpu.int_list_to_str(
                [0b01000000, 0b01000001]),  # NEGX.W D1
            method_args=(
                1,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_negx_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x12340002, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=1, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0x1234FFFD, None, None,
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
            cpu_method=ins.negx,
            program=test_cpu.int_list_to_str(
                [0b01000000, 0b01000001]),  # NEGX.W D1
            method_args=(
                1,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_negx_005(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x8000, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=None, init_z=1, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0x8000, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.negx,
            program=test_cpu.int_list_to_str(
                [0b01000000, 0b01000001]),  # NEGX.W D1
            method_args=(
                1,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_negx_006(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, 0xFF1234,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=1, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 0xFFFF),
                (0xFF1236, 0xFFFE),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, 0xFF1234,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=0, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1234, 0),
                (0xFF1236, 1),
            ),
            # Instruction
            cpu_method=ins.negx,
            program=test_cpu.int_list_to_str(
                [0b01000000, 0b10010011]),  # NEGX.L (A3)
            method_args=(
                2,  # op_size
                2,  # ea_mode
                3,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20)


if __name__ == "__main__":
    unittest.main()
