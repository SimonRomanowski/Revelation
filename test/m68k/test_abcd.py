# -*- coding: utf-8 -*-
"""
Test the ABCD instruction of the 68k CPU.

Created on Thu Sep 21 11:05:50 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestAbcd(unittest.TestCase):

    def test_abcd_000(self):
        test_cpu.test_instruction(
            init_d=[0x12, 0x22, None, None,
                    None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x34, 0x22, None, None,
               None, None, None, None],
            a=None,
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.abcd,
            program=test_cpu.int_list_to_str(
                [0b11000001, 0b00000001]),  # ABCD D1, D0
            method_args=(
                1,  # register_src
                0,  # register_dst
                0,  # op_type
            ),
            method_kwargs={},
            cycle=6)

    def test_abcd_001(self):
        test_cpu.test_instruction(
            init_d=[0x11, 0x22, None, None,
                    None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x34, 0x22, None, None,
               None, None, None, None],
            a=None,
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.abcd,
            program=test_cpu.int_list_to_str(
                [0b11000001, 0b00000001]),  # ABCD D1, D0
            method_args=(
                1,  # register_src
                0,  # register_dst
                0,  # op_type
            ),
            method_kwargs={},
            cycle=6)

    def test_abcd_002(self):
        test_cpu.test_instruction(
            init_d=[0x0F, 0x0, None, None,
                    None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=0, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x15, 0x0, None, None,
               None, None, None, None],
            a=None,
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.abcd,
            program=test_cpu.int_list_to_str(
                [0b11000001, 0b00000001]),  # ABCD D1, D0
            method_args=(
                1,  # register_src
                0,  # register_dst
                0,  # op_type
            ),
            method_kwargs={},
            cycle=6)

    def test_abcd_003(self):
        test_cpu.test_instruction(
            init_d=[0x0F, 0x0F, None, None,
                    None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=0, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x30, 0x0F, None, None,
               None, None, None, None],
            a=None,
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.abcd,
            program=test_cpu.int_list_to_str(
                [0b11000001, 0b00000001]),  # ABCD D1, D0
            method_args=(
                1,  # register_src
                0,  # register_dst
                0,  # op_type
            ),
            method_kwargs={},
            cycle=6)

    def test_abcd_004(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[0xFF4446, 0xFF1116, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF1114, 0x2270),
                (0xFF4444, 0x3313),
            ),
            d=[0]*8,
            a=[0xFF4445, 0xFF1115, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(
                (0xFF1112, 0),
                (0xFF1114, 0x2270),
                (0xFF1116, 0),
                (0xFF4442, 0),
                (0xFF4444, 0x3383),
                (0xFF4446, 0),
            ),
            cpu_method=ins.abcd,
            program=test_cpu.int_list_to_str(
                [0b11000001, 0b00001001]),  # ABCD -(A1), -(A0)
            method_args=(
                1,  # register_src
                0,  # register_dst
                1,  # op_type
            ),
            method_kwargs={},
            cycle=18)

    def test_abcd_005(self):
        test_cpu.test_instruction(
            init_d=[0x1234560F, 0x1234560F, None, None,
                    None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=1, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x12345631, 0x1234560F, None, None,
               None, None, None, None],
            a=None,
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.abcd,
            program=test_cpu.int_list_to_str(
                [0b11000001, 0b00000001]),  # ABCD D1, D0
            method_args=(
                1,  # register_src
                0,  # register_dst
                0,  # op_type
            ),
            method_kwargs={},
            cycle=6)

    def test_abcd_006(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[0xFF4445, 0xFF1115, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF1114, 0x2245),
                (0xFF4444, 0x337D),
            ),
            d=[0]*8,
            a=[0xFF4444, 0xFF1114, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(
                (0xFF1112, 0),
                (0xFF1114, 0x2245),
                (0xFF1116, 0),
                (0xFF4442, 0),
                (0xFF4444, 0x557D),
                (0xFF4446, 0),
            ),
            cpu_method=ins.abcd,
            program=test_cpu.int_list_to_str(
                [0b11000001, 0b00001001]),  # ABCD -(A1), -(A0)
            method_args=(
                1,  # register_src
                0,  # register_dst
                1,  # op_type
            ),
            method_kwargs={},
            cycle=18)


if __name__ == "__main__":
    unittest.main()
