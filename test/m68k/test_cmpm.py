# -*- coding: utf-8 -*-
"""
Test the CMP instruction of the 68k CPU.

Created on Sun Sep 24 17:37:29 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestCmpm(unittest.TestCase):

    def test_cmpm_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[0xFF1234, 0xFF2234, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 1),
                (0xFF2234, 2),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[0xFF1236, 0xFF2236, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=0, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1234, 1),
                (0xFF2234, 2),
            ),

            # Instruction
            cpu_method=ins.cmpm,
            program=test_cpu.int_list_to_str(
                [0b10110001, 0b01001001]),  # CMPM (A1)+, (A0)+
            method_args=(
                0,  # register_dst
                1,  # register_src
                1,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_cmpm_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[0xFF1234, 0xFF2234, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 2),
                (0xFF2234, 1),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[0xFF1236, 0xFF2236, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1234, 2),
                (0xFF2234, 1),
            ),

            # Instruction
            cpu_method=ins.cmpm,
            program=test_cpu.int_list_to_str(
                [0b10110001, 0b01001001]),  # CMPM (A1)+, (A0)+
            method_args=(
                0,  # register_dst
                1,  # register_src
                1,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_cmpm_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[0xFF1234, 0xFF2234, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 2),
                (0xFF2234, 2),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[0xFF1236, 0xFF2236, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1234, 2),
                (0xFF2234, 2),
            ),

            # Instruction
            cpu_method=ins.cmpm,
            program=test_cpu.int_list_to_str(
                [0b10110001, 0b01001001]),  # CMPM (A1)+, (A0)+
            method_args=(
                0,  # register_dst
                1,  # register_src
                1,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_cmpm_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[0xFF1234, 0xFF2234, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 0x7F00),
                (0xFF2234, 0xFF00),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[0xFF1235, 0xFF2235, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=1, z=0, v=1, c=1,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1234, 0x7F00),
                (0xFF2234, 0xFF00),
            ),

            # Instruction
            cpu_method=ins.cmpm,
            program=test_cpu.int_list_to_str(
                [0b10110001, 0b00001001]),  # CMPM.B (A1)+, (A0)+
            method_args=(
                0,  # register_dst
                1,  # register_src
                0,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=12)

    def test_cmpm_004(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[0xFF1234, 0xFF2234, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF1234, 0x8000),
                (0xFF1236, 0),
                (0xFF2234, 0),
                (0xFF2236, 1),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[0xFF1238, 0xFF2238, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=1, c=0,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF1234, 0x8000),
                (0xFF1236, 0),
                (0xFF2234, 0),
                (0xFF2236, 1),
            ),

            # Instruction
            cpu_method=ins.cmpm,
            program=test_cpu.int_list_to_str(
                [0b10110001, 0b10001001]),  # CMPM.L (A1)+, (A0)+
            method_args=(
                0,  # register_dst
                1,  # register_src
                2,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=20)


if __name__ == "__main__":
    unittest.main()
