# -*- coding: utf-8 -*-
"""
Test the DBcc instruction of the 68k CPU.

Created on Sun Sep 24 18:07:14 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestDbcc(unittest.TestCase):

    def test_dbcc_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, 5,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, 5,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=4,
            x=None, n=None, z=None, v=None, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.dbcc,
            program=test_cpu.int_list_to_str(
                [0b01010101, 0b11001011,
                 0x04, 0x08]),  # DBCS D3, <+$408>
            method_args=(
                3,  # register_index
                5,  # condition
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_dbcc_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, 5,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, 4,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=0x40A,
            x=None, n=None, z=None, v=None, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.dbcc,
            program=test_cpu.int_list_to_str(
                [0b01010101, 0b11001011,
                 0x04, 0x08]),  # DBCS D3, <+$408>
            method_args=(
                3,  # register_index
                5,  # condition
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=10)

    def test_dbcc_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, 0x12340000,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, 0x1234FFFF,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=0x4,
            x=None, n=None, z=None, v=None, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.dbcc,
            program=test_cpu.int_list_to_str(
                [0b01010101, 0b11001011,
                 0x04, 0x08]),  # DBCS D3, <+$408>
            method_args=(
                3,  # register_index
                5,  # condition
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=14)

    def test_dbcc_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, 7,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=2,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, 6,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=0,
            x=None, n=None, z=None, v=None, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.dbcc,
            program=test_cpu.int_list_to_str(
                [0xFF, 0xFF, 0b01010101, 0b11001011,
                 0xFF, 0xFC]),  # DBCS D3, <-4>
            method_args=(
                3,  # register_index
                5,  # condition
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=10)


if __name__ == "__main__":
    unittest.main()
