# -*- coding: utf-8 -*-
"""
Test the SUBI instruction of the 68k CPU.

Created on Wed Sep 27 21:13:23 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestSubi(unittest.TestCase):

    def test_subi_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x55, None, None,
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
            d=[None, 0x52, None, None,
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
            cpu_method=ins.subi,
            program=test_cpu.int_list_to_str(
                [0b00000100, 0b00000001, 0, 3]),  # SUB.B #3, D1
            method_args=(
                0,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_subi_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFF67C0, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF67C0, 0x7FFF),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=0, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF67C0, 0x8001),
            ),

            # Instruction
            cpu_method=ins.subi,
            program=test_cpu.int_list_to_str(
                [0b00000100, 0b01010001, 0xFF, 0xFE]),  # SUB.W #$FFFE, (A1)
            method_args=(
                1,  # op_size
                2,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_subi_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0xFF67C0, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF67C0, 4),
                (0xFF67C2, 0x2345),
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
                (0xFF67C0, 0xFFFF),
                (0xFF67C2, 0xFFFF),
            ),

            # Instruction
            cpu_method=ins.subi,
            program=test_cpu.int_list_to_str(
                [0b00000100, 0b10010001,
                 0, 4, 0x23, 0x46]),  # SUB.L #$42346, (A1)
            method_args=(
                2,  # op_size
                2,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=28)

    def test_subi_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x5678A, None, None,
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
            d=[None, 1, None, None,
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
            cpu_method=ins.subi,
            program=test_cpu.int_list_to_str(
                [0b00000100, 0b10000001,
                 0, 5, 0x67, 0x89]),  # SUB.L #$56789, D1
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
