# -*- coding: utf-8 -*-
"""
Test the ADD instruction of the 68k CPU.

Created on Sun Sep 17 14:01:53 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestAdd(unittest.TestCase):

    def test_add_000(self):
        test_cpu.test_instruction(
            init_d=None,
            init_a=None,
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0]*8,
            a=None,
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            memory_values=(),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010000, 0b01000001]),  # ADD D0, D1
            method_args=(0, 0, 1, 0, 1),
            method_kwargs={},
            cycle=4)

    def test_add_001(self):
        test_cpu.test_instruction(
            init_d=[1, 1, None, None, None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[2, 1, None, None, None, None, None, None],
            a=None,
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010000, 0b01000001]),  # ADD D0, D1
            method_args=(0, 0, 1, 0, 1),
            method_kwargs={},
            cycle=4)

    def test_add_002(self):
        test_cpu.test_instruction(
            init_d=[0x7FFFFFFF, 1, None, None, None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x80000000, 1, None, None, None, None, None, None],
            a=None,
            pc=None,
            x=0, n=1, z=0, v=1, c=0,
            memory_values=(),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010000, 0b10000001]),  # ADD.L D0, D1
            method_args=(
                0,  # register_index
                0,  # op_type
                2,  # op_size
                0,  # ea_mode
                1),  # ea_register
            method_kwargs={},
            cycle=8)

    def test_add_003(self):
        test_cpu.test_instruction(
            init_d=[0x12345678, 0xFFFFFF01, None, None,
                    None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x12345679, 0xFFFFFF01, None, None, None, None, None, None],
            a=None,
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010000, 0b00000001]),  # ADD.B D0, D1
            method_args=(
                0,  # register_index
                0,  # op_type
                0,  # op_size
                0,  # ea_mode
                1),  # ea_register
            method_kwargs={},
            cycle=4)

    def test_add_004(self):
        test_cpu.test_instruction(
            init_d=[0x12345678, 0xFFFF1111, None, None,
                    None, None, None, None],
            init_a=None,
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x12346789, 0xFFFF1111, None, None, None, None, None, None],
            a=None,
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010000, 0b01000001]),  # ADD D0, D1
            method_args=(
                0,  # register_index
                0,  # op_type
                1,  # op_size
                0,  # ea_mode
                1),  # ea_register
            method_kwargs={},
            cycle=4)

    def test_add_005(self):
        test_cpu.test_instruction(
            init_d=[0x12345678, None, None, None,
                    None, None, None, None],
            init_a=[0x12345678, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x2468ACF0, None, None, None, None, None, None, None],
            a=[0x12345678, None, None, None, None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010000, 0b10001000]),  # ADD.L D0, A0
            method_args=(
                0,  # register_index
                0,  # op_type
                2,  # op_size
                1,  # ea_mode
                0),  # ea_register
            method_kwargs={},
            cycle=8)

    def test_add_006(self):
        test_cpu.test_instruction(
            init_d=[None, None, None, 0xFFFFFFFF,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFFFF0001],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[None, None, None, 0xFFFF0000, None, None, None, None],
            a=[None, None, None, None, None, None, None, 0xFFFF0001],
            pc=None,
            x=1, n=0, z=1, v=0, c=1,
            memory_values=(),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010110, 0b01001111]),  # ADD D3, A7
            method_args=(
                3,  # register_index
                0,  # op_type
                1,  # op_size
                1,  # ea_mode
                7),  # ea_register
            method_kwargs={},
            cycle=4)

    def test_add_007(self):
        test_cpu.test_instruction(
            init_d=[None, None, 0x8000, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, 0xFF1234, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF1234, 6),
            ),
            d=[None, None, 0x8006, None, None, None, None, None],
            a=[None, None, None, None, None, 0xFF1234, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(
                (0xFF1232, 0),
                (0xFF1234, 6),
                (0xFF1236, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010100, 0b01010101]),  # ADD D2, (A5)
            method_args=(
                2,  # register_index
                0,  # op_type
                1,  # op_size
                2,  # ea_mode
                5),  # ea_register
            method_kwargs={},
            cycle=8)

    def test_add_008(self):
        test_cpu.test_instruction(
            init_d=[None, None, 0x8000, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, 0xFF1234, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF1234, 6),
            ),
            d=[None, None, 0x8000, None, None, None, None, None],
            a=[None, None, None, None, None, 0xFF1234, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(
                (0xFF1232, 0),
                (0xFF1234, 0x8006),
                (0xFF1236, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010101, 0b01010101]),  # ADD (A5), D2
            method_args=(
                2,  # register_index
                1,  # op_type
                1,  # op_size
                2,  # ea_mode
                5),  # ea_register
            method_kwargs={},
            cycle=12)

    def test_add_009(self):
        test_cpu.test_instruction(
            init_d=[None, None, 0x8000, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, 0xFF1234, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF1234, 6),
            ),
            d=[None, None, 0x8000, None, None, None, None, None],
            a=[None, None, None, None, None, 0xFF1236, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(
                (0xFF1232, 0),
                (0xFF1234, 0x8006),
                (0xFF1236, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010101, 0b01011101]),  # ADD (A5)+, D2
            method_args=(
                2,  # register_index
                1,  # op_type
                1,  # op_size
                3,  # ea_mode
                5),  # ea_register
            method_kwargs={},
            cycle=12)

    def test_add_010(self):
        test_cpu.test_instruction(
            init_d=[None, None, 0x8000, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, 0xFF1234, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF1234, 6),
                (0xFF1236, 1),
            ),
            d=[None, None, 0x68001, None, None, None, None, None],
            a=[None, None, None, None, None, 0xFF1238, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(
                (0xFF1232, 0),
                (0xFF1234, 6),
                (0xFF1236, 1),
                (0xFF1238, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010100, 0b10011101]),  # ADD.L D2, (A5)+
            method_args=(
                2,  # register_index
                0,  # op_type
                2,  # op_size
                3,  # ea_mode
                5),  # ea_register
            method_kwargs={},
            cycle=14)

    def test_add_011(self):
        test_cpu.test_instruction(
            init_d=[None, None, 0x8000, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, 0xFF1234, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF1232, 7),
                (0xFF1234, 8),
                (0xFF1236, 9),
            ),
            d=[None, None, 0x8007, None, None, None, None, None],
            a=[None, None, None, None, None, 0xFF1232, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(
                (0xFF1230, 0),
                (0xFF1232, 7),
                (0xFF1234, 8),
                (0xFF1236, 9),
                (0xFF1238, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010100, 0b01100101]),  # ADD D2, -(A5)
            method_args=(
                2,  # register_index
                0,  # op_type
                1,  # op_size
                4,  # ea_mode
                5),  # ea_register
            method_kwargs={},
            cycle=10)

    def test_add_012(self):
        test_cpu.test_instruction(
            init_d=[None, None, 0x90008000, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, 0xFF1234, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF122C, 4),
                (0xFF122E, 5),
                (0xFF1230, 6),
                (0xFF1232, 7),
                (0xFF1234, 8),
                (0xFF1236, 9),
            ),
            d=[None, None, 0x90008000, None, None, None, None, None],
            a=[None, None, None, None, None, 0xFF1230, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(
                (0xFF122A, 0),
                (0xFF122C, 4),
                (0xFF122E, 5),
                (0xFF1230, 0x9006),
                (0xFF1232, 0x8007),
                (0xFF1234, 8),
                (0xFF1236, 9),
                (0xFF1238, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010101, 0b10100101]),  # ADD -(A5), D2
            method_args=(
                2,  # register_index
                1,  # op_type
                2,  # op_size
                4,  # ea_mode
                5),  # ea_register
            method_kwargs={},
            cycle=22)

    def test_add_013(self):
        test_cpu.test_instruction(
            init_d=[None, None, 0x90008000, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, 0xFF1234, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF1234, 8),
                (0xFF2234, 9),
            ),
            d=[None, None, 0x90008000, None, None, None, None, None],
            a=[None, None, None, None, None, 0xFF1234, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(
                (0xFF1232, 0),
                (0xFF1234, 8),
                (0xFF1236, 0),
                (0xFF2232, 0),
                (0xFF2234, 0x8009),
                (0xFF2236, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010101, 0b01101101,
                 0b00010000, 0b00000000]),  # ADD ($1000, A5), D2
            method_args=(
                2,  # register_index
                1,  # op_type
                1,  # op_size
                5,  # ea_mode
                5),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_add_014(self):
        test_cpu.test_instruction(
            init_d=[None, None, 0x90008000, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, 0xFF1234, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF1234, 8),
                (0xFF2234, 9),
            ),
            d=[None, None, 0x90008009, None, None, None, None, None],
            a=[None, None, None, None, None, 0xFF1234, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(
                (0xFF1232, 0),
                (0xFF1234, 8),
                (0xFF1236, 0),
                (0xFF2232, 0),
                (0xFF2234, 9),
                (0xFF2236, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010100, 0b01101101,
                 0b00010000, 0b00000000]),  # ADD D2, ($1000, A5)
            method_args=(
                2,  # register_index
                0,  # op_type
                1,  # op_size
                5,  # ea_mode
                5),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_add_015(self):
        test_cpu.test_instruction(
            init_d=[None, None, 0x90008000, None,
                    None, None, 0x0000FFFF, None],
            init_a=[None, None, None, None,
                    None, 0xFF1234, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF1232, 0x607),
                (0xFF1234, 8),
                (0xFF1333, 9),
            ),
            d=[None, None, 0x90008607, None, None, None, 0xFFFF, None],
            a=[None, None, None, None, None, 0xFF1234, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(
                (0xFF1230, 0),
                (0xFF1232, 0x607),
                (0xFF1234, 8),
                (0xFF1236, 0),
                (0xFF1331, 0),
                (0xFF1333, 9),
                (0xFF1335, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010100, 0b01110101,
                 0b01100000, 0b11111111]),  # ADD D2, ($FF, A5, D6)
            method_args=(
                2,  # register_index
                0,  # op_type
                1,  # op_size
                6,  # ea_mode
                5),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=14)

    def test_add_016(self):
        test_cpu.test_instruction(
            init_d=[None, None, 0x90008000, None,
                    None, None, 0x0000FFFF, None],
            init_a=[None, None, None, None,
                    None, 0xFF1234, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF1232, 0x607),
                (0xFF1234, 8),
                (0xFF1333, 9),
            ),
            d=[None, None, 0x90008000, None, None, None, 0xFFFF, None],
            a=[None, None, None, None, None, 0xFF1234, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(
                (0xFF1230, 0),
                (0xFF1232, 0x9607),
                (0xFF1234, 0x8008),
                (0xFF1236, 0),
                (0xFF1331, 0),
                (0xFF1333, 9),
                (0xFF1335, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010101, 0b10110101,
                 0b01100000, 0b11111111]),  # ADD ($FF, A5, D6), D2
            method_args=(
                2,  # register_index
                1,  # op_type
                2,  # op_size
                6,  # ea_mode
                5),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=26)

    def test_add_017(self):
        test_cpu.test_instruction(
            init_d=[None, None, 0x90008020, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, 0xFF1234, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF1232, 0x306),
                (0xFF1234, 8),
            ),
            d=[None, None, 0x90008020, None, None, None, None, None],
            a=[None, None, None, None, None, 0xFF1234, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            memory_values=(
                (0xFF1230, 0),
                (0xFF1232, 0x2306),
                (0xFF1234, 8),
                (0xFF1236, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010101, 0b00101101,
                 0b11111111, 0b11111110]),  # ADD ($FFFE, A5), D2
            method_args=(
                2,  # register_index
                1,  # op_type
                0,  # op_size
                5,  # ea_mode
                5),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_add_018(self):
        test_cpu.test_instruction(
            init_d=[0x80009000, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF8000, 0x8123),
            ),
            d=[0x80001123, None, None, None, None, None, None, None],
            a=[None, None, None, None, None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=1, c=1,
            memory_values=(
                (0xFF7FFE, 0),
                (0xFF8000, 0x8123),
                (0xFF8002, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010000, 0b01111000,
                 0b10000000, 0b00000000]),  # ADD D0, ($8000).W
            method_args=(
                0,  # register_index
                0,  # op_type
                1,  # op_size
                7,  # ea_mode
                0),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_add_019(self):
        test_cpu.test_instruction(
            init_d=[0x80009000, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF8000, 0x8123),
            ),
            d=[0x80009000, None, None, None, None, None, None, None],
            a=[None, None, None, None, None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=1, c=1,
            memory_values=(
                (0xFF7FFE, 0),
                (0xFF8000, 0x1123),
                (0xFF8002, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010001, 0b01111000,
                 0b10000000, 0b00000000]),  # ADD ($8000).W, D0
            method_args=(
                0,  # register_index
                1,  # op_type
                1,  # op_size
                7,  # ea_mode
                0),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_add_020(self):
        test_cpu.test_instruction(
            init_d=[0x80009000, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF5678, 0x8123),
            ),
            d=[0x80001123, None, None, None, None, None, None, None],
            a=[None, None, None, None, None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=1, c=1,
            memory_values=(
                (0xFF5676, 0),
                (0xFF5678, 0x8123),
                (0xFF567A, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010000, 0b01111001,
                 0x00, 0xFF, 0x56, 0x78]),  # ADD D0, ($FF5678).L
            method_args=(
                0,  # register_index
                0,  # op_type
                1,  # op_size
                7,  # ea_mode
                1),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_add_021(self):
        test_cpu.test_instruction(
            init_d=[0x80009000, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(
                (0xFF5678, 0x8123),
            ),
            d=[0x80009000, None, None, None, None, None, None, None],
            a=[None, None, None, None, None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=1, c=1,
            memory_values=(
                (0xFF5676, 0),
                (0xFF5678, 0x1123),
                (0xFF567A, 0),
            ),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010001, 0b01111001,
                 0x00, 0xFF, 0x56, 0x78]),  # ADD D0, ($FF5678).L
            method_args=(
                0,  # register_index
                1,  # op_type
                1,  # op_size
                7,  # ea_mode
                1),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_add_022(self):
        test_cpu.test_instruction(
            init_d=[0x80000100, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x8000D17A, None, None, None, None, None, None, None],
            a=[None, None, None, None, None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010000, 0b01111010,
                 0b11111111, 0b11111110,]),  # ADD D0, ($FFFE, PC)
            method_args=(
                0,  # register_index
                0,  # op_type
                1,  # op_size
                7,  # ea_mode
                2),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_add_023(self):
        test_cpu.test_instruction(
            init_d=[0x80000100, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFFFFFFFF],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[0x8000D17B, None, None, None, None, None, None, None],
            a=[None, None, None, None, None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010000, 0b01111011,
                 0b11111000, 0b11111111,]),  # ADD D0, ($FF, PC, A7)
            method_args=(
                0,  # register_index
                0,  # op_type
                1,  # op_size
                7,  # ea_mode
                3),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=14)

    def test_add_024(self):
        test_cpu.test_instruction(
            init_d=[None, 0x80008080, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[None, 0x80008000, None, None, None, None, None, None],
            a=[None, None, None, None, None, None, None, None],
            pc=None,
            x=1, n=0, z=1, v=1, c=1,
            memory_values=(),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010010, 0b00111100,
                 0b00000000, 0b10000000,]),  # ADD D1, #$80
            method_args=(
                1,  # register_index
                0,  # op_type
                0,  # op_size
                7,  # ea_mode
                4),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_add_025(self):
        test_cpu.test_instruction(
            init_d=[None, 0x80008080, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[None, 0x800092B4, None, None, None, None, None, None],
            a=[None, None, None, None, None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=0,
            memory_values=(),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010010, 0b01111100,
                 0b00010010, 0b00110100,]),  # ADD D1, #$1234
            method_args=(
                1,  # register_index
                0,  # op_type
                1,  # op_size
                7,  # ea_mode
                4),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=8)

    def test_add_026(self):
        test_cpu.test_instruction(
            init_d=[None, 0x80008080, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_mem=(),
            d=[None, 0x2BCD92B4, None, None, None, None, None, None],
            a=[None, None, None, None, None, None, None, None],
            pc=None,
            x=1, n=0, z=0, v=1, c=1,
            memory_values=(),
            cpu_method=ins.add,
            program=test_cpu.int_list_to_str(
                [0b11010010, 0b10111100,
                 0xAB, 0xCD, 0x12, 0x34]),  # ADD D1, #$ABCD1234
            method_args=(
                1,  # register_index
                0,  # op_type
                2,  # op_size
                7,  # ea_mode
                4),  # ea_register
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    # TODO add negative tests for illegal instructions


if __name__ == "__main__":
    unittest.main()
