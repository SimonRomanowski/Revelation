# -*- coding: utf-8 -*-
"""
Provides access to M68000 effective address calculation.

Created on Wed Sep 20 11:46:04 2023

@author: Simon Romanowski
"""

from m68k.constants import (
    OP_SIZE_BYTE, OP_SIZE_WORD, OP_SIZE_LONG,
    EA_MODE_REG_A, EA_MODE_A_INDIRECT, EA_MODE_A_POSTINC,
    EA_MODE_A_PREDEC, EA_MODE_A_INDX, EA_MODE_OTHER,
    EA_REGISTER_ABS_WORD, EA_REGISTER_PC_INDX, EA_REGISTER_IMMEDIATE,
)
from utils import int_utils


def split(ea):
    """Split the effective address bits into 'mode' and 'register'."""
    return int_utils.select_bits(ea, 3, 5), int_utils.select_bits(ea, 0, 2)

def is_valid(ea, ea_register=None):
    """Check the effective address bits for validity."""
    if ea_register is None:
        ea_mode, ea_register = split(ea)
    else:
        ea_mode = ea
    return ea_mode != EA_MODE_OTHER or ea_register < 5

def is_data(ea, ea_register=None):
    """Check, if the effective address bits are data addressing."""
    if ea_register is None:
        ea_mode, ea_register = split(ea)
    else:
        ea_mode = ea
    return is_valid(ea_mode, ea_register) and ea_mode != EA_MODE_REG_A

def is_memory(ea, ea_register=None):
    """Check, if the effective address bits are memory addressing."""
    if ea_register is None:
        ea_mode, ea_register = split(ea)
    else:
        ea_mode = ea
    return is_valid(ea_mode, ea_register) and ea_mode > EA_MODE_REG_A

def is_control(ea, ea_register=None):
    """Check, if the effective address bits are control addressing."""
    if ea_register is None:
        ea_mode, ea_register = split(ea)
    else:
        ea_mode = ea
    return \
        is_valid(ea_mode, ea_register) \
        and (ea_mode > 4 or ea_mode == EA_MODE_A_INDIRECT) \
        and (ea_mode != EA_MODE_OTHER or ea_register != EA_REGISTER_IMMEDIATE)

def is_alterable(ea, ea_register=None):
    """Check, if the effective address bits are alterable addressing."""
    if ea_register is None:
        ea_mode, ea_register = split(ea)
    else:
        ea_mode = ea
    return ea_mode != EA_MODE_OTHER  # All modes != 7 are valid


def is_data_alterable(ea, ea_register=None):
    """Check, if the effective address bits are alterable addressing."""
    if ea_register is None:
        ea_mode, ea_register = split(ea)
    else:
        ea_mode = ea
    return ea_mode != EA_MODE_REG_A \
        and (ea_mode != EA_MODE_OTHER or ea_register < 2)


def is_memory_alterable(ea, ea_register=None):
    """Check, if the effective address bits are alterable addressing."""
    if ea_register is None:
        ea_mode, ea_register = split(ea)
    else:
        ea_mode = ea
    return ea_mode > 1 \
        and (ea_mode != EA_MODE_OTHER or ea_register < 2)


def _resolve_register(ea_mode, ea_register):
    return ea_register + (ea_mode << 3)

def resolve_address(cpu, ea_mode, ea_register, op_size):
    """
    Resolve address register indirect effective address.

    Parameters
    ----------
    cpu: m68k.cpu.Cpu
        The CPU instance to work on.

    ea_mode, ea_register: int
        Define the effective address mode.

    op_size: int
        The size of the operation. Influences postincrement and predecrement
        modes.

    Returns
    -------
    address: int
        The memory address that the effective address refers to.

    cycles: int
        The amount of cycles the calculation took.
    """
    address = cpu.get_a(ea_register)
    cycles = 8 if op_size == OP_SIZE_LONG else 4
    size_displacement = (4 if op_size == OP_SIZE_LONG else op_size + 1)
    # Stack pointer is always aligned to word boundary
    if ea_register == 7:
        size_displacement = max(2, size_displacement)

    if ea_mode == EA_MODE_A_PREDEC:
        # Predecrement mode
        cycles += 2
        # Decrement according to operation size
        address -= size_displacement
        cpu.set_a(ea_register, address)
    elif ea_mode == EA_MODE_A_POSTINC:
        # Postincrement mode
        # Increment according to operation size
        cpu.set_a(ea_register, address + size_displacement)

    return address, cycles

def resolve_absolute(cpu, ea_register, op_size):
    """
    Resolve absolute effective address.

    Parameters
    ----------
    cpu: m68k.cpu.Cpu
        The CPU instance to work on.

    ea_register: int
        Defines the effective address mode.

    op_size: int
        The size of the operation. Influences amount of cycles.

    Returns
    -------
    address: int
        The memory address that the effective address refers to.

    cycles: int
        The amount of cycles the calculation took.
    """
    # Load first extension word
    first_ext = cpu.fetch_next()
    if ea_register == EA_REGISTER_ABS_WORD:
        # Address is sign-extended first extension word
        address = int_utils.sign_extend_16_to_32(first_ext)
        cycles = 8
    else:
        # First extension word is the upper 16 bit of the address
        second_ext = cpu.fetch_next()
        address = (first_ext << 16) | second_ext
        cycles = 12

    if op_size == OP_SIZE_LONG:
        cycles += 4

    return address, cycles

def resolve_displacement(cpu, ea_mode, ea_register, op_size):
    """
    Resolve address register / PC indirect with displacement effective address.

    Parameters
    ----------
    cpu: m68k.cpu.Cpu
        The CPU instance to work on.

    ea_mode, ea_register: int
        Define the effective address mode.

    op_size: int
        The size of the operation. Influences postincrement and predecrement
        modes.

    Returns
    -------
    address: int
        The memory address that the effective address refers to.

    cycles: int
        The amount of cycles the calculation took.
    """
    ext_word = cpu.fetch_next()
    cycles = 8
    if ea_mode == EA_MODE_OTHER:
        # PC indirect
        # Value is the address of the extension word
        base_value = cpu.get_pc() - 2
        has_index_register = (ea_register == EA_REGISTER_PC_INDX)
    else:
        # Address register indirect
        base_value = cpu.get_a(ea_register)
        has_index_register = (ea_mode == EA_MODE_A_INDX)

    if has_index_register:
        cycles += 2
        # Base displacement is 8 bit value, sign-extended to 32 bit
        displacement = int_utils.sign_extend_8_to_32(ext_word & 0xFF)
        # Index register type
        registers = \
            cpu.a_registers if ext_word & 0x8000 else cpu.d_registers
        # Index is bits 14-12
        reg_index = int_utils.select_bits(ext_word, 12, 14)
        register = registers[reg_index]
        # Bit 11 is the register size bit
        reg_long = ext_word & 0x800
        reg_value = register.get() if reg_long else register.get_word()
        if not reg_long:
            # Sign-extend the register word value
            reg_value = int_utils.sign_extend_16_to_32(reg_value)
        displacement = (displacement + reg_value) & 0xFFFFFFFF
    else:
        # Use sign-extended extension word
        displacement = int_utils.sign_extend_16_to_32(ext_word)

    if op_size == OP_SIZE_LONG:
        cycles += 4

    address = (base_value + displacement) & 0xFFFFFFFF
    return address, cycles

def accessors(cpu, ea_mode, ea_register, op_size):
    """
    Get the get and set functions for the given effective address mode.

    This might increase the PC, if extension words are expected for the
    effective address mode.

    Parameters
    ----------
    cpu: m68k.cpu.Cpu
        The CPU instance for which to get the accessors.

    ea_mode, ea_register: int
        Define the type of effective address.

    op_size: int
        Value from 0 to 2. Defines the size of the operation.

    Returns
    -------
    get_func: Callable[[m68k.cpu.Cpu, int], int]
        This function will retrieve the value that the effective address
        refers to when called with ``address``.

    set_func: None | Callable[[m68k.cpu.Cpu, int, int], None]
        This function may be called with ``address`` as the first and the
        new value as the second parameter. Might be ``None`` if the
        effective address points to a location that is not writable.

    address: int
        Address parameter for ``set_func``.

    cycles: int
        The amount of cycles the calculation took.
    """
    if ea_mode < 2:
        # Register direct
        reg_address = _resolve_register(ea_mode, ea_register)

        # TODO bake 'op_size' into 'reg_address' and combine these methods
        if op_size == OP_SIZE_BYTE:
            get_func = _register_get_byte
            set_func = _register_set_byte
        elif op_size == OP_SIZE_WORD:
            get_func = _register_get_word
            set_func = _register_set_word
        else:
            get_func = _register_get_long
            set_func = _register_set_long
        return get_func, set_func, reg_address, 0

    elif ea_mode == EA_MODE_OTHER and ea_register == EA_REGISTER_IMMEDIATE:
        # Immediate value
        cycles = 4
        value = cpu.fetch_next()
        if op_size == OP_SIZE_LONG:
            # Long word
            cycles += 4
            second_ext = cpu.fetch_next()
            value = (value << 16) | second_ext
        elif op_size == OP_SIZE_BYTE:
            # Byte
            value &= 0xFF

        # Slightly cheating here, but this holds the contract
        # 'int' could be any function that will just return 'value'
        return _return_address, None, value, cycles

    # - Value is in memory -

    elif ea_mode < 5:
        # Address register indirect
        address, cycles = resolve_address(cpu, ea_mode, ea_register, op_size)

    elif ea_mode == EA_MODE_OTHER and ea_register < 2:
        # Absolute short/long addressing mode
        address, cycles = resolve_absolute(cpu, ea_register, op_size)

    else:
        # Address register / PC indirect with extension (and index
        # register)
        address, cycles = resolve_displacement(
            cpu, ea_mode, ea_register, op_size)

    # Resolve address
    if op_size == OP_SIZE_BYTE:
        get_func = _get_mem_byte
        set_func = _set_mem_byte
    elif op_size == OP_SIZE_WORD:
        get_func = _get_mem_word
        set_func = _set_mem_word
    else:
        # Long word
        get_func = _get_mem_long
        set_func = _set_mem_long

    return get_func, set_func, address, cycles

def _register_get_byte(cpu, reg_address):
    if reg_address & 8:
        return cpu.get_a(reg_address & 7, OP_SIZE_BYTE)
    return cpu.get_d(reg_address & 7, OP_SIZE_BYTE)

def _register_get_word(cpu, reg_address):
    if reg_address & 8:
        return cpu.get_a(reg_address & 7, OP_SIZE_WORD)
    return cpu.get_d(reg_address & 7, OP_SIZE_WORD)

def _register_get_long(cpu, reg_address):
    if reg_address & 8:
        return cpu.get_a(reg_address & 7, OP_SIZE_LONG)
    return cpu.get_d(reg_address & 7, OP_SIZE_LONG)

def _register_set_byte(cpu, reg_address, value):
    if reg_address & 8:
        cpu.set_a(reg_address & 7, value)
    else:
        cpu.set_d(reg_address & 7, value, OP_SIZE_BYTE)

def _register_set_word(cpu, reg_address, value):
    if reg_address & 8:
        cpu.set_a(reg_address & 7, value)
    else:
        cpu.set_d(reg_address & 7, value, OP_SIZE_WORD)

def _register_set_long(cpu, reg_address, value):
    if reg_address & 8:
        cpu.set_a(reg_address & 7, value)
    else:
        cpu.set_d(reg_address & 7, value, OP_SIZE_LONG)

def _return_address(_, address):
    return address

def _get_mem_byte(cpu, address):
    return (cpu.mem.read(address) & 0xFF00) >> 8

def _set_mem_byte(cpu, address, value):
    # Get the original value
    o_value = cpu.mem.read(address)
    cpu.mem.write(address, (o_value & 0xFF) | (value << 8))

def _get_mem_word(cpu, address):
    return cpu.mem.read(address)

def _set_mem_word(cpu, address, value):
    cpu.mem.write(address, value)

def _get_mem_long(cpu, address):
    # Get both words
    lower = cpu.mem.read(address + 2)
    higher = cpu.mem.read(address)
    # Combine
    return (higher << 16) | lower

def _set_mem_long(cpu, address, value):
    # Next write should only write the higher word
    cpu.mem.write(address, value >> 16)
    # Write the lower word from 'value'
    cpu.mem.write(address + 2, value)  # Already trims to 16 bit
