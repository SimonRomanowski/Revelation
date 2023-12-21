# -*- coding: utf-8 -*-
"""
Test the m68k.cpu module.

Created on Sat Sep 16 20:24:06 2023

@author: Simon Romanowski
"""

import unittest

import m68k.cpu as cpu
import megadrive.memory as mem


class TestCpu(unittest.TestCase):

    def test_init(self):
        m = mem.Memory()
        c = cpu.Cpu(m)
        c.set_pc(0)
        c.set_ssp(0x1234)
        check_state(c, m,
                    d=[0]*8, a=[0]*7 + [0x1234],
                    pc=0,
                    x=0, n=0, z=0, v=0, c=0,
                    t1=0, s=1, i=0,
                    usp=0, ssp=0x1234)

    def test_str_0(self):
        expected = """cycle = 0
------------------------------------
  D0 = 0x12345678    A0 = 0xABCD1234
  D1 = 0x23456781    A1 = 0xBCD1234A
  D2 = 0x34567812    A2 = 0xCD1234AB
  D3 = 0x45678123    A3 = 0xD1234ABC
  D4 = 0x56781234    A4 = 0x1234ABCD
  D5 = 0x67812345    A5 = 0x234ABCD1
  D6 = 0x78123456    A6 = 0x34ABCD12
  D7 = 0x81234567    A7 = 0x4ABCD123
------------------------------------
  USP = 0x00000000
  SSP = 0x4ABCD123
------------------------------------
  PC = 0xDEADBEEF
------------------------------------
  T-S--III---XNZVC
  1010011100011111
"""
        cpu_ = init_cpu(
            init_d=[0x12345678, 0x23456781, 0x34567812, 0x45678123,
                    0x56781234, 0x67812345, 0x78123456, 0x81234567],
            init_a=[0xABCD1234, 0xBCD1234A, 0xCD1234AB, 0xD1234ABC,
                    0x1234ABCD, 0x234ABCD1, 0x34ABCD12, 0x4ABCD123],
            init_pc=0xDEADBEEF,
            init_x=1, init_n=1, init_z=1, init_v=1, init_c=1,
            init_t1=1, init_s=1, init_i=7,
            init_mem=())[0]
        actual = str(cpu_)
        assert actual == expected, ("""Expected
####################################
{}
####################################
But got
####################################
{}
####################################
""").format(expected, actual)

    def test_str_1(self):
        expected = """cycle = 0
------------------------------------
  D0 = 0x00000000    A0 = 0x00000000
  D1 = 0x00000000    A1 = 0x00000000
  D2 = 0x00000000    A2 = 0x00000000
  D3 = 0x00000000    A3 = 0x00000000
  D4 = 0x00000000    A4 = 0x00000000
  D5 = 0x00000000    A5 = 0x00000000
  D6 = 0x00000000    A6 = 0x00000000
  D7 = 0x00000000    A7 = 0x00000000
------------------------------------
  USP = 0x00000000
  SSP = 0x00000000
------------------------------------
  PC = 0x00000000
------------------------------------
  T-S--III---XNZVC
  0000000000010000
"""
        cpu_ = init_cpu(
            init_d=None,
            init_a=[0]*8,
            init_pc=0,
            init_x=1, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=0, init_i=0,
            init_usp=0, init_ssp=0,
            init_mem=())[0]
        actual = str(cpu_)
        assert actual == expected, ("""Expected
####################################
{}
####################################
But got
####################################
{}
####################################
""").format(expected, actual)

    def test_str_2(self):
        expected = """cycle = 0
------------------------------------
  D0 = 0x00000000    A0 = 0x00000000
  D1 = 0x00000000    A1 = 0x00000000
  D2 = 0x00000000    A2 = 0x00000000
  D3 = 0x00000000    A3 = 0x00000000
  D4 = 0x00000000    A4 = 0x00000000
  D5 = 0x00000000    A5 = 0x00000000
  D6 = 0x00000000    A6 = 0x00000000
  D7 = 0x00000000    A7 = 0x00000000
------------------------------------
  USP = 0x00000000
  SSP = 0x00000000
------------------------------------
  PC = 0x00000000
------------------------------------
  T-S--III---XNZVC
  0000000000001000
"""
        cpu_ = init_cpu(
            init_d=None,
            init_a=[0]*8,
            init_pc=0,
            init_x=0, init_n=1, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=0, init_i=0,
            init_usp=0, init_ssp=0,
            init_mem=())[0]
        actual = str(cpu_)
        assert actual == expected, ("""Expected
####################################
{}
####################################
But got
####################################
{}
####################################
""").format(expected, actual)

    def test_str_3(self):
        expected = """cycle = 0
------------------------------------
  D0 = 0x00000000    A0 = 0x00000000
  D1 = 0x00000000    A1 = 0x00000000
  D2 = 0x00000000    A2 = 0x00000000
  D3 = 0x00000000    A3 = 0x00000000
  D4 = 0x00000000    A4 = 0x00000000
  D5 = 0x00000000    A5 = 0x00000000
  D6 = 0x00000000    A6 = 0x00000000
  D7 = 0x00000000    A7 = 0x00000000
------------------------------------
  USP = 0x00000000
  SSP = 0x00000000
------------------------------------
  PC = 0x00000000
------------------------------------
  T-S--III---XNZVC
  0000000000000100
"""
        cpu_ = init_cpu(
            init_d=None,
            init_a=[0]*8,
            init_pc=0,
            init_x=0, init_n=0, init_z=1, init_v=0, init_c=0,
            init_t1=0, init_s=0, init_i=0,
            init_usp=0, init_ssp=0,
            init_mem=())[0]
        actual = str(cpu_)
        assert actual == expected, ("""Expected
####################################
{}
####################################
But got
####################################
{}
####################################
""").format(expected, actual)

    def test_str_4(self):
        expected = """cycle = 0
------------------------------------
  D0 = 0x00000000    A0 = 0x00000000
  D1 = 0x00000000    A1 = 0x00000000
  D2 = 0x00000000    A2 = 0x00000000
  D3 = 0x00000000    A3 = 0x00000000
  D4 = 0x00000000    A4 = 0x00000000
  D5 = 0x00000000    A5 = 0x00000000
  D6 = 0x00000000    A6 = 0x00000000
  D7 = 0x00000000    A7 = 0x00000000
------------------------------------
  USP = 0x00000000
  SSP = 0x00000000
------------------------------------
  PC = 0x00000000
------------------------------------
  T-S--III---XNZVC
  0000000000000010
"""
        cpu_ = init_cpu(
            init_d=None,
            init_a=[0]*8,
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=1, init_c=0,
            init_t1=0, init_s=0, init_i=0,
            init_usp=0, init_ssp=0,
            init_mem=())[0]
        actual = str(cpu_)
        assert actual == expected, ("""Expected
####################################
{}
####################################
But got
####################################
{}
####################################
""").format(expected, actual)

    def test_str_5(self):
        expected = """cycle = 0
------------------------------------
  D0 = 0x00000000    A0 = 0x00000000
  D1 = 0x00000000    A1 = 0x00000000
  D2 = 0x00000000    A2 = 0x00000000
  D3 = 0x00000000    A3 = 0x00000000
  D4 = 0x00000000    A4 = 0x00000000
  D5 = 0x00000000    A5 = 0x00000000
  D6 = 0x00000000    A6 = 0x00000000
  D7 = 0x00000000    A7 = 0x00000000
------------------------------------
  USP = 0x00000000
  SSP = 0x00000000
------------------------------------
  PC = 0x00000000
------------------------------------
  T-S--III---XNZVC
  0000000000000001
"""
        cpu_ = init_cpu(
            init_d=None,
            init_a=[0]*8,
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=1,
            init_t1=0, init_s=0, init_i=0,
            init_usp=0, init_ssp=0,
            init_mem=())[0]
        actual = str(cpu_)
        assert actual == expected, ("""Expected
####################################
{}
####################################
But got
####################################
{}
####################################
""").format(expected, actual)

    def test_str_6(self):
        expected = """cycle = 0
------------------------------------
  D0 = 0x00000000    A0 = 0x00000000
  D1 = 0x00000000    A1 = 0x00000000
  D2 = 0x00000000    A2 = 0x00000000
  D3 = 0x00000000    A3 = 0x00000000
  D4 = 0x00000000    A4 = 0x00000000
  D5 = 0x00000000    A5 = 0x00000000
  D6 = 0x00000000    A6 = 0x00000000
  D7 = 0x00000000    A7 = 0x00000000
------------------------------------
  USP = 0x00000000
  SSP = 0x00000000
------------------------------------
  PC = 0x00000000
------------------------------------
  T-S--III---XNZVC
  1000000000000000
"""
        cpu_ = init_cpu(
            init_d=None,
            init_a=[0]*8,
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=1, init_s=0, init_i=0,
            init_usp=0, init_ssp=0,
            init_mem=())[0]
        actual = str(cpu_)
        assert actual == expected, ("""Expected
####################################
{}
####################################
But got
####################################
{}
####################################
""").format(expected, actual)

    def test_str_7(self):
        expected = """cycle = 0
------------------------------------
  D0 = 0x00000000    A0 = 0x00000000
  D1 = 0x00000000    A1 = 0x00000000
  D2 = 0x00000000    A2 = 0x00000000
  D3 = 0x00000000    A3 = 0x00000000
  D4 = 0x00000000    A4 = 0x00000000
  D5 = 0x00000000    A5 = 0x00000000
  D6 = 0x00000000    A6 = 0x00000000
  D7 = 0x00000000    A7 = 0x00000000
------------------------------------
  USP = 0x00000000
  SSP = 0x00000000
------------------------------------
  PC = 0x00000000
------------------------------------
  T-S--III---XNZVC
  0010000000000000
"""
        cpu_ = init_cpu(
            init_d=None,
            init_a=[0]*8,
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=1, init_i=0,
            init_usp=0, init_ssp=0,
            init_mem=())[0]
        actual = str(cpu_)
        assert actual == expected, ("""Expected
####################################
{}
####################################
But got
####################################
{}
####################################
""").format(expected, actual)

    def test_str_8(self):
        expected = """cycle = 0
------------------------------------
  D0 = 0x00000000    A0 = 0x00000000
  D1 = 0x00000000    A1 = 0x00000000
  D2 = 0x00000000    A2 = 0x00000000
  D3 = 0x00000000    A3 = 0x00000000
  D4 = 0x00000000    A4 = 0x00000000
  D5 = 0x00000000    A5 = 0x00000000
  D6 = 0x00000000    A6 = 0x00000000
  D7 = 0x00000000    A7 = 0x00000000
------------------------------------
  USP = 0x00000000
  SSP = 0x00000000
------------------------------------
  PC = 0x00000000
------------------------------------
  T-S--III---XNZVC
  0000010000000000
"""
        cpu_ = init_cpu(
            init_d=None,
            init_a=[0]*8,
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=0, init_i=4,
            init_usp=0, init_ssp=0,
            init_mem=())[0]
        actual = str(cpu_)
        assert actual == expected, ("""Expected
####################################
{}
####################################
But got
####################################
{}
####################################
""").format(expected, actual)

    def test_str_9(self):
        expected = """cycle = 0
------------------------------------
  D0 = 0x00000000    A0 = 0x00000000
  D1 = 0x00000000    A1 = 0x00000000
  D2 = 0x00000000    A2 = 0x00000000
  D3 = 0x00000000    A3 = 0x00000000
  D4 = 0x00000000    A4 = 0x00000000
  D5 = 0x00000000    A5 = 0x00000000
  D6 = 0x00000000    A6 = 0x00000000
  D7 = 0x00000000    A7 = 0x00000000
------------------------------------
  USP = 0x00000000
  SSP = 0x00000000
------------------------------------
  PC = 0x00000000
------------------------------------
  T-S--III---XNZVC
  0000001000000000
"""
        cpu_ = init_cpu(
            init_d=None,
            init_a=[0]*8,
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=0, init_i=2,
            init_usp=0, init_ssp=0,
            init_mem=())[0]
        actual = str(cpu_)
        assert actual == expected, ("""Expected
####################################
{}
####################################
But got
####################################
{}
####################################
""").format(expected, actual)

    def test_str_10(self):
        expected = """cycle = 0
------------------------------------
  D0 = 0x00000000    A0 = 0x00000000
  D1 = 0x00000000    A1 = 0x00000000
  D2 = 0x00000000    A2 = 0x00000000
  D3 = 0x00000000    A3 = 0x00000000
  D4 = 0x00000000    A4 = 0x00000000
  D5 = 0x00000000    A5 = 0x00000000
  D6 = 0x00000000    A6 = 0x00000000
  D7 = 0x00000000    A7 = 0x00000000
------------------------------------
  USP = 0x00000000
  SSP = 0x00000000
------------------------------------
  PC = 0x00000000
------------------------------------
  T-S--III---XNZVC
  0000000100000000
"""
        cpu_ = init_cpu(
            init_d=None,
            init_a=[0]*8,
            init_pc=0,
            init_x=0, init_n=0, init_z=0, init_v=0, init_c=0,
            init_t1=0, init_s=0, init_i=1,
            init_usp=0, init_ssp=0,
            init_mem=())[0]
        actual = str(cpu_)
        assert actual == expected, ("""Expected
####################################
{}
####################################
But got
####################################
{}
####################################
""").format(expected, actual)

    def test_push_00(self):
        c, m = init_cpu(
            init_a=[None, None, None, None,
                    None, None, None, 0xFF1234],
            init_mem=(
                (0xFF1234, 0xABCD),
            )
        )
        c.push(0xCAFE)
        check_state(
            c, m,
            a=[None, None, None, None,
               None, None, None, 0xFF1232],
            memory_values=(
                (0xFF1230, 0),
                (0xFF1232, 0xCAFE),
                (0xFF1234, 0xABCD),
                (0xFF1236, 0),
            )
        )

    def test_push_01(self):
        c, m = init_cpu(
            init_a=[None, None, None, None,
                    None, None, None, 0xFF1234],
            init_mem=(
                (0xFF1234, 0xABCD),
            )
        )
        c.push(0xDEADCAFE, 2)
        check_state(
            c, m,
            a=[None, None, None, None,
               None, None, None, 0xFF1230],
            memory_values=(
                (0xFF122E, 0),
                (0xFF1230, 0xDEAD),
                (0xFF1232, 0xCAFE),
                (0xFF1234, 0xABCD),
                (0xFF1236, 0),
            )
        )


def check_state(
        cpu_, m,
        d=None, a=None,
        pc=None,
        usp=None, ssp=None,
        x=None, n=None, z=None, v=None, c=None, t1=None, s=None, i=None,
        memory_values=(),
        cycle=None):
    """
    Assert that the CPU has a certain state.

    Parameters
    ----------
    cpu_: m68k.cpu.Cpu
        The CPU whose state should be checked.

    m: megadrive.memory.Memory
        The memory that ``cpu_`` uses.

    d, a, pc, usp, ssp, x, n, z, v, c, t1, s, i: optional
        The expected state of the CPU registers. ``d`` and ``a`` are
        sequences of 8 values. Each value is the expected value of the
        corresponding D- or A-register. ``None`` is allowed as a
        "don't care" for a single register or for the entire list.
        ``pc`` is the expected value for the PC register, or ``None``, if
        no specific value is expected.
        ``usp`` and ``ssp`` are the expected values for the user/system stack
        pointers. An explicit error is raised, when the state has conflicting
        values for A7 and the active stack pointer.
        ``x``, ``n``, ``z``, ``v`` and ``c`` are the boolean values of the
        CCR bits or ``None`` if no specific is expected.

    memory_values: Iterable[tuple(int, int)], optional
        Tuples of ``(address, value)`` that define the expected state of
        the memory. The value of any other address is not checked.

    cycle: Optional[int], optional
        The amount of cycles that should have passed after execution. Will not
        be checked if ``None``.
    """
    if d is not None:
        for index in range(8):
            expected = d[index]
            if expected is None:
                continue
            d_value = cpu_.get_d(index)
            assert d_value == expected, (
                "The value of D{} was expected to be 0x{:X} but was "
                "0x{:X}\nCPU:\n{}").format(index, expected, d_value, cpu_)

    if a is not None:
        for index in range(8):
            expected = a[index]
            if expected is None:
                continue
            a_value = cpu_.get_a(index)
            assert a_value == expected, (
                "The value of A{} was expected to be 0x{:X} but was "
                "0x{:X}\nCPU:\n{}").format(index, expected, a_value, cpu_)

    if pc is not None:
        pc_value = cpu_.get_pc()
        assert pc_value == pc, (
            "The value of PC was expected to be 0x{:X} but was "
            "0x{:X}\nCPU:\n{}").format(pc, pc_value, cpu_)

    if x is not None:
        x_value = cpu_.get_x()
        assert x_value == x, (
            "The value of X was expected to be a {} bit but was a "
            "{} bit\nCPU:\n{}").format(int(x), x_value, cpu_)

    if n is not None:
        n_value = cpu_.get_n()
        assert n_value == n, (
            "The value of N was expected to be a {} bit but was a "
            "{} bit\nCPU:\n{}").format(int(n), n_value, cpu_)

    if z is not None:
        z_value = cpu_.get_z()
        assert z_value == z, (
            "The value of Z was expected to be a {} bit but was a "
            "{} bit\nCPU:\n{}").format(int(z), z_value, cpu_)

    if v is not None:
        v_value = cpu_.get_v()
        assert v_value == v, (
            "The value of V was expected to be a {} bit but was a "
            "{} bit\nCPU:\n{}").format(int(v), v_value, cpu_)

    if c is not None:
        c_value = cpu_.get_c()
        assert c_value == c, (
            "The value of C was expected to be a {} bit but was a "
            "{} bit\nCPU:\n{}").format(int(c), c_value, cpu_)

    if t1 is not None:
        t1_value = cpu_.get_t1()
        assert t1_value == t1, (
            "The value of T1 was expected to be a {} bit but was a "
            "{} bit\nCPU:\n{}").format(int(t1), t1_value, cpu_)

    s_value = cpu_.get_s()
    if s is not None:
        assert s_value == s, (
            "The value of S was expected to be a {} bit but was a "
            "{} bit\nCPU:\n{}").format(int(s), s_value, cpu_)

    if i is not None:
        i_value = cpu_.get_i()
        assert i_value == i, (
            "The value of I was expected to be 0b{:03b} but was "
            "0b{:03b}\nCPU:\n{}").format(int(i), i_value, cpu_)

    if s_value:
        if not (a is None or a[7] is None or ssp is None) and a[7] != ssp:
            raise ValueError((
                "Expected system stack to be active, but expected different "
                "values for SSP (0x{:08X}) and A7 (0x{:08X})").format(
                    ssp, a[7]))
    else:
        if not (a is None or a[7] is None or usp is None) and a[7] != usp:
            raise ValueError((
                "Expected user stack to be active, but expected different "
                "values for USP (0x{:08X}) and A7 (0x{:08X})").format(
                    usp, a[7]))

    if usp is not None:
        usp_value = cpu_.get_usp()
        assert usp_value == usp, (
            "The value of USP was expected to be 0x{:08X} but was "
            "0x{:08X}.\nCPU:\n{}").format(usp, usp_value, cpu_)

    if ssp is not None:
        ssp_value = cpu_.get_ssp()
        assert ssp_value == ssp, (
            "The value of SSP was expected to be 0x{:08X} but was "
            "0x{:08X}.\nCPU:\n{}").format(ssp, ssp_value, cpu_)

    for address, ex_value in memory_values:
        mem_value = m.read(address)
        assert mem_value == ex_value, (
            "Expected memory location 0x{:X} to contain the value 0x{:X} "
            "but found 0x{:X}\nCPU:\n{}\nMemory:\n"
            "0x{:08X}: 0x{:04X}\n0x{:08X}: 0x{:04X}\n"
            "0x{:08X}: 0x{:04X}").format(
                address, ex_value, mem_value, cpu_,
                address - 2, m.read(address - 2),
                address, mem_value,
                address + 2, m.read(address + 2))

    if cycle is not None:
        cycle_value = cpu_.get_cycle()
        assert cycle_value == cycle, (
            "Expected {} to have passed, but got {}.").format(
                cycle, cycle_value)

def init_cpu(init_d=None, init_a=None,
             init_pc=None,
             init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
             init_t1=None, init_s=None, init_i=None,
             init_usp=None, init_ssp=None,
             init_mem=(),
             program=None):
    """
    Initialize a ``m68k.cpu.Cpu`` and a ``megadrive.memory.Memory``.

    Parameters
    ----------
    init_d, init_a: None | Sequence[int | None]
        Initial state of the D- and A-registers. ``None`` will leave values
        at their default.

    init_pc: None | int
        Initial program counter. ``None`` will leave it at its default.

    init_x, init_n, init_z, init_v, init_c: None | bool
        Initial values for the CCR. ``None`` will leave them at their
        default.

    init_t1, init_s, init_i: None | bool
        Initial values for the SR. ``None`` will leave them at their
        default.

    init_usp, init_ssp: None | int
        Initial values for user stack pointer and system stack pointer.
        Will only be set if not ``None``. Will potentially override
        ``init_a[7]`` if the S bit is set accordingly.

    init_mem: Iterable[tuple[int, int]]
        Tuples of ``(address, value)`` that will be set before execution.

    Returns
    -------
    c: m68k.cpu.Cpu
        The initialized CPU instance.

    m: megadrive.memory.Memory
        The initialized memory controller.
    """
    # Create and initialize memory
    m = mem.Memory(program)

    for address, value in init_mem:
        m.write(address, value)

    # Create and initialize CPU
    c = cpu.Cpu(m)

    ccr_mask = \
        (0 if init_x is None else 16) \
        + (0 if init_n is None else 8) \
        + (0 if init_z is None else 4) \
        + (0 if init_v is None else 2) \
        + (0 if init_c is None else 1)
    c.set_ccr(ccr_mask,
              bool(init_x),
              bool(init_n),
              bool(init_z),
              bool(init_v),
              bool(init_c))

    sr_mask = \
        (0 if init_t1 is None else 0x80) \
        + (0 if init_s is None else 0x20) \
        + (0 if init_i is None else 7)
    c.set_sr(sr_mask,
             bool(init_t1),
             bool(init_s),
             init_i or 0)

    if init_d is not None:
        for index, value in enumerate(init_d):
            if value is None:
                continue
            c.set_d(index, value)

    if init_a is not None:
        for index, value in enumerate(init_a):
            if value is None:
                continue
            c.set_a(index, value)

    if init_pc is not None:
        c.set_pc(init_pc)

    if init_usp is not None:
        c.set_usp(init_usp)

    if init_ssp is not None:
        c.set_ssp(init_ssp)

    return c, m

def test_instruction(
        cpu_method,
        program,
        init_d=None, init_a=None,
        init_pc=None,
        init_x=None, init_n=None, init_z=None, init_v=None, init_c=None,
        init_t1=None, init_s=None, init_i=None,
        init_usp=None, init_ssp=None,
        init_mem=(),
        d=None, a=None,
        pc=0,
        x=None, n=None, z=None, v=None, c=None,
        t1=None, s=None, i=None,
        usp=None, ssp=None,
        memory_values=(),
        method_args=(),
        method_kwargs=None,
        method_load_program=False,
        cycle=None,
        do_trace=False):
    """
    Test any instruction.

    Parameters
    ----------
    cpu_method: Callable
        Method of ``m68k.cpu.Cpu`` that should be called to simulate the
        instruction directly.

    program: str
        Sequence of bytes representing the instruction in 68k machine code.
        Only the first instruction will be executed.

    init_d, init_a: None | Sequence[int | None]
        Initial state of the D- and A-registers. ``None`` will leave values
        at their default.

    init_pc: int
        Initial program counter. Default is 0.

    init_x, init_n, init_z, init_v, init_c: None | bool
        Initial values for the CCR. ``None`` will leave them at their
        default.

    init_t1, init_s, init_i: None | bool
        Initial values for the SR. ``None`` will leave them at their
        default.

    init_usp, init_ssp: None | int
        Initial values for user stack pointer and system stack pointer.
        Will only be set if not ``None``. Will potentially override
        ``init_a[7]`` if the S bit is set accordingly.

    init_mem: Iterable[tuple[int, int]]
        Tuples of ``(address, value)`` that will be set before execution.

    d, a, pc, x, n, z, v, c, t1, s, i, usp, ssp:
        The expected state of the CPU. Refer to ``_check_state`` for more
        infos.

    memory_values: Iterable[tuple(int, int)]
        Tuples of ``(address, value)`` that define the expected state of
        the memory. The value of any other address is not checked.

    method_args, method_kwargs:
        Tuple of positional arguments and dictionary of keyword arguments
        for the call of ``cpu_method``.

    method_load_program: bool, optional
        If set to ``True``, the program will be loaded into memory even when
        calling ``cpu_method``. In this case, ``init_pc`` is incremented by 2
        (or set to 2 if it was ``None``). The change to ``init_pc`` will only
        be reflected when calling the method, not when executing ``program``.

    cycle: Optional[int], optional
        The amount of cycles that should have passed after execution. Will not
        be checked if ``None``. Default is ``None``.

    do_trace: bool, optional
        Whether to use tracing or not. Default is ``False``.
    """
    if method_kwargs is None:
        method_kwargs = {}
    # Simulate the first program word being loaded
    method_init_pc = init_pc + 2

    # Test the direct method call
    cpu_, m = init_cpu(
        init_d=init_d, init_a=init_a,
        init_pc=method_init_pc,
        init_x=init_x, init_n=init_n, init_z=init_z, init_v=init_v,
        init_c=init_c,
        init_t1=init_t1, init_s=init_s, init_i=init_i,
        init_usp=init_usp, init_ssp=init_ssp,
        init_mem=init_mem,
        program=program if method_load_program else None)

    cpu_method(cpu_, *method_args, **method_kwargs)
    check_state(cpu_, m,
                d=d, a=a,
                pc=pc,
                x=x, n=n, z=z, v=v, c=c,
                t1=t1, s=s, i=i,
                usp=usp, ssp=ssp,
                memory_values=memory_values,
                cycle=cycle)

    # Test the program
    cpu_, m = init_cpu(
        init_d=init_d, init_a=init_a,
        init_pc=init_pc,
        init_x=init_x, init_n=init_n, init_z=init_z, init_v=init_v,
        init_c=init_c,
        init_t1=init_t1, init_s=init_s, init_i=init_i,
        init_usp=init_usp, init_ssp=init_ssp,
        init_mem=init_mem,
        program=program)
    cpu_.step(do_trace=do_trace)
    try:
        check_state(cpu_, m,
                    d=d, a=a,
                    pc=pc,
                    x=x, n=n, z=z, v=v, c=c,
                    t1=t1, s=s, i=i,
                    usp=usp, ssp=ssp,
                    memory_values=memory_values,
                    cycle=cycle)
    except AssertionError as e:
        raise AssertionError(
            "!!! Method call and program caused different results !!!\n"
            + str(e))

def int_list_to_str(ints):
    """Transform a list of byte-sized integers to a string."""
    return "".join(map(chr, ints))


if __name__ == "__main__":
    unittest.main()
