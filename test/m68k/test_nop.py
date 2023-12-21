# -*- coding: utf-8 -*-
"""
Test the NOP instruction of the 68k CPU.

Created on Tue Sep 26 19:59:21 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestNop(unittest.TestCase):

    def test_nop_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
                    0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0x12345678],
            init_a=[0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
                    0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0x12345678],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=1, init_s=1, init_i=7,
            init_usp=0x87654321,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
               0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0x12345678],
            a=[0x99999999, 0xAAAAAAAA, 0xBBBBBBBB, 0xCCCCCCCC,
               0xDDDDDDDD, 0xEEEEEEEE, 0xFFFFFFFF, 0x12345678],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            t1=1, s=1, i=7,
            usp=0x87654321,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.nop,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b01110001]),  # NOP
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=4)


if __name__ == "__main__":
    unittest.main()
