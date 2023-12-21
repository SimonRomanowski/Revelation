# -*- coding: utf-8 -*-
"""
Test the MOVEQ instruction of the 68k CPU.

Created on Tue Sep 26 15:33:24 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestMoveq(unittest.TestCase):

    def test_moveq_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x5566BB11, None,
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
            d=[None, None, 0x7F, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.moveq,
            program=test_cpu.int_list_to_str(
                [0b01110100, 0x7F]),  # MOVEQ #$7F, D2
            method_args=(
                2,  # register_index
                0x7F,  # value
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)

    def test_moveq_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, 0x5566BB11, None,
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
            d=[None, None, 0xFFFFFF82, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.moveq,
            program=test_cpu.int_list_to_str(
                [0b01110100, 0x82]),  # MOVEQ #$82, D2
            method_args=(
                2,  # register_index
                0x82,  # value
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=4)


if __name__ == "__main__":
    unittest.main()
