# -*- coding: utf-8 -*-
"""
Test the Scc instruction of the 68k CPU.

Created on Wed Sep 27 18:54:44 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestStop(unittest.TestCase):

    def test_stop_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=1, init_i=0,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            t1=1, s=1, i=7,
            usp=None,
            ssp=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.stop,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b01110010, 0xA7, 0x1F]),  # STOP
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=4)


if __name__ == "__main__":
    unittest.main()
