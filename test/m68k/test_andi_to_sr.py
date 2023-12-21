# -*- coding: utf-8 -*-
"""
Test the ANDI to SR instruction of the 68k CPU.

Created on Fri Sep 22 16:52:56 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestAndiToSr(unittest.TestCase):

    def test_andi_to_sr_000(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=0, init_v=0, init_c=1,
            init_t1=1, init_s=1, init_i=7,
            init_mem=(),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=0, c=1,
            t1=1, s=1, i=7,
            memory_values=(),
            cpu_method=ins.andi_to_sr,
            program=test_cpu.int_list_to_str(
                [0b10, 0x7C,
                 0xA7, 0b10011]),  # ANDI #$A71F, SR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_andi_to_sr_001(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=0, init_c=1,
            init_t1=0, init_s=1, init_i=5,
            init_mem=(),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=0, c=0,
            t1=0, s=1, i=4,
            memory_values=(),
            cpu_method=ins.andi_to_sr,
            program=test_cpu.int_list_to_str(
                [0b10, 0x7C,
                 0x26, 0b11110]),  # ANDI #$271F, SR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_andi_to_sr_002(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=0, init_s=1, init_i=3,
            init_mem=(),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=1,
            t1=0, s=0, i=3,
            memory_values=(),
            cpu_method=ins.andi_to_sr,
            program=test_cpu.int_list_to_str(
                [0b10, 0x7C,
                 0x87, 1]),  # ANDI #$700, SR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)


if __name__ == "__main__":
    unittest.main()
