# -*- coding: utf-8 -*-
"""
Test the CHK instruction of the 68k CPU.

Created on Sun Sep 24 11:28:34 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestChk(unittest.TestCase):

    def test_chk_000(self):
        program = [0xFF]*0x100
        # Example CHK Vector offset = 0x2030
        program[0x18] = 0
        program[0x19] = 0
        program[0x1A] = 0x20
        program[0x1B] = 0x30
        test_cpu.test_instruction(
            # Setup
            init_d=[10, 5, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0],
            init_pc=0x100,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=0, init_i=0,
            init_usp=0,
            init_ssp=0xFF100A,
            init_mem=(
                (0xFF100A, 0),
            ),

            # Expected state
            d=[10, 5, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0],
            pc=0x102,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=0, i=None,
            usp=0,
            ssp=0xFF100A,
            memory_values=(
                (0xFF1008, 0),
                (0xFF100A, 0),
                (0xFF100C, 0),
            ),

            # Instruction
            cpu_method=ins.chk,
            program=test_cpu.int_list_to_str(
                program + [0b01000011, 0b10000000]),  # CHK D0, D1
            method_args=(
                1,  # register_index
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=10)

    def test_chk_001(self):
        program = [0xFF]*0x100
        # Example CHK Vector offset = 0x2030
        program[0x18] = 0
        program[0x19] = 0
        program[0x1A] = 0x20
        program[0x1B] = 0x30
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 5, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0],
            init_pc=0x100,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=0, init_i=0,
            init_usp=0,
            init_ssp=0xFF100A,
            init_mem=(
                (0xFF100A, 0),
            ),

            # Expected state
            d=[None, 5, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0],
            pc=0x104,
            x=None, n=None, z=None, v=None, c=None,
            t1=None, s=0, i=None,
            usp=0,
            ssp=0xFF100A,
            memory_values=(
                (0xFF1008, 0),
                (0xFF100A, 0),
                (0xFF100C, 0),
            ),

            # Instruction
            cpu_method=ins.chk,
            program=test_cpu.int_list_to_str(
                program + [0b01000011, 0b10111100,
                           0, 5]),  # CHK #5, D1
            method_args=(
                1,  # register_index
                7,  # ea_mode
                4,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=14)

    def test_chk_002(self):
        program = [0xFF]*0x100
        # Example CHK Vector offset = 0x2030
        program[0x18] = 0
        program[0x19] = 0
        program[0x1A] = 0x20
        program[0x1B] = 0x30
        test_cpu.test_instruction(
            # Setup
            init_d=[10, 11, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0],
            init_pc=0x100,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=0, init_i=0,
            init_usp=0,
            init_ssp=0xFF100A,
            init_mem=(
                (0xFF100A, 0),
            ),

            # Expected state
            d=[10, 11, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFF1004],
            pc=0x2030,
            x=0, n=0, z=0, v=0, c=0,
            t1=0, s=1, i=0,
            usp=0,
            ssp=0xFF1004,
            memory_values=(
                (0xFF1002, 0),
                (0xFF1004, 0),
                (0xFF1006, 0),
                (0xFF1008, 0x102),
                (0xFF100A, 0),
                (0xFF100C, 0),
            ),

            # Instruction
            cpu_method=ins.chk,
            program=test_cpu.int_list_to_str(
                program + [0b01000011, 0b10000000]),  # CHK D0, D1
            method_args=(
                1,  # register_index
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=40)

    def test_chk_003(self):
        program = [0xFF]*0x100
        # Example CHK Vector offset = 0x2030
        program[0x18] = 0
        program[0x19] = 0
        program[0x1A] = 0x20
        program[0x1B] = 0x30
        test_cpu.test_instruction(
            # Setup
            init_d=[10, 0x1234FFFF, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0],
            init_pc=0x100,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=0, init_i=0,
            init_usp=0,
            init_ssp=0xFF100A,
            init_mem=(
                (0xFF100A, 0),
            ),

            # Expected state
            d=[10, 0x1234FFFF, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFF1004],
            pc=0x2030,
            usp=0,
            ssp=0xFF1004,
            x=0, n=1, z=0, v=0, c=0,
            t1=0, s=1, i=0,
            memory_values=(
                (0xFF1002, 0),
                (0xFF1004, 0b01000),
                (0xFF1006, 0),
                (0xFF1008, 0x102),
                (0xFF100A, 0),
                (0xFF100C, 0),
            ),

            # Instruction
            cpu_method=ins.chk,
            program=test_cpu.int_list_to_str(
                program + [0b01000011, 0b10000000]),  # CHK D0, D1
            method_args=(
                1,  # register_index
                0,  # ea_mode
                0,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=40)

    def test_chk_004(self):
        program = [0xFF]*0x100
        # Example CHK Vector offset = 0x2030
        program[0x18] = 0
        program[0x19] = 0
        program[0x1A] = 0x20
        program[0x1B] = 0x30
        test_cpu.test_instruction(
            # Setup
            init_d=[None, 0x107, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0],
            init_pc=0x100,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=0, init_i=0,
            init_usp=0,
            init_ssp=0xFF100A,
            init_mem=(
                (0xFF100A, 0),
            ),

            # Expected state
            d=[None, 0x107, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFF1004],
            pc=0x2030,
            x=0, n=0, z=0, v=0, c=0,
            t1=0, s=1, i=0,
            usp=0,
            ssp=0xFF1004,
            memory_values=(
                (0xFF1002, 0),
                (0xFF1004, 0),
                (0xFF1006, 0),
                (0xFF1008, 0x104),
                (0xFF100A, 0),
                (0xFF100C, 0),
            ),

            # Instruction
            cpu_method=ins.chk,
            program=test_cpu.int_list_to_str(
                program + [0b01000011, 0b10111100,
                           1, 6]),  # CHK #$106, D1
            method_args=(
                1,  # register_index
                7,  # ea_mode
                4,  # ea_register
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=44)


if __name__ == "__main__":
    unittest.main()
