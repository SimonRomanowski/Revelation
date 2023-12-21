# -*- coding: utf-8 -*-
"""
Test the EORI to CCR instruction of the 68k CPU.

Created on Sun Sep 24 20:58:08 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestEoriToCcr(unittest.TestCase):

    def test_eori_to_ccr_000(self):
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
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.eori_to_ccr,
            program=test_cpu.int_list_to_str(
                [0x0A, 0x3C,
                 0, 0b11111]),  # EORI #$1F, CCR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_eori_to_ccr_001(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_mem=(),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            memory_values=(),
            cpu_method=ins.eori_to_ccr,
            program=test_cpu.int_list_to_str(
                [0x0A, 0x3C,
                 0, 0b11111]),  # EORI #$1F, CCR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_eori_to_ccr_002(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=1, init_c=0,
            init_mem=(),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=1,
            memory_values=(),
            cpu_method=ins.eori_to_ccr,
            program=test_cpu.int_list_to_str(
                [0x0A, 0x3C,
                 0, 0b11011]),  # EORI #$1B, CCR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)


if __name__ == "__main__":
    unittest.main()
