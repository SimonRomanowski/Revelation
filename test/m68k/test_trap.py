# -*- coding: utf-8 -*-
"""
Test the TRAP instruction of the 68k CPU.

Created on Thu Sep 28 12:01:53 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestTrap(unittest.TestCase):

    def test_trap_000(self):
        # TRAP vectors start at address 128 = 0x80
        program = [0xFF] * 0x80 \
            + [0, 0x3, 0x45, 0x68]
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFF3008],
            init_pc=0x84,
            init_x=1, init_n=1, init_z=0, init_v=1, init_c=1,
            init_t1=0, init_s=0, init_i=5,
            init_usp=None,
            init_ssp=0xFF2008,
            init_mem=(
                (0xFF2008, 0x1234),
                (0xFF3008, 0xABCD),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFF2002],
            pc=0x34568,
            x=1, n=1, z=0, v=1, c=1,
            t1=0, s=1, i=5,
            usp=0xFF3008,
            ssp=None,
            memory_values=(
                (0xFF2002, 0x051B),
                (0xFF2004, 0),
                (0xFF2006, 0x86),
                (0xFF2008, 0x1234),
                (0xFF3008, 0xABCD),
            ),

            # Instruction
            cpu_method=ins.trap,
            program=test_cpu.int_list_to_str(
                program + [0b01001110, 0b01000000]),  # TRAP 0
            method_args=(
                0,  # vector_number
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=34)

    def test_trap_001(self):
        # TRAP vectors start at address 32 = 0x20
        program = [0xFF] * 0x80 \
            + [0, 0x3, 0x45, 0x68] \
            + [0, 0x3, 0x48, 0x68]
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFF3008],
            init_pc=0x88,
            init_x=1, init_n=1, init_z=0, init_v=1, init_c=1,
            init_t1=0, init_s=0, init_i=5,
            init_usp=None,
            init_ssp=0xFF2008,
            init_mem=(
                (0xFF2008, 0x1234),
                (0xFF3008, 0xABCD),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFF2002],
            pc=0x34868,
            x=1, n=1, z=0, v=1, c=1,
            t1=0, s=1, i=5,
            usp=0xFF3008,
            ssp=None,
            memory_values=(
                (0xFF2002, 0x051B),
                (0xFF2004, 0),
                (0xFF2006, 0x8A),
                (0xFF2008, 0x1234),
                (0xFF3008, 0xABCD),
            ),

            # Instruction
            cpu_method=ins.trap,
            program=test_cpu.int_list_to_str(
                program + [0b01001110, 0b01000001]),  # TRAP 1
            method_args=(
                1,  # vector_number
            ),
            method_kwargs={},
            method_load_program=True,
            cycle=34)


if __name__ == "__main__":
    unittest.main()
