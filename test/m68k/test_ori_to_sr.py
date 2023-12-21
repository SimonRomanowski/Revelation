# -*- coding: utf-8 -*-
"""
Test the ORI to SR instruction of the 68k CPU.

Created on Tue Sep 26 22:26:16 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestOriToSr(unittest.TestCase):

    def test_ori_to_sr_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=1, init_i=0,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=1, n=1, z=1, v=1, c=1,
            t1=1, s=1, i=7,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.ori_to_sr,
            program=test_cpu.int_list_to_str(
                [0b00000000, 0b01111100,
                 0xFF, 0xFF]),  # OR #$FFFF, SR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_ori_to_sr_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=1, init_i=0,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=0, v=0, c=0,
            t1=0, s=1, i=0,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.ori_to_sr,
            program=test_cpu.int_list_to_str(
                [0b00000000, 0b01111100,
                 0, 0]),  # OR #$0, SR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)

    def test_ori_to_sr_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, None],
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=1, init_i=0,
            init_usp=None,
            init_ssp=None,
            init_mem=(),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, None],
            pc=None,
            x=0, n=0, z=1, v=0, c=1,
            t1=1, s=1, i=2,
            usp=None,
            ssp=None,
            memory_values=(),
            # Instruction
            cpu_method=ins.ori_to_sr,
            program=test_cpu.int_list_to_str(
                [0b00000000, 0b01111100,
                 0x82, 0x05]),  # OR #$8205, SR
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=20)


if __name__ == "__main__":
    unittest.main()
