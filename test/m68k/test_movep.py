# -*- coding: utf-8 -*-
"""
Test the MOVEP instruction of the 68k CPU.

Created on Tue Sep 26 13:38:49 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestMovep(unittest.TestCase):

    def test_movep_000(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, 0x11223344],
            init_a=[None, None, 0xFF6000, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF6030, 0xBBDD),
                (0xFF6032, 0xCCEE),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, 0x11223344],
            a=[None, None, 0xFF6000, None,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF6030, 0x33DD),
                (0xFF6032, 0x44EE),
            ),

            # Instruction
            cpu_method=ins.movep,
            program=test_cpu.int_list_to_str(
                [0b00001111, 0b10001010,
                 0x00, 0x30]),  # MOVEP.W D7, ($30, A2)
            method_args=(
                7,  # data_register
                2,  # address_register
                1,  # direction
                0,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_movep_001(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, 0x11223344],
            init_a=[None, None, 0xFF6000, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF6030, 0x7766),
                (0xFF6032, 0x55AA),
                (0xFF6034, 0xBBDD),
                (0xFF6036, 0xCCEE),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, 0x11223344],
            a=[None, None, 0xFF6000, None,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF6030, 0x1166),
                (0xFF6032, 0x22AA),
                (0xFF6034, 0x33DD),
                (0xFF6036, 0x44EE),
            ),

            # Instruction
            cpu_method=ins.movep,
            program=test_cpu.int_list_to_str(
                [0b00001111, 0b11001010,
                 0x00, 0x30]),  # MOVEP.L D7, ($30, A2)
            method_args=(
                7,  # data_register
                2,  # address_register
                1,  # direction
                1,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=24)

    def test_movep_002(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, 0x11225566],
            init_a=[None, None, 0xFF6000, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF6030, 0x33DD),
                (0xFF6032, 0x44EE),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, 0x11223344],
            a=[None, None, 0xFF6000, None,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF6030, 0x33DD),
                (0xFF6032, 0x44EE),
            ),

            # Instruction
            cpu_method=ins.movep,
            program=test_cpu.int_list_to_str(
                [0b00001111, 0b00001010,
                 0x00, 0x30]),  # MOVEP.W ($30, A2), D7
            method_args=(
                7,  # data_register
                2,  # address_register
                0,  # direction
                0,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=16)

    def test_movep_003(self):
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, 0x11223344],
            init_a=[None, None, 0xFF6000, None,
                    None, None, None, None],
            init_pc=0,
            init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
            init_t1=None, init_s=None, init_i=None,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF6030, 0x7766),
                (0xFF6032, 0x55AA),
                (0xFF6034, 0xBBDD),
                (0xFF6036, 0xCCEE),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, 0x7755BBCC],
            a=[None, None, 0xFF6000, None,
               None, None, None, None],
            pc=None,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=None, i=None,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF6030, 0x7766),
                (0xFF6032, 0x55AA),
                (0xFF6034, 0xBBDD),
                (0xFF6036, 0xCCEE),
            ),

            # Instruction
            cpu_method=ins.movep,
            program=test_cpu.int_list_to_str(
                [0b00001111, 0b01001010,
                 0x00, 0x30]),  # MOVEP.L ($30, A2), D7
            method_args=(
                7,  # data_register
                2,  # address_register
                0,  # direction
                1,  # op_size
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=24)


if __name__ == "__main__":
    unittest.main()
