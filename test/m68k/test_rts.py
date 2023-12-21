# -*- coding: utf-8 -*-
"""
Test the RTS instruction of the 68k CPU.

Created on Wed Sep 27 16:12:01 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestRts(unittest.TestCase):

    def test_rts_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFF1002],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=1, init_s=0, init_i=7,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1002, 3),
                (0xFF1004, 0x50B2)
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFF1006],
            pc=0x350B2,
            x=1, n=1, z=1, v=1, c=1,
            t1=1, s=0, i=7,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.rts,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b01110101]),  # RTS
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_rte_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFF1002],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=1, init_i=0,
            init_usp=0xFF2000,
            init_ssp=None,
            init_mem=(
                (0xFF1002, 3),
                (0xFF1004, 0x50B2)
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFF1006],
            pc=0x350B2,
            x=0, n=0, z=0, v=0, c=0,
            t1=0, s=1, i=0,
            usp=0xFF2000,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.rts,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b01110101]),  # RTR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=16)


if __name__ == "__main__":
    unittest.main()
