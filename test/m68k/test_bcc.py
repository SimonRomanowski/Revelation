# -*- coding: utf-8 -*-
"""
Test the ASd instruction of the 68k CPU.

Created on Fri Sep 22 17:10:02 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestBcc(unittest.TestCase):

    def test_bcc_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=0, init_v=None, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=None, z=0, v=None, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100010, 10]),  # BHI <+10>
            method_args=(
                2,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=0, init_v=None, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=None, z=0, v=None, c=1,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100010, 10]),  # BHI <+10>
            method_args=(
                2,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=2,
            init_x=None, init_n=None, init_z=0, init_v=None, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=0,
            x=None, n=None, z=0, v=None, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0xFF, 0xFF,
                 0b01100010, 0xFC]),  # BHI <-4>
            method_args=(
                2,  # condition
                0xFFFC,  # offset
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=10)

    def test_bcc_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=0, init_v=None, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=0x1236,
            x=None, n=None, z=0, v=None, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100010, 0,
                 0x12, 0x34]),  # BHI <+$1234>
            method_args=(
                2,  # condition
                0,  # offset
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=10)

    def test_bcc_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=1, init_v=None, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=4,
            x=None, n=None, z=1, v=None, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100010, 0,
                 0x12, 0x34]),  # BHI <+$31234>
            method_args=(
                2,  # condition
                0,  # offset
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_bcc_005(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=1, init_v=None, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=None, z=1, v=None, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100011, 10]),  # BLS <+10>
            method_args=(
                3,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_006(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=0, init_v=None, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=None, z=0, v=None, c=1,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100011, 10]),  # BLS <+10>
            method_args=(
                3,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_007(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=0, init_v=None, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=None, z=0, v=None, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100011, 10]),  # BLS <+10>
            method_args=(
                3,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_008(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=None, z=None, v=None, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100100, 10]),  # BCC <+10>
            method_args=(
                4,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_009(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=None, z=None, v=None, c=1,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100100, 10]),  # BCC <+10>
            method_args=(
                4,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_010(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=1,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=None, z=None, v=None, c=1,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100101, 10]),  # BCS <+10>
            method_args=(
                5,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_011(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=None, z=None, v=None, c=0,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100101, 10]),  # BCS <+10>
            method_args=(
                5,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_012(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=0, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=None, z=0, v=None, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100110, 10]),  # BNE <+10>
            method_args=(
                6,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_013(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=1, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=None, z=1, v=None, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100110, 10]),  # BNE <+10>
            method_args=(
                6,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_014(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=1, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=None, z=1, v=None, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100111, 10]),  # BEQ <+10>
            method_args=(
                7,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_015(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=0, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=None, z=0, v=None, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01100111, 10]),  # BEQ <+10>
            method_args=(
                7,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_016(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=None, z=None, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101000, 10]),  # BVC <+10>
            method_args=(
                8,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_017(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=None, z=None, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101000, 10]),  # BVC <+10>
            method_args=(
                8,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_018(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=None, z=None, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101001, 10]),  # BVS <+10>
            method_args=(
                9,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_019(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=None, z=None, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101001, 10]),  # BVS <+10>
            method_args=(
                9,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_020(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=0, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101010, 10]),  # BPL <+10>
            method_args=(
                10,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_021(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=1, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101010, 10]),  # BPL <+10>
            method_args=(
                10,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_022(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=1, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101011, 10]),  # BMI <+10>
            method_args=(
                11,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_023(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=0, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101011, 10]),  # BMI <+10>
            method_args=(
                11,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_024(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=None, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=0, z=None, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101100, 10]),  # BGE <+10>
            method_args=(
                12,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_025(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=1, z=None, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101100, 10]),  # BGE <+10>
            method_args=(
                12,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_026(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=0, z=None, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101100, 10]),  # BGE <+10>
            method_args=(
                12,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_027(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=None, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=1, z=None, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101100, 10]),  # BGE <+10>
            method_args=(
                12,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_028(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=0, z=None, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101101, 10]),  # BLT <+10>
            method_args=(
                13,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_029(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=None, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=1, z=None, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101101, 10]),  # BLT <+10>
            method_args=(
                13,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_030(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=None, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=0, z=None, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101101, 10]),  # BLT <+10>
            method_args=(
                13,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_031(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=None, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=1, z=None, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101101, 10]),  # BLT <+10>
            method_args=(
                13,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_032(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=0, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=0, z=0, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101110, 10]),  # BGT <+10>
            method_args=(
                14,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_033(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=0, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=0, z=0, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101110, 10]),  # BGT <+10>
            method_args=(
                14,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_034(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=1, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=0, z=1, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101110, 10]),  # BGT <+10>
            method_args=(
                14,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_035(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=1, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=0, z=1, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101110, 10]),  # BGT <+10>
            method_args=(
                14,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_036(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=0, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=1, z=0, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101110, 10]),  # BGT <+10>
            method_args=(
                14,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_037(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=0, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=1, z=0, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101110, 10]),  # BGT <+10>
            method_args=(
                14,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_038(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=1, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=1, z=1, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101110, 10]),  # BGT <+10>
            method_args=(
                14,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_039(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=1, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=1, z=1, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101110, 10]),  # BGT <+10>
            method_args=(
                14,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_040(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=0, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=0, z=0, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101111, 10]),  # BLE <+10>
            method_args=(
                15,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_041(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=0, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=0, z=0, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101111, 10]),  # BLE <+10>
            method_args=(
                15,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_042(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=1, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=0, z=1, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101111, 10]),  # BLE <+10>
            method_args=(
                15,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_043(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=0, init_z=1, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=0, z=1, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101111, 10]),  # BLE <+10>
            method_args=(
                15,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_044(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=0, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=1, z=0, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101111, 10]),  # BLE <+10>
            method_args=(
                15,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_045(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=0, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=2,
            x=None, n=1, z=0, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101111, 10]),  # BLE <+10>
            method_args=(
                15,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=8)

    def test_bcc_046(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=1, init_v=0, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=1, z=1, v=0, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101111, 10]),  # BLE <+10>
            method_args=(
                15,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)

    def test_bcc_047(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=1, init_z=1, init_v=1, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=12,
            x=None, n=1, z=1, v=1, c=None,
            t1=None, s=None, i=None,
            memory_values=(),

            # Instruction
            cpu_method=ins.bcc,
            program=test_cpu.int_list_to_str(
                [0b01101111, 10]),  # BLE <+10>
            method_args=(
                15,  # condition
                10,  # offset
            ),
            method_kwargs={},
            method_load_program=False,
            cycle=10)


if __name__ == "__main__":
    unittest.main()
