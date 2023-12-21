# -*- coding: utf-8 -*-
"""
Test the CMPA instruction of the 68k CPU.

Created on Sun Sep 24 16:57:11 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestCmpa(unittest.TestCase):

    def test_cmpa_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 2, None, None,
                    None, None, None, None],
            init_a=[1, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 2, None, None,
               None, None, None, None],
            a=[1, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.cmpa,
            program=test_cpu.int_list_to_str(
                [0b10110000, 0b11000001]),  # CMPA D1, A0
            method_args=(
                0,  # register_index
                0,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_cmpa_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 1, None, None,
                    None, None, None, None],
            init_a=[2, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 1, None, None,
               None, None, None, None],
            a=[2, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.cmpa,
            program=test_cpu.int_list_to_str(
                [0b10110000, 0b11000001]),  # CMPA D1, A0
            method_args=(
                0,  # register_index
                0,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_cmpa_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 2, None, None,
                    None, None, None, None],
            init_a=[2, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 2, None, None,
               None, None, None, None],
            a=[2, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.cmpa,
            program=test_cpu.int_list_to_str(
                [0b10110000, 0b11000001]),  # CMPA D1, A0
            method_args=(
                0,  # register_index
                0,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_cmpa_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xFFFF, None, None,
                    None, None, None, None],
            init_a=[0x7FFFFFFF, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0xFFFF, None, None,
               None, None, None, None],
            a=[0x7FFFFFFF, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.cmpa,
            program=test_cpu.int_list_to_str(
                [0b10110000, 0b11000001]),  # CMPA D1, A0
            method_args=(
                0,  # register_index
                0,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_cmpa_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 1, None, None,
                    None, None, None, None],
            init_a=[0x80000000, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 1, None, None,
               None, None, None, None],
            a=[0x80000000, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=1, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.cmpa,
            program=test_cpu.int_list_to_str(
                [0b10110000, 0b11000001]),  # CMPA D1, A0
            method_args=(
                0,  # register_index
                0,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)

    def test_cmpa_005(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0xFFFF, None, None,
                    None, None, None, None],
            init_a=[0x7FFFFFFF, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, 0xFFFF, None, None,
               None, None, None, None],
            a=[0x7FFFFFFF, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.cmpa,
            program=test_cpu.int_list_to_str(
                [0b10110001, 0b11000001]),  # CMPA.L D1, A0
            method_args=(
                0,  # register_index
                1,  # op_size
                0,  # ea_mode
                1,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=6)


if __name__ == "__main__":
    unittest.main()
