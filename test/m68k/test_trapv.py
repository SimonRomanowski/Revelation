# -*- coding: utf-8 -*-
"""
Test the TRAPV instruction of the 68k CPU.

Created on Thu Sep 28 13:06:26 2023

@author: Simon Romanowski
"""

import unittest

from test.m68k import test_cpu
import m68k.instructions as ins


class TestTrapv(unittest.TestCase):

    def test_trapv_000(self):
        # TRAPV vector is at 0x1C
        program = [0xFF] * 0x1C \
            + [0, 0x3, 0x45, 0x68]
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFF3008],
            init_pc=0x20,
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
                (0xFF2006, 0x22),
                (0xFF2008, 0x1234),
                (0xFF3008, 0xABCD),
            ),

            # Instruction
            cpu_method=ins.trapv,
            program=test_cpu.int_list_to_str(
                program + [0b01001110, 0b01110110]),  # TRAPV
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=34)

    def test_trapv_001(self):
        # TRAPV vector is at 0x1C
        program = [0xFF] * 0x1C \
            + [0, 0x3, 0x45, 0x68]
        test_cpu.test_instruction(
            # Setup
            init_d=[None, None, None, None,
                    None, None, None, None],
            init_a=[None, None, None, None,
                    None, None, None, 0xFF3008],
            init_pc=0x20,
            init_x=1, init_n=1, init_z=0, init_v=0, init_c=1,
            init_t1=0, init_s=0, init_i=5,
            init_usp=None,
            init_ssp=None,
            init_mem=(
                (0xFF2008, 0x1234),
                (0xFF3008, 0xABCD),
            ),

            # Expected state
            d=[None, None, None, None,
               None, None, None, None],
            a=[None, None, None, None,
               None, None, None, 0xFF3008],
            pc=0x22,
            x=1, n=1, z=0, v=0, c=1,
            t1=0, s=0, i=5,
            usp=None,
            ssp=None,
            memory_values=(
                (0xFF2008, 0x1234),
                (0xFF3008, 0xABCD),
            ),

            # Instruction
            cpu_method=ins.trapv,
            program=test_cpu.int_list_to_str(
                program + [0b01001110, 0b01110110]),  # TRAPV
            method_args=(),
            method_kwargs={},
            method_load_program=True,
            cycle=4)


if __name__ == "__main__":
    unittest.main()
