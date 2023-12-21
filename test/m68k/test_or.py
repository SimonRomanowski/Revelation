# -*- coding: utf-8 -*-
"""
Test the OR instruction of the 68k CPU.

Created on Tue Sep 26 21:45:12 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestOr(unittest.TestCase):

    def test_or_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x556677F0, None, 0x12340F,
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
            d=[None, 0x556677F0, None, 0x1234FF,
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
            cpu_method=ins.or_,
            program=test_cpu.int_list_to_str(
                [0b10000110, 0b00000001]),  # OR.B D1, D3
            method_args=(
                3,  # register_index
                0,  # op_type
                0,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_or_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x556677F0, None, 0x12340F,
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
            d=[None, 0x556677F0, None, 0x1277FF,
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
            cpu_method=ins.or_,
            program=test_cpu.int_list_to_str(
                [0b10000110, 0b01000001]),  # OR.W D1, D3
            method_args=(
                3,  # register_index
                0,  # op_type
                1,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_or_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x556677F0, None, 0x12340F,
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
            d=[None, 0x556677F0, None, 0x557677FF,
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
            cpu_method=ins.or_,
            program=test_cpu.int_list_to_str(
                [0b10000110, 0b10000001]),  # OR.L D1, D3
            method_args=(
                3,  # register_index
                0,  # op_type
                2,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_or_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x556677F0, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFF3400],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF3400, 0x8BA0),
            ),

            # Expected state
            d=[None, 0x556677F0, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF3400, 0xFFF0),
            ),
            # Instruction
            cpu_method=ins.or_,
            program=test_cpu.int_list_to_str(
                [0b10000011, 0b01010111]),  # OR.W D1, (A7)
            method_args=(
                1,  # register_index
                1,  # op_type
                1,  # op_size
                2,  # ea_mode
                7,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_or_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x556677F0, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFF3400],
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=1, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF3400, 0x8BA0),
                (0xFF3402, 0x7532),
            ),

            # Expected state
            d=[None, 0x556677F0, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFF3400],
            pc=None,
            x=1, n=1, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF3400, 0xDFE6),
                (0xFF3402, 0x77F2),
            ),
            # Instruction
            cpu_method=ins.or_,
            program=test_cpu.int_list_to_str(
                [0b10000011, 0b10010111]),  # OR.L D1, (A7)
            method_args=(
                1,  # register_index
                1,  # op_type
                2,  # op_size
                2,  # ea_mode
                7,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20)


if __name__ == "__main__":
    unittest.main()
