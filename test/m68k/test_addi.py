# -*- coding: utf-8 -*-
"""
Test the ADDI instruction of the 68k CPU.

Created on Thu Sep 21 11:05:50 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestAddi(unittest.TestCase):

    def test_addi_000(self):
        test_cpu.test_instruction(
            init_d=[0, None, None, None,
                    None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x11223344, None, None, None,
               None, None, None, None],
            a=None,
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.addi,
            program=test_cpu.int_list_to_str(
                [0b00000110, 0b10000000,
                 0x11, 0x22, 0x33, 0x44]),  # ADDI #$11223344, D0
            method_args=(
                2,  # op_size
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_addi_001(self):
        test_cpu.test_instruction(
            init_d=[0, None, None, None,
                    None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x22, None, None, None,
               None, None, None, None],
            a=None,
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.addi,
            program=test_cpu.int_list_to_str(
                [0b00000110, 0b00000000,
                 0x11, 0x22]),  # ADDI #$22, D0
            method_args=(
                0,  # op_size
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_addi_002(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFFFF032, 0x7FFF),
            ),
            d=[None, None, None, None,
               None, None, None, None],
            a=None,
            pc=None,
            x=0, n=1, z=0, v=1, c=0,
            memory_values=(
                (0xFFFF030, 0),
                (0xFFFF032, 0x8003),
                (0xFFFF034, 0),
            ),
            cpu_method=ins.addi,
            program=test_cpu.int_list_to_str(
                [0b00000110, 0b01111000,
                 0, 4,
                 0xF0, 0x32]),  # ADDI #$4, ($F032)
            method_args=(
                1,  # op_size
                7,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20)


if __name__ == "__main__":
    unittest.main()
