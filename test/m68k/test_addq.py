# -*- coding: utf-8 -*-
"""
Test the ADDQ instruction of the 68k CPU.

Created on Wed Sep 20 15:15:31 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestAddq(unittest.TestCase):

    def test_addq_000(self):
        test_cpu.test_instruction(
            init_d=[None, 0x1234FFFB, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[None, 0x12340000, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=0, z=1, v=0, c=1,
            memory_values=(),
            cpu_method=ins.addq,
            program=test_cpu.int_list_to_str(
                [0b01011010, 0b01000001]),  # ADDQ #5, D1
            method_args=(
                5, # value
                1, # op_size
                0, # ea_mode
                1, # ea_register
            ),
            method_kwargs={},
            cycle=4)

    def test_addq_001(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, 0x1234FFFB, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, 0x12350000, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.addq,
            program=test_cpu.int_list_to_str(
                [0b01011010, 0b01001001]),  # ADDQ #5, A1
            method_args=(
                5, # value
                1, # op_size
                1, # ea_mode
                1, # ea_register
            ),
            method_kwargs={},
            cycle=4)

    def test_addq_002(self):
        test_cpu.test_instruction(
            init_d=[None, 0x12340000, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[None, 0x12340008, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.addq,
            program=test_cpu.int_list_to_str(
                [0b01010000, 0b01000001]),  # ADDQ #8, D1
            method_args=(
                0, # value
                1, # op_size
                0, # ea_mode
                1, # ea_register
            ),
            method_kwargs={},
            cycle=4)


if __name__ == "__main__":
    unittest.main()
