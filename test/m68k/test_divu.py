# -*- coding: utf-8 -*-
"""
Test the DIVU instruction of the 68k CPU.

Created on Sun Sep 24 19:59:59 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestDivu(unittest.TestCase):

    def test_divu_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[16, 2, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=0, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x00000008, 2, None, None,
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
            cpu_method=ins.divu,
            program=test_cpu.int_list_to_str(
                [0b10000000, 0b11000001]),  # DIVU D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=140)

    def test_divu_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[10, 3, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=0, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x00010003, 3, None, None,
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
            cpu_method=ins.divu,
            program=test_cpu.int_list_to_str(
                [0b10000000, 0b11000001]),  # DIVU D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=140)

    def test_divu_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x10000, 2, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=0, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x00008000, 2, None, None,
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
            cpu_method=ins.divu,
            program=test_cpu.int_list_to_str(
                [0b10000000, 0b11000001]),  # DIVU D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=140)

    def test_divu_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[6, 9, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=0, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x00060000, 9, None, None,
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
            cpu_method=ins.divu,
            program=test_cpu.int_list_to_str(
                [0b10000000, 0b11000001]),  # DIVU D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=140)

    def test_divu_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x1234567, 3, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=0, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x1234567, 3, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=1, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.divu,
            program=test_cpu.int_list_to_str(
                [0b10000000, 0b11000001]),  # DIVU D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=140)

    def test_divu_005(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0xFFFF0, 0xFFFF, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=0, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x00000010, 0xFFFF, None, None,
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
            cpu_method=ins.divu,
            program=test_cpu.int_list_to_str(
                [0b10000000, 0b11000001]),  # DIVU D1, D0
            method_args=(
                0,  # register_index
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=140)


if __name__ == "__main__":
    unittest.main()
