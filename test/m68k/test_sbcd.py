# -*- coding: utf-8 -*-
"""
Test the SBCD instruction of the 68k CPU.

Created on Wed Sep 27 16:24:10 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestSbcd(unittest.TestCase):

    def test_sbcd_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x11, 0x33,
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
            d=[None, None, 0x11, 0x22,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=None, z=0, v=None, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.sbcd,
            program=test_cpu.int_list_to_str(
                [0b10000111, 0b00000010]),  # SBCD D2, D3
            method_args=(
                3,  # register_dst
                2,  # register_src
                0,  # op_type
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_sbcd_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x11, 0x11,
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
            d=[None, None, 0x11, 0x00,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=None, z=1, v=None, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.sbcd,
            program=test_cpu.int_list_to_str(
                [0b10000111, 0b00000010]),  # SBCD D2, D3
            method_args=(
                3,  # register_dst
                2,  # register_src
                0,  # op_type
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_sbcd_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x11, 0x13,
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
            d=[None, None, 0x11, 0x01,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=None, z=0, v=None, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.sbcd,
            program=test_cpu.int_list_to_str(
                [0b10000111, 0b00000010]),  # SBCD D2, D3
            method_args=(
                3,  # register_dst
                2,  # register_src
                0,  # op_type
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_sbcd_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x11, 0x01,
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
            d=[None, None, 0x11, 0x89,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=None, z=0, v=None, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.sbcd,
            program=test_cpu.int_list_to_str(
                [0b10000111, 0b00000010]),  # SBCD D2, D3
            method_args=(
                3,  # register_dst
                2,  # register_src
                0,  # op_type
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_sbcd_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, 0xFF1234, 0xFFBCDE,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=None, init_z=1, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1232, 0x5440),
                (0xFFBCDC, 0x7820),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, 0xFF1233, 0xFFBCDD,
               None, None, None, None],
            pc=None,
            x=1, n=None, z=0, v=None, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1232, 0x5440),
                (0xFFBCDC, 0x7879),
            ),

            # Instruction
            cpu_method=ins.sbcd,
            program=test_cpu.int_list_to_str(
                [0b10000111, 0b00001010]),  # SBCD -(A2), -(A3)
            method_args=(
                3,  # register_dst
                2,  # register_src
                1,  # op_type
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=18)

    def test_sbcd_005(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x11, 0x11,
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
            d=[None, None, 0x11, 0x00,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=None, z=0, v=None, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.sbcd,
            program=test_cpu.int_list_to_str(
                [0b10000111, 0b00000010]),  # SBCD D2, D3
            method_args=(
                3,  # register_dst
                2,  # register_src
                0,  # op_type
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)


if __name__ == "__main__":
    unittest.main()
