# -*- coding: utf-8 -*-
"""
Test the ANDI to CCR instruction of the 68k CPU.

Created on Fri Sep 22 15:59:01 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestAndiToCcr(unittest.TestCase):

    def test_andi_to_ccr_000(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_mem=(),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            memory_values=(),
            cpu_method=ins.andi_to_ccr,
            program=test_cpu.int_list_to_str(
                [0b10, 0x3C,
                 0, 0b11111]),  # ANDI #$1F, CCR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_andi_to_ccr_001(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=1, init_z=1, init_v=1, init_c=1,
            init_mem=(),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=1,
            memory_values=(),
            cpu_method=ins.andi_to_ccr,
            program=test_cpu.int_list_to_str(
                [0b10, 0x3C,
                 0, 0b10001]),  # ANDI #$1, CCR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_andi_to_ccr_002(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_mem=(),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=1, c=0,
            memory_values=(),
            cpu_method=ins.andi_to_ccr,
            program=test_cpu.int_list_to_str(
                [0b10, 0x3C,
                 0, 0b00010]),  # ANDI #$2, CCR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_andi_to_ccr_003(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=1, init_v=1, init_c=0,
            init_mem=(),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            memory_values=(),
            cpu_method=ins.andi_to_ccr,
            program=test_cpu.int_list_to_str(
                [0b10, 0x3C,
                 0, 0b01100]),  # ANDI #$4, CCR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_andi_to_ccr_004(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=1, init_z=0, init_v=1, init_c=0,
            init_mem=(),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.andi_to_ccr,
            program=test_cpu.int_list_to_str(
                [0b10, 0x3C,
                 0, 0b01001]),  # ANDI #$8, CCR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_andi_to_ccr_005(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=1, init_v=0, init_c=1,
            init_mem=(),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.andi_to_ccr,
            program=test_cpu.int_list_to_str(
                [0b10, 0x3C,
                 0, 0b11010]),  # ANDI #$10, CCR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)


if __name__ == "__main__":
    unittest.main()
