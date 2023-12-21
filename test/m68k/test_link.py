# -*- coding: utf-8 -*-
"""
Test the LINK instruction of the 68k CPU.

Created on Mon Sep 25 13:00:59 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestLink(unittest.TestCase):

    def test_link_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, 0xFFEACA, None, 0xFFD458],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFFD458, 0x5678),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, 0xFFD454, None, 0xFFD450],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFFD44E, 0),
                (0xFFD450, 0),
                (0xFFD452, 0),
                (0xFFD454, 0xFF),
                (0xFFD456, 0xEACA),
                (0xFFD458, 0x5678),
                (0xFFD45A, 0),
            ),

            # Instruction
            cpu_method=ins.link,
            program=test_cpu.int_list_to_str(
                [0b01001110, 0b01010101, 0xFF, 0xFC]),  # LINK A5, #$FFFC
            method_args=(
                5,  # register_index
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16)


if __name__ == "__main__":
    unittest.main()
