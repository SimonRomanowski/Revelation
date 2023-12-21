# -*- coding: utf-8 -*-
"""
Concerned with the execution of 68k instructions.

Created on Thu Sep 21 22:31:36 2023

@author: Simon Romanowski
"""

from utils import int_utils
import m68k.effective_address as ea
from m68k.constants import (
    OP_SIZE_BYTE, OP_SIZE_WORD, OP_SIZE_LONG,

    EA_MODE_REG_D, EA_MODE_REG_A, EA_MODE_A_INDIRECT, EA_MODE_A_POSTINC,
    EA_MODE_A_PREDEC, EA_MODE_A_DISP, EA_MODE_A_INDX, EA_MODE_OTHER,

    EA_REGISTER_ABS_WORD, EA_REGISTER_ABS_LONG, EA_REGISTER_PC_DISP,
    EA_REGISTER_PC_INDX, EA_REGISTER_IMMEDIATE,

    CCR_ALL, CCR_X, CCR_N, CCR_Z, CCR_V, CCR_C, SR_ALL
)
from m68k.errors import IllegalInstruction, PrivilegeError


# --- Instruction helpers ---

def _raise_ea_error(ea_mode, ea_register):
    raise IllegalInstruction(
        "Invalid effective address %d, %d" % (ea_mode, ea_register))


def _binary_op_write_result(cpu,
                            result,
                            op_size,
                            register_index,
                            ea_address,
                            write_to_ea,
                            ea_mode, ea_set, ea_cycles):
    # Same for ADD, AND, OR and SUB
    if write_to_ea:
        ea_set(cpu, ea_address, result)

        cycles = (12 if op_size == OP_SIZE_LONG else 8)
    else:
        cpu.set_d(register_index, result, op_size)

        # Needs 2 extra cycles if effective address is register direct or
        # immediate and size is long word
        extra_cycles = (2 if ea_mode in (0, 1, 0b111) else 0)
        cycles = ((6 + extra_cycles) if op_size == OP_SIZE_LONG else 4)

    # In any case, calculation of the effective address is added on top
    cpu.increment_cycles(cycles + ea_cycles)


def _load_immediate(cpu, op_size):
    v0 = cpu.fetch_next()
    if op_size == OP_SIZE_BYTE:
        v0 &= 0xFF
    elif op_size == OP_SIZE_LONG:
        # Combine to 32 bits with next word
        v0 = (v0 << 16) | cpu.fetch_next()
    return v0


def _bit_masks(op_size):
    # Mask for the relevant bits of the result
    size_displacement = 3 if op_size == OP_SIZE_LONG else op_size
    mask = 0xFFFFFFFF >> (8 * (3 - size_displacement))
    # Mask for the most significant bit
    msb_mask = (0x80 << 8 * size_displacement)
    return mask, msb_mask


def _shift_value(cpu, value, shift_amount, op_size, direction, is_arith=True):
    """Calculate the shift, set CCR and return the result."""
    mask, msb_mask = _bit_masks(op_size)
    value_msb = value & msb_mask

    if shift_amount != 0:
        ccr_mask = CCR_ALL
        if direction == 0:
            # Sign-extend from the left
            fill_mask = \
                ~((msb_mask - 1) >> (shift_amount - 1)) \
                if value_msb and is_arith \
                else 0
            result_raw = (value >> shift_amount) | fill_mask
        else:
            result_raw = value << shift_amount

        result = result_raw & mask

        # Set CCR
        result_msb = result & msb_mask
        if direction == 0:
            c_bit = \
                False if shift_amount == 0 \
                else bool(int_utils.select_bits(value, shift_amount - 1))
            # Sign only changes on logical shift when the value was negative
            v_bit = not is_arith and bool(value & msb_mask)
        else:
            c_bit = bool(result_raw & (msb_mask << 1))
            # The bits that were shifted out of the value
            start = 32 if op_size == OP_SIZE_LONG else (8 * (op_size + 1))
            removed_bits = \
                int_utils.select_bits(result_raw, start, start + shift_amount)
            # The bits that were moved out of the value have to be either all 0
            # or all 1, which is (1 << shift_amount) - 1
            msb_flipped = \
                not (removed_bits == 0 or removed_bits == (1 << shift_amount) - 1)
            v_bit = result_msb != value_msb or msb_flipped
    else:
        result = value
        v_bit = False
        c_bit = 0
        ccr_mask = CCR_ALL ^ CCR_X
        result_msb = 0

    cpu.set_ccr(ccr_mask,
                x=c_bit,
                n=bool(result_msb),
                z=not result,
                v=v_bit,
                c=c_bit)

    return result


def _evaluate_condition(cpu, condition):
    """Evaluate a branching condition."""
    if condition == 0:
        value = True
    elif condition == 1:
        value = False
    elif condition == 2:
        value = not (cpu.get_c() or cpu.get_z())
    elif condition == 3:
        value = cpu.get_c() or cpu.get_z()
    elif condition == 4:
        value = not cpu.get_c()
    elif condition == 5:
        value = cpu.get_c()
    elif condition == 6:
        value = not cpu.get_z()
    elif condition == 7:
        value = cpu.get_z()
    elif condition == 8:
        value = not cpu.get_v()
    elif condition == 9:
        value = cpu.get_v()
    elif condition == 10:
        value = not cpu.get_n()
    elif condition == 11:
        value = cpu.get_n()
    elif condition == 12:
        value = cpu.get_v() == cpu.get_n()
    elif condition == 13:
        value = cpu.get_v() != cpu.get_n()
    elif condition == 14:
        value = not cpu.get_z() and cpu.get_n() == cpu.get_v()
    else:
        value = cpu.get_z() or cpu.get_n() != cpu.get_v()
    return value


def _subtract_set_ccr(cpu, dst, src, op_size, set_x=False, always_set_z=True):
    mask, msb_mask = _bit_masks(op_size)
    result = (dst - src) & mask
    # Set CCR
    res_msb = result & msb_mask
    dst_msb = dst & msb_mask
    src_msb = src & msb_mask
    c_bit = bool(
        (src_msb and not dst_msb)
        or (res_msb and not dst_msb)
        or (src_msb and res_msb))
    v_bit = bool(
        (not src_msb and dst_msb and not res_msb)
        or (src_msb and not dst_msb and res_msb))

    z_bit = not (result & mask)
    ccr_mask = CCR_ALL
    if not set_x:
        ccr_mask = ccr_mask ^ CCR_X
    if not always_set_z and z_bit:
        # Only set z_bit to 0
        ccr_mask = ccr_mask ^ CCR_Z
    cpu.set_ccr(
        ccr_mask,
        x=c_bit,
        n=bool(res_msb),
        z=z_bit,
        v=v_bit,
        c=c_bit)

    return result


def _rotate_value(cpu, value, rotate_amount, op_size, direction):
    """Calculate the rotation, set CCR and return the result."""
    mask, msb_mask = _bit_masks(op_size)
    if rotate_amount != 0:
        # Amount of places to shift the bits that do get rotated out of the value
        bit_amount = 32 if op_size == OP_SIZE_LONG else (8 + 8*op_size)
        shift_amount = bit_amount - rotate_amount
        if direction == 0:
            # Rotate right
            # Mask for the bits that will be rotated out of the value
            out_mask = (1 << rotate_amount) - 1
            # Mask for the bits that are not rotated out
            move_mask = ~out_mask & mask

            out_bits = (value & out_mask) << shift_amount
            move_bits = (value & move_mask) >> rotate_amount

            # The last bit that was shifted out of the value
            c_bit = bool(out_bits & msb_mask)
        else:
            # Rotate left
            # Mask for the bits that are not rotated out
            move_mask = (1 << shift_amount) - 1
            # Mask for the bits that will be rotated out of the value
            out_mask = ~move_mask & mask

            out_bits = (value & out_mask) >> shift_amount
            move_bits = (value & move_mask) << rotate_amount

            # The last bit that was shifted out of the value
            c_bit = bool(out_bits & 1)

        result = out_bits | move_bits
    else:
        result = value
        c_bit = 0

    # Set CCR
    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(result & msb_mask),
                z=not result,
                v=False,
                c=c_bit)

    return result


def _rotate_value_extend(cpu, value, rotate_amount, op_size, direction):
    """Calculate the rotation with extend, set CCR and return the result."""
    mask, msb_mask = _bit_masks(op_size)
    if rotate_amount != 0:
        # Amount of places to shift the bits that do get rotated out of the value
        bit_amount = 32 if op_size == OP_SIZE_LONG else (8 + 8*op_size)
        shift_amount = bit_amount - rotate_amount
        ccr_mask = CCR_ALL

        if direction == 0:
            # Rotate right
            # Mask for the bits that will be rotated out of the value
            out_mask = (1 << rotate_amount) - 1
            # Mask for the bits that are not rotated out
            move_mask = ~out_mask & mask

            out_bits = (value & out_mask) << (shift_amount + 1)
            move_bits = (value & move_mask) >> rotate_amount
            x_value = (cpu.get_x() << shift_amount)

            result = (move_bits | out_bits | x_value) & mask

            # The last bit that was shifted out of the value
            c_bit = int_utils.select_bits(value, rotate_amount - 1)
        else:
            # Rotate left
            # Mask for the bits that are not rotated out
            move_mask = (1 << shift_amount) - 1
            # Mask for the bits that will be rotated out of the value
            out_mask = ~move_mask & mask

            out_bits = (value & out_mask) >> (shift_amount + 1)
            move_bits = (value & move_mask) << rotate_amount
            x_value = (cpu.get_x() << (rotate_amount - 1))

            result = move_bits | out_bits | x_value

            # The last bit that was shifted out of the value
            c_bit = int_utils.select_bits(value, shift_amount)

    else:
        result = value
        ccr_mask = CCR_ALL ^ CCR_X
        c_bit = cpu.get_x()

    # Set CCR
    cpu.set_ccr(ccr_mask,
                x=c_bit,
                n=bool(result & msb_mask),
                z=not result,
                v=False,
                c=c_bit)

    return result


# --- Instruction implementation ---

def abcd(cpu, register_src, register_dst, op_type):
    """
    Add decimal with the extend bit.

    Parameters
    ----------
    register_src, register_dst: int
        Index of the source and destination registers.

    op_type: int
        If 0, the register indices are for data registers, else they are
        for address registers that will be dereferenced with predecrement
        addressing mode.
    """
    use_address = op_type == 1
    # Read operands
    if use_address:
        src_get, _, src_address, _ = ea.accessors(
            cpu, EA_MODE_A_PREDEC, register_src, OP_SIZE_BYTE)
        src = src_get(cpu, src_address)

        dst_get, dst_set, dst_address, _ = ea.accessors(
            cpu, EA_MODE_A_PREDEC, register_dst, OP_SIZE_BYTE)
        dst = dst_get(cpu, dst_address)
    else:
        # Data register to data register
        src = cpu.get_d(register_src, OP_SIZE_BYTE)
        dst = cpu.get_d(register_dst, OP_SIZE_BYTE)
        # For RPython, this needs to be set:
        dst_set = None
        dst_address = 0

    first_digit_raw = (src & 0xF) + (dst & 0xF) + cpu.get_x()
    # Always has to be a value from 0-9
    first_digit = first_digit_raw % 10
    # The remainder is the second decimal digit of the first result.
    first_remainder = (first_digit_raw - first_digit) // 10

    second_digit_raw = \
        int_utils.select_bits(src, 4, 7) \
        + int_utils.select_bits(dst, 4, 7) \
        + first_remainder
    second_digit = second_digit_raw % 10
    # We do not need to  adjust this, we only need to know if it is > 0
    second_remainder = second_digit_raw - second_digit

    result = ((second_digit << 4) | first_digit) | (dst & 0xFFFFFF00)

    # Set CCR
    z_bit = first_digit == 0 and second_digit == 0 and second_remainder == 0
    c_bit = second_remainder != 0
    # Only set Z to 0, otherwise we leave it unchanged
    ccr_mask = CCR_X | CCR_C
    if not z_bit:
        ccr_mask |= CCR_Z
    cpu.set_ccr(ccr_mask, x=c_bit, z=z_bit, c=c_bit)

    # Write result
    if use_address:
        dst_set(cpu, dst_address, result)
        cycles = 18
    else:
        cpu.set_d(register_dst, result, OP_SIZE_BYTE)
        cycles = 6
    cpu.increment_cycles(cycles)


def add(cpu, register_index, op_type, op_size, ea_mode, ea_register):
    """
    Add two values.

    Parameters
    ----------
    register_index: int
        Value from 0 to 7 that indicates the register index for either the
        source (``op_type == 1``) or the destination (``op_type == 0``).

    op_type: int
        Determines whether the effective address and the register are
        source or destination. 0 means register is the destination, 1 means
        register is the source.

    op_size: int
        Defines the size of the operands.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    # When writing to effective address, only memory mode is valid
    write_to_ea = (op_type == 1)
    if not ((write_to_ea and ea.is_memory_alterable(ea_mode, ea_register))
             or (not write_to_ea
                 and ea.is_valid(ea_mode, ea_register)
                 and (op_size != OP_SIZE_BYTE or ea_mode != EA_MODE_REG_A))):
        _raise_ea_error(ea_mode, ea_register)
    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)
    v0 = ea_get(cpu, ea_address)
    v1 = cpu.get_d(register_index, op_size)

    # Mask for the relevant bits of the result
    mask, msb_mask = _bit_masks(op_size)

    # TODO This needs to be changed for 32-bit machines
    result_raw = v0 + v1
    result = result_raw & mask

    # Set CCR
    c_bit = bool(result_raw & (mask + 1))  # The bit after the MSB is set
    result_msb = result & msb_mask
    v0_msb = v0 & msb_mask

    cpu.set_ccr(
        CCR_ALL,
        x=c_bit,  # Same as C
        n=bool(result_msb),
        z=not result,
        # Overflow is when the sign of 'v0' and 'v1' are the same, but
        # 'result' has a different one.
        v=bool((v0_msb == (v1 & msb_mask))
               and (v0_msb != result_msb)),
        c=c_bit)

    _binary_op_write_result(cpu,
                            result,
                            op_size,
                            register_index,
                            ea_address,
                            write_to_ea,
                            ea_mode, ea_set, ea_cycles)


def adda(cpu, register_index, op_size, ea_mode, ea_register):
    """
    Add to address register.

    Parameters
    ----------
    register_index: int
        Index of the address register to add to.

    op_size: int
        0 for word-sized source operand with sign-extension, else long
        word.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the source.
    """
    # All valid effective address modes are allowed
    if not ea.is_valid(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    is_word_op = op_size == 0
    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu,
        ea_mode, ea_register,
        OP_SIZE_WORD if is_word_op else OP_SIZE_LONG)
    src = ea_get(cpu, ea_address)

    if is_word_op:
        src = int_utils.sign_extend_16_to_32(src)

    dst = cpu.get_a(register_index)

    result = src + dst

    cpu.set_a(register_index, result)

    # Increment cycle
    if is_word_op:
        cycles = 8
    else:
        # Needs 2 more cycles if effective address is register direct or
        # immediate
        extra_cycles = \
            2 if (ea_mode < 2
                  or (ea_mode == EA_MODE_OTHER
                      and ea_register == EA_REGISTER_IMMEDIATE)) \
            else 0
        cycles = 6 + extra_cycles
    # Cycles for effective address calculation are always added on top
    cpu.increment_cycles(cycles + ea_cycles)


def addi(cpu, op_size, ea_mode, ea_register):
    """
    Add immediate.

    Parameters
    ----------
    op_size:
        Defines the size of the immediate and destination operands.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the
        destination.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    # Read the immediate operand before resolving the effective address!
    v0 = _load_immediate(cpu, op_size)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)
    v1 = ea_get(cpu, ea_address)

    # Mask for the relevant bits of the result
    mask, msb_mask = _bit_masks(op_size)

    result_raw = v0 + v1
    result = result_raw & mask

    # Set CCR
    c_bit = bool(result_raw & (mask + 1))  # The bit after the MSB is set
    result_msb = result & msb_mask
    v0_msb = v0 & msb_mask

    cpu.set_ccr(
        CCR_ALL,
        x=c_bit,  # Same as C
        n=bool(result_msb),
        z=not result,
        # Overflow is when the sign of 'v0' and 'v1' are the same, but
        # 'result' has a different one.
        v=bool((v0_msb == (v1 & msb_mask))
               and (v0_msb != result_msb)),
        c=c_bit)

    ea_set(cpu, ea_address, result)

    cycles = 16 if op_size == OP_SIZE_LONG else 8
    if ea_mode != EA_MODE_REG_D:
        cycles += 4
    cpu.increment_cycles(cycles + ea_cycles)


def addq(cpu, value, op_size, ea_mode, ea_register):
    """
    Add quick.

    Parameters
    ----------
    value: int
        Value to add to the destination. 0 means to add 8.

    op_size:
        Defines the size of the destination operand, if it is not address
        register direct, in which case it is always long word.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the
        destination.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ((ea.is_alterable(ea_mode, ea_register)
             or (ea_mode == EA_MODE_OTHER and ea_register < 2))
            and (op_size != OP_SIZE_BYTE or ea_mode != EA_MODE_REG_A)):
        _raise_ea_error(ea_mode, ea_register)

    to_address = ea_mode == EA_MODE_REG_A
    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_LONG if to_address else op_size)

    v0 = ea_get(cpu, ea_address)
    v1 = 8 if value == 0 else value

    mask, msb_mask = _bit_masks(OP_SIZE_LONG if to_address else op_size)

    result_raw = v0 + v1
    result = result_raw & mask

    # Set CCR
    c_bit = bool(result_raw & (mask + 1))  # The bit after the MSB is set
    result_msb = result & msb_mask
    v0_msb = v0 & msb_mask

    if not to_address:
        cpu.set_ccr(
            CCR_ALL,
            x=c_bit,  # Same as C
            n=bool(result_msb),
            z=not result,
            # Overflow is when the sign of 'v0' and 'v1' are the same, but
            # 'result' has a different one.
            v=bool((v0_msb == (v1 & msb_mask))
                   and (v0_msb != result_msb)),
            c=c_bit)

    ea_set(cpu, ea_address, result)

    # Set cycles
    if ea_mode < 2:
        cycles = 8 if op_size == OP_SIZE_LONG else 4
    else:
        cycles = (12 if op_size == OP_SIZE_LONG else 8) + ea_cycles
    cpu.increment_cycles(cycles)


def addx(cpu, register_src, register_dst, op_type, op_size):
    """
    Add with extend bit.

    Parameters
    ----------
    register_src, register_dst: int
        Index of the source and destination registers.

    op_type: int
        If 0, the register indices are for data registers, else they are
        for address registers that will be dereferenced with predecrement
        addressing mode.

    op_size: int
        Defines the size of the operands.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    use_address = op_type == 1
    if use_address:
        ea_mode = EA_MODE_A_PREDEC
    else:
        ea_mode = EA_MODE_REG_D

    dst_get, dst_set, dst_address, _ = ea.accessors(
        cpu, ea_mode, register_dst, op_size)
    src_get, _, src_address, _ = ea.accessors(
        cpu, ea_mode, register_src, op_size)

    dst = dst_get(cpu, dst_address)
    src = src_get(cpu, src_address)

    # Mask for the relevant bits of the result
    mask, msb_mask = _bit_masks(op_size)

    result = src + dst + cpu.get_x()

    dst_set(cpu, dst_address, result)

    # Set CCR
    c_bit = bool(result & (mask + 1))  # The bit after the MSB is set
    result_msb = result & msb_mask
    src_msb = src & msb_mask
    z_bit = not (result & mask)

    ccr_mask = CCR_ALL ^ CCR_Z
    if not z_bit:
        ccr_mask |= CCR_Z
    cpu.set_ccr(ccr_mask,
                x=c_bit,
                z=z_bit,
                v=(src_msb == (dst & msb_mask)) and (src_msb != result_msb),
                c=c_bit)

    # Write result
    if use_address:
        cycles = 30 if op_size == OP_SIZE_LONG else 18
    else:
        cycles = 8 if op_size == OP_SIZE_LONG else 4
    cpu.increment_cycles(cycles)


def and_(cpu, register_index, op_type, op_size, ea_mode, ea_register):
    """
    Build logical conjunction of two values.

    Parameters
    ----------
    register_index: int
        Value from 0 to 7 that indicates the register index for either the
        source (``op_type == 1``) or the destination (``op_type == 0``).

    op_type: int
        Determines whether the effective address and the register are
        source or destination. 0 means register is the destination, 1 means
        register is the source.

    op_size: int
        Defines the size of the operands.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    # When writing to effective address, only memory mode is valid
    write_to_ea = (op_type == 1)
    if not ((write_to_ea and ea.is_memory_alterable(ea_mode, ea_register))
             or (not write_to_ea and ea.is_data(ea_mode, ea_register))):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, ea_set, address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)
    v0 = ea_get(cpu, address)
    v1 = cpu.get_d(register_index, op_size)

    # Mask for the relevant bits of the result
    msb_mask = _bit_masks(op_size)[1]

    result = v0 & v1

    # Set CCR
    result_msb = result & msb_mask
    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(result_msb),
                z=not result,
                v=False,
                c=False)

    _binary_op_write_result(cpu,
                            result,
                            op_size,
                            register_index,
                            address,
                            write_to_ea,
                            ea_mode, ea_set, ea_cycles)


def andi(cpu, op_size, ea_mode, ea_register):
    """
    Logical conjunction with immediate.

    Parameters
    ----------
    op_size:
        Defines the size of the immediate and destination operands.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the
        destination.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    v0 = _load_immediate(cpu, op_size)
    msb_mask = _bit_masks(op_size)[1]

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)

    result = v0 & ea_get(cpu, ea_address)

    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(result & msb_mask),
                z=not result,
                v=0, c=0)

    ea_set(cpu, ea_address, result)

    if ea_mode < 2:
        cycles = 14 if op_size == OP_SIZE_LONG else 8
    else:
        cycles = (20 if op_size == OP_SIZE_LONG else 12) + ea_cycles
    cpu.increment_cycles(cycles)


def andi_to_ccr(cpu):
    """
    Logical conjunction with CCR.

    Takes the next instruction word as the second operand. Only considers
    its lower 5 bits.
    """
    value = cpu.get_sr_full() & _load_immediate(cpu, OP_SIZE_WORD)
    cpu.set_ccr(CCR_ALL,
                int_utils.select_bits(value, 4),
                int_utils.select_bits(value, 3),
                int_utils.select_bits(value, 2),
                int_utils.select_bits(value, 1),
                int_utils.select_bits(value, 0))
    cpu.increment_cycles(20)


def andi_to_sr(cpu):
    """
    Logical conjunction with status register.

    Priviliged instruction. Takes the next instruction word as the second
    operand. Only affects the bits of the status register, that are not
    constant.
    """
    if not cpu.get_s():
        raise PrivilegeError()
    value = cpu.get_sr_full() & _load_immediate(cpu, OP_SIZE_WORD)
    cpu.set_ccr(CCR_ALL,
                int_utils.select_bits(value, 4),
                int_utils.select_bits(value, 3),
                int_utils.select_bits(value, 2),
                int_utils.select_bits(value, 1),
                int_utils.select_bits(value, 0))
    cpu.set_sr(SR_ALL,
               int_utils.select_bits(value, 15),
               int_utils.select_bits(value, 13),
               int_utils.select_bits(value, 8, 10))
    cpu.increment_cycles(20)


def asl_asr_to_data(
        cpu, register_index, shift_amount, op_type, op_size, direction):
    """
    Arithmetic shift left/right to data register.

    Parameters
    ----------
    register_index: int
        The index of the data register to shift.

    shift_amount: int
        Amount of bits to shift by (value 0 means a shift by 8) if
        ``op_type == 0``, else index of the register containing that
        amount (is taken modulo 32 before).

    op_type: int
        Whether ``shift_amount`` is a value (0) or a register index (1).

    op_size: int
        Defines the size of the shifted operand.

    direction: int
        Determines the shift direction. 0 means right, 1 means left.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    # Get shift amount
    if op_type == 0:
        shift_amount = 8 if shift_amount == 0 else shift_amount
    else:
        shift_amount = cpu.get_d(shift_amount) & 0x1F  # mod 32

    value = cpu.get_d(register_index, op_size)

    result = _shift_value(cpu, value, shift_amount, op_size, direction)

    cpu.set_d(register_index, result, op_size)

    cycles = 8 if op_size == OP_SIZE_LONG else 6
    cpu.increment_cycles(cycles + (shift_amount << 1))


def asl_asr_to_mem(cpu, direction, ea_mode, ea_register):
    """
    Arithmetic shift left/right by 1 bit to memory.

    Operation size is always Word.

    Parameters
    ----------
    direction: int
        Determines the shift direction. 0 means right, 1 means left.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the
        shifted operand.
    """
    if not ea.is_memory_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_WORD)
    value = ea_get(cpu, ea_address)

    result = _shift_value(cpu, value, 1, OP_SIZE_WORD, direction)

    ea_set(cpu, ea_address, result)

    cpu.increment_cycles(8 + ea_cycles)


def bcc(cpu, condition, offset):
    """
    Branch conditionally.

    Parameters
    ----------
    condition: int
        Value from 2 to 15 that specifies the condition on which to branch.

    offset: int
        The 8-bit signed offset of the instruction to branch to relative to
        the instruction right after the Bcc instruction.
    """
    if condition < 2:
        raise IllegalInstruction("Invalid condition %d" % condition)
    pc_base = cpu.get_pc()
    use_extension = offset == 0
    if use_extension:
        offset = int_utils.sign_extend_16_to_32(
            _load_immediate(cpu, OP_SIZE_WORD))
    else:
        offset = int_utils.sign_extend_8_to_32(offset)

    if _evaluate_condition(cpu, condition):
        cycles = 10
        cpu.set_pc(pc_base + offset)
    else:
        cycles = 12 if use_extension else 8
    cpu.increment_cycles(cycles)


def bchg(cpu, register_index, use_register, ea_mode, ea_register):
    """
    Test a bit and change it.

    Parameters
    ----------
    register_index: int
        Index of the data register that contains the bit index. If
        ``use_register`` is 0, has to be 4.

    use_register: int
        Whether to get the bit index from a data register or from an
        immediate value. If this is 1, a register is used, else the next
        instruction word is used as the immediate value.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the value to
        test.
    """
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    if not use_register:
        if register_index != 4:
            raise IllegalInstruction("register_index has to be 4")
        index = cpu.fetch_next()
    else:
        index = cpu.get_d(register_index)

    target_data_register = ea_mode == EA_MODE_REG_D
    index &= (31 if target_data_register else 7)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu,
        ea_mode, ea_register,
        OP_SIZE_LONG if target_data_register else OP_SIZE_BYTE)
    value = ea_get(cpu, ea_address)

    z_bit = not int_utils.select_bits(value, index)
    cpu.set_ccr(CCR_Z, z=z_bit)

    mask = 1 << index
    ea_set(cpu, ea_address, (value | mask) if z_bit else (value & ~mask))

    cycles = \
        (8 if use_register else 12) + (0 if target_data_register else ea_cycles)
    cpu.increment_cycles(cycles)


def bclr(cpu, register_index, use_register, ea_mode, ea_register):
    """
    Test a bit and clear it.

    Parameters
    ----------
    register_index: int
        Index of the data register that contains the bit index. If
        ``use_register`` is 0, has to be 4.

    use_register: int
        Whether to get the bit index from a data register or from an
        immediate value. If this is 1, a register is used, else the next
        instruction word is used as the immediate value.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the value to
        test.
    """
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    if not use_register:
        if register_index != 4:
            raise IllegalInstruction("register_index has to be 4")
        index = cpu.fetch_next()
    else:
        index = cpu.get_d(register_index)

    target_data_register = ea_mode == EA_MODE_REG_D
    index &= (31 if target_data_register else 7)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu,
        ea_mode, ea_register,
        OP_SIZE_LONG if target_data_register else OP_SIZE_BYTE)
    value = ea_get(cpu, ea_address)

    z_bit = not int_utils.select_bits(value, index)
    cpu.set_ccr(CCR_Z, z=z_bit)

    mask = ~(1 << index)
    ea_set(cpu, ea_address, value & mask)

    cycles = \
        (8 if use_register else 12) + (2 if target_data_register else ea_cycles)
    cpu.increment_cycles(cycles)


def bra(cpu, offset):
    """
    Branch unconditionally.

    Parameters
    ----------
    offset: int
        The 8-bit signed offset of the instruction to branch to relative to
        the instruction right after the BRA instruction.
    """
    old_pc = cpu.get_pc()
    use_extension = offset == 0
    if use_extension:
        # 16-bit extension word
        offset = int_utils.sign_extend_16_to_32(
            _load_immediate(cpu, OP_SIZE_WORD))
    else:
        offset = int_utils.sign_extend_8_to_32(offset)
    cpu.set_pc(old_pc + offset)
    cpu.increment_cycles(10)


def bset(cpu, register_index, use_register, ea_mode, ea_register):
    """
    Test a bit and set it.

    Parameters
    ----------
    register_index: int
        Index of the data register that contains the bit index. If
        ``use_register`` is 0, has to be 4.

    use_register: int
        Whether to get the bit index from a data register or from an
        immediate value. If this is 1, a register is used, else the next
        instruction word is used as the immediate value.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the value to
        test.
    """
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    if not use_register:
        if register_index != 4:
            raise IllegalInstruction("register_index has to be 4")
        index = cpu.fetch_next()
    else:
        index = cpu.get_d(register_index)

    target_data_register = ea_mode == EA_MODE_REG_D
    index &= (31 if target_data_register else 7)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu,
        ea_mode, ea_register,
        OP_SIZE_LONG if target_data_register else OP_SIZE_BYTE)
    value = ea_get(cpu, ea_address)

    z_bit = not int_utils.select_bits(value, index)
    cpu.set_ccr(CCR_Z, z=z_bit)

    mask = 1 << index
    ea_set(cpu, ea_address, value | mask)

    cycles = \
        (8 if use_register else 12) + (0 if target_data_register else ea_cycles)
    cpu.increment_cycles(cycles)


def bsr(cpu, offset):
    """
    Branch to soubroutine.

    Parameters
    ----------
    offset: int
        The 8-bit signed offset of the instruction to branch to relative to
        the instruction right after the BSR instruction.
    """
    pc_base = cpu.get_pc()  # Offset is relative to current PC

    if offset == 0:
        # Offset is in extension word
        offset = int_utils.sign_extend_16_to_32(
            _load_immediate(cpu, OP_SIZE_WORD))
    else:
        offset = int_utils.sign_extend_8_to_32(offset)

    # Push address of the next instruction after returning
    # Get PC again, since it might have changed
    cpu.push(cpu.get_pc(), OP_SIZE_LONG)

    # Jump to subroutine
    cpu.set_pc(pc_base + offset)

    cpu.increment_cycles(18)


def btst(cpu, register_index, use_register, ea_mode, ea_register):
    """
    Test a bit.

    Parameters
    ----------
    register_index: int
        Index of the data register that contains the bit index. If
        ``use_register`` is 0, has to be 4.

    use_register: int
        Whether to get the bit index from a data register or from an
        immediate value. If this is 1, a register is used, else the next
        instruction word is used as the immediate value.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the value to
        test.
    """
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    if not use_register:
        if register_index != 4:
            raise IllegalInstruction("register_index has to be 4")
        index = cpu.fetch_next()
    else:
        index = cpu.get_d(register_index)

    target_data_register = ea_mode == EA_MODE_REG_D
    index &= (31 if target_data_register else 7)

    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu,
        ea_mode, ea_register,
        OP_SIZE_LONG if target_data_register else OP_SIZE_BYTE)
    value = ea_get(cpu, ea_address)

    z_bit = not int_utils.select_bits(value, index)
    cpu.set_ccr(CCR_Z, z=z_bit)

    cycles = \
        (4 if use_register else 8) + (2 if target_data_register else ea_cycles)
    cpu.increment_cycles(cycles)


def chk(cpu, register_index, ea_mode, ea_register):
    """
    Check register against bounds, TRAP on fail.

    Parameters
    ----------
    register_index: int
        The index of the register that should be tested. Only the lower word
        is considered.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the upper bound.
    """
    if not ea.is_data(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_WORD)
    upper_bound = ea_get(cpu, ea_address)

    value = cpu.get_d(register_index, OP_SIZE_WORD)

    is_negative = bool(value & 0x8000)
    do_trap = \
        is_negative or (value > upper_bound) or bool(upper_bound & 0x8000)

    if do_trap:
        cpu.set_ccr(CCR_N, n=is_negative)
        cpu.cause_trap(6)
        cycles = 40
    else:
        cycles = 10
    cpu.increment_cycles(cycles + ea_cycles)


def clr(cpu, op_size, ea_mode, ea_register):
    """
    Clear an operand.

    Parameters
    ----------
    op_size: int
        Defines the size of the operand.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the operand.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    _, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)

    ea_set(cpu, ea_address, 0)

    if ea_mode == EA_MODE_REG_D:
        cycles = 6 if op_size == OP_SIZE_LONG else 4
    else:
        cycles = (12 if op_size == OP_SIZE_LONG else 8) + ea_cycles
    cpu.increment_cycles(cycles)


def cmp_(cpu, register_index, op_size, ea_mode, ea_register):
    """
    Compare two values by calculating 'destination - source'.

    Parameters
    ----------
    register_index: int
        Index of the data register containing the destination operand.

    op_size: int
        Defines the size of the operation.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the source
        operand.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not (ea.is_valid(ea_mode, ea_register)
            and (op_size != OP_SIZE_BYTE or ea_mode != EA_MODE_REG_A)):
        _raise_ea_error(ea_mode, ea_register)

    dst = cpu.get_d(register_index, op_size)

    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)
    src = ea_get(cpu, ea_address)

    _subtract_set_ccr(cpu, dst, src, op_size)

    cpu.increment_cycles((6 if op_size == OP_SIZE_LONG else 4) + ea_cycles)


def cmpa(cpu, register_index, op_size, ea_mode, ea_register):
    """
    Compare two values by calculating 'destination - source'.

    Parameters
    ----------
    register_index: int
        Index of the address register containing the destination operand.

    op_size: int
        Defines the size of the operation. 0 means word, 1 means long word.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the source
        operand.
    """
    if not ea.is_valid(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    dst = cpu.get_a(register_index, OP_SIZE_LONG)

    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu,
        ea_mode, ea_register,
        OP_SIZE_LONG if op_size == 1 else OP_SIZE_WORD)
    src = ea_get(cpu, ea_address)
    if op_size == 0:
        src = int_utils.sign_extend_16_to_32(src)

    _subtract_set_ccr(cpu, dst, src, OP_SIZE_LONG)

    cpu.increment_cycles(6 + ea_cycles)


def cmpi(cpu, op_size, ea_mode, ea_register):
    """
    Compare two values by calculating 'destination - immediate'.

    Parameters
    ----------
    op_size: int
        Defines the size of the operation.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the destination
        operand.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    src = _load_immediate(cpu, op_size)

    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)
    dst = ea_get(cpu, ea_address)

    _subtract_set_ccr(cpu, dst, src, OP_SIZE_LONG)

    if ea_mode == EA_MODE_REG_D:
        cycles = 14 if op_size == OP_SIZE_LONG else 8
    else:
        cycles = (12 if op_size == OP_SIZE_LONG else 8) + ea_cycles
    cpu.increment_cycles(cycles)


def cmpm(cpu, register_dst, register_src, op_size):
    """
    Compare two values from memory by calculating 'destination - source'.

    Always uses postincrement addressing mode.

    Parameters
    ----------
    register_dst, register_src: int
        Index of the address registers containing the addresses of the
        destination and source operands.

    op_size: int
        Defines the size of the operation.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    dst_get, _, dst_address, _ = ea.accessors(
        cpu, EA_MODE_A_POSTINC, register_dst, op_size)
    dst = dst_get(cpu, dst_address)

    src_get, _, src_address, _ = ea.accessors(
        cpu, EA_MODE_A_POSTINC, register_src, op_size)
    src = src_get(cpu, src_address)

    _subtract_set_ccr(cpu, dst, src, op_size)

    cpu.increment_cycles(20 if op_size == OP_SIZE_LONG else 12)


def dbcc(cpu, register_index, condition):
    """
    Test condition, decrement and branch.

    Offset to the instruction to branch to is in the extension word and is
    relative to the address it.

    Parameters
    ----------
    register_index: int
        Index of the data register that holds the counter.

    condition: int
        Value from 0 to 15 that specifies the condition that will stop the
        loop.
    """
    pc_base = cpu.get_pc()
    # Load offset now to increment the PC past it
    offset = _load_immediate(cpu, OP_SIZE_WORD)
    # Test condition
    if not _evaluate_condition(cpu, condition):
        # Decrement
        new_value = (cpu.get_d(register_index, OP_SIZE_WORD) - 1) & 0xFFFF
        cpu.set_d(register_index, new_value, OP_SIZE_WORD)
        if new_value != 0xFFFF:
            # Branch
            offset = int_utils.sign_extend_16_to_32(offset)
            cpu.set_pc(pc_base + offset)
            cycles = 10
        else:
            cycles = 14
    else:
        cycles = 12
    cpu.increment_cycles(cycles)


def divs(cpu, register_index, ea_mode, ea_register):
    """
    Signed integer division.

    Parameters
    ----------
    register_index: int
        Index of the data register containing the long word dividend.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the word-sized
        divisor.
    """
    if not ea.is_data(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_WORD)
    divisor = ea_get(cpu, ea_address)

    if divisor == 0:
        cpu.cause_trap(5)
        cpu.increment_cycles(38)
        return

    dividend = cpu.get_d(register_index, OP_SIZE_LONG)

    neg_divisor = bool(divisor & 0x8000)
    neg_dividend = bool(dividend & 0x80000000)
    is_positive = neg_divisor == neg_dividend

    # Make both positive
    if neg_divisor:
        divisor = (~divisor + 1) & 0xFFFF
    if neg_dividend:
        dividend = (~dividend + 1) & 0xFFFFFFFF

    quotient = dividend // divisor
    # Check if the quotient fits into a 16-bit signed integer
    if (quotient & 0xFFFF8000) == 0:
        remainder = dividend % divisor
        # Remainder has the same sign as the dividend
        if neg_dividend:
            remainder = (~remainder + 1) & 0xFFFF
        # Potentially negate the result
        if not is_positive:
            quotient = (~quotient + 1) & 0xFFFF

        # Set the result
        cpu.set_d(register_index, (remainder << 16) | quotient, OP_SIZE_LONG)
        # Set ccr
        cpu.set_ccr(CCR_ALL ^ CCR_X,
                    n=not is_positive,
                    z=not quotient,
                    v=False,
                    c=False)
    else:
        cpu.set_ccr(CCR_V | CCR_C, v=True, c=False)

    cpu.increment_cycles(158 + ea_cycles)


def divu(cpu, register_index, ea_mode, ea_register):
    """
    Unsigned integer division.

    Parameters
    ----------
    register_index: int
        Index of the data register containing the long word dividend.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the word-sized
        divisor.
    """
    if not ea.is_data(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_WORD)
    divisor = ea_get(cpu, ea_address)

    if divisor == 0:
        cpu.cause_trap(5)
        cpu.increment_cycles(38)
        return

    dividend = cpu.get_d(register_index, OP_SIZE_LONG)

    quotient = dividend // divisor
    # Check if the quotient fits into a 16-bit signed integer
    if (quotient & 0xFFFF0000) == 0:
        remainder = dividend % divisor

        # Set the result
        cpu.set_d(register_index, (remainder << 16) | quotient, OP_SIZE_LONG)
        # Set ccr
        cpu.set_ccr(CCR_ALL ^ CCR_X,
                    n=bool(quotient & 0x8000),
                    z=not quotient,
                    v=False,
                    c=False)
    else:
        cpu.set_ccr(CCR_V | CCR_C, v=True, c=False)

    cpu.increment_cycles(140 + ea_cycles)


def eor(cpu, register_index, op_size, ea_mode, ea_register):
    """
    Build exlusive-or of two values.

    Parameters
    ----------
    register_index: int
        Index of the data register containing the source operand.

    op_size: int
        Defines the size of the operation.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the destination
        operand.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)
    v0 = ea_get(cpu, ea_address)
    v1 = cpu.get_d(register_index, op_size)

    # Mask for the relevant bits of the result
    mask, msb_mask = _bit_masks(op_size)

    result = (v0 ^ v1) & mask

    # Set CCR
    result_msb = result & msb_mask
    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(result_msb),
                z=not result,
                v=False,
                c=False)

    ea_set(cpu, ea_address, result)

    cycles = 8 if op_size == OP_SIZE_LONG else 4
    if ea_mode != EA_MODE_REG_D:
        cycles += 4 + ea_cycles
    cpu.increment_cycles(cycles)


def eori(cpu, op_size, ea_mode, ea_register):
    """
    Build exlusive-or with an immediate value.

    Parameters
    ----------
    op_size: int
        Defines the size of the operation.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the destination
        operand.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    v0 = _load_immediate(cpu, op_size)
    mask, msb_mask = _bit_masks(op_size)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)

    result = (v0 ^ ea_get(cpu, ea_address)) & mask

    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(result & msb_mask),
                z=not result,
                v=False,
                c=False)

    ea_set(cpu, ea_address, result)

    if ea_mode < 2:
        cycles = 16 if op_size == OP_SIZE_LONG else 8
    else:
        cycles = (20 if op_size == OP_SIZE_LONG else 12) + ea_cycles
    cpu.increment_cycles(cycles)


def eori_to_ccr(cpu):
    """
    Build exlusive-or with an immediate value and CCR.

    The immediate value is always 8-bit and located in the next instruction
    word.
    """
    value = cpu.get_sr_full() ^ _load_immediate(cpu, OP_SIZE_WORD)
    cpu.set_ccr(CCR_ALL,
                int_utils.select_bits(value, 4),
                int_utils.select_bits(value, 3),
                int_utils.select_bits(value, 2),
                int_utils.select_bits(value, 1),
                int_utils.select_bits(value, 0))
    cpu.increment_cycles(20)


def eori_to_sr(cpu):
    """
    Build exclusive-or with status register.

    Priviliged instruction. Takes the next instruction word as the second
    operand. Only affects the bits of the status register, that are not
    constant.
    """
    if not cpu.get_s():
        raise PrivilegeError()
    value = cpu.get_sr_full() ^ _load_immediate(cpu, OP_SIZE_WORD)
    cpu.set_ccr(CCR_ALL,
                int_utils.select_bits(value, 4),
                int_utils.select_bits(value, 3),
                int_utils.select_bits(value, 2),
                int_utils.select_bits(value, 1),
                int_utils.select_bits(value, 0))
    cpu.set_sr(SR_ALL,
               int_utils.select_bits(value, 15),
               int_utils.select_bits(value, 13),
               int_utils.select_bits(value, 8, 10))
    cpu.increment_cycles(20)


def exg(cpu, register_x, register_y, op_type):
    """
    Exchange registers.

    Parameters
    ----------
    register_x, register_y: int
        Indices of the registers to exchange. When changing data and
        address registers, ``register_x`` is the index of the data
        register.

    op_type: int
        Value that describes what registers to exchange.
        8 means data to data, 9 means address to address, 17 means data to
        address.
    """
    if op_type not in (8, 9, 17):
        raise IllegalInstruction("EXG invalid op_type")
    if op_type == 8:
        v0 = cpu.get_d(register_x, OP_SIZE_LONG)
        v1 = cpu.get_d(register_y, OP_SIZE_LONG)
        cpu.set_d(register_x, v1, OP_SIZE_LONG)
        cpu.set_d(register_y, v0, OP_SIZE_LONG)
    elif op_type == 9:
        v0 = cpu.get_a(register_x, OP_SIZE_LONG)
        v1 = cpu.get_a(register_y, OP_SIZE_LONG)
        cpu.set_a(register_x, v1)
        cpu.set_a(register_y, v0)
    else:
        v0 = cpu.get_d(register_x, OP_SIZE_LONG)
        v1 = cpu.get_a(register_y, OP_SIZE_LONG)
        cpu.set_d(register_x, v1, OP_SIZE_LONG)
        cpu.set_a(register_y, v0)
    cpu.increment_cycles(6)


def ext(cpu, register_index, op_size):
    """
    Sign-extend a register.

    Parameters
    ----------
    register_index: int
        Index of the register containing the value to sign-extend.

    op_size: int
        Whether to extend from byte to word (0) or from word to long word
        (1).
    """
    is_word_to_long = op_size == 1
    value = cpu.get_d(register_index,
                      OP_SIZE_WORD if is_word_to_long else OP_SIZE_BYTE)
    result = \
        int_utils.sign_extend_16_to_32(value) \
        if is_word_to_long \
        else int_utils.sign_extend_8_to_16(value)

    size = OP_SIZE_LONG if is_word_to_long else OP_SIZE_WORD
    cpu.set_d(register_index, result, size)

    msb_mask = _bit_masks(size)[1]
    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(result & msb_mask),
                z=not result,
                v=0, c=0)

    cpu.increment_cycles(4)


def illegal(cpu):
    """Force the illegal instruction TRAP."""
    cpu.cause_trap(4)
    cpu.increment_cycles(34)


def jmp(cpu, ea_mode, ea_register):
    """
    Jump to an instruction.

    Parameters
    ----------
    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the instruction
        address.
    """
    if not ea.is_control(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    ea_address = ea.accessors(cpu, ea_mode, ea_register, OP_SIZE_LONG)[2]
    cpu.set_pc(ea_address)

    if ea_mode == EA_MODE_A_INDIRECT:
        cycles = 8
    elif ea_mode == EA_MODE_A_DISP:
        cycles = 10
    elif ea_mode == EA_MODE_A_INDX:
        cycles = 14
    # ea_mode == EA_MODE_OTHER
    elif ea_register == EA_REGISTER_ABS_WORD:
        cycles = 10
    elif ea_register == EA_REGISTER_ABS_LONG:
        cycles = 12
    elif ea_register == EA_REGISTER_PC_DISP:
        cycles = 10
    else:  # ea_register == EA_REGISTER_PC_DISP
        cycles = 14
    cpu.increment_cycles(cycles)


def jsr(cpu, ea_mode, ea_register):
    """
    Jump to subroutine.

    Parameters
    ----------
    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the subroutine
        address.
    """
    if not ea.is_control(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    ea_address = ea.accessors(cpu, ea_mode, ea_register, OP_SIZE_LONG)[2]
    cpu.push(cpu.get_pc(), OP_SIZE_LONG)
    cpu.set_pc(ea_address)

    if ea_mode == EA_MODE_A_INDIRECT:
        cycles = 16
    elif ea_mode == EA_MODE_A_DISP:
        cycles = 18
    elif ea_mode == EA_MODE_A_INDX:
        cycles = 22
    # ea_mode == EA_MODE_OTHER
    elif ea_register == EA_REGISTER_ABS_WORD:
        cycles = 18
    elif ea_register == EA_REGISTER_ABS_LONG:
        cycles = 20
    elif ea_register == EA_REGISTER_PC_DISP:
        cycles = 18
    else:  # ea_register == EA_REGISTER_PC_DISP
        cycles = 22
    cpu.increment_cycles(cycles)


def lea(cpu, register_index, ea_mode, ea_register):
    """
    Load effective address.

    Parameters
    ----------
    register_index: int
        Index of the address register to load the address into.

    ea_mode, ea_register: int
        Define the address that will be loaded.
    """
    if not ea.is_control(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    _, _, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_LONG)
    cpu.set_a(register_index, ea_address)

    extra_cycles = \
        2 if (ea_mode == EA_MODE_A_INDX
              or (ea_mode == EA_MODE_OTHER
                  and ea_register == EA_REGISTER_PC_INDX)) \
        else 0
    cpu.increment_cycles(ea_cycles + extra_cycles - 4)


def link(cpu, register_index):
    """
    Link and allocate.

    Parameters
    ----------
    register_index: int
        Index of the register to save on the stack and then contain the current
        stack pointer.
    """
    # Push address register
    cpu.push(cpu.get_a(register_index), OP_SIZE_LONG)
    # Save current stack pointer
    stack_pointer = cpu.get_a(7)
    cpu.set_a(register_index, stack_pointer)
    # Load the offset from the extension word
    offset = int_utils.sign_extend_16_to_32(_load_immediate(cpu, OP_SIZE_WORD))
    cpu.set_a(7, stack_pointer + offset)

    cpu.increment_cycles(16)


def lsl_lsr_to_data(
        cpu, register_index, shift_amount, op_type, op_size, direction):
    """
    Logical shift left/right to data register.

    Parameters
    ----------
    register_index: int
        The index of the data register to shift.

    shift_amount: int
        Amount of bits to shift by (value 0 means a shift by 8) if
        ``op_type == 0``, else index of the register containing that
        amount (is taken modulo 32 before).

    op_type: int
        Whether ``shift_amount`` is a value (0) or a register index (1).

    op_size: int
        Defines the size of the shifted operand.

    direction: int
        Determines the shift direction. 0 means right, 1 means left.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    # Get shift amount
    if op_type == 0:
        shift_amount = 8 if shift_amount == 0 else shift_amount
    else:
        shift_amount = cpu.get_d(shift_amount) & 0x1F  # mod 32

    value = cpu.get_d(register_index, op_size)

    result = _shift_value(
        cpu, value, shift_amount, op_size, direction, is_arith=False)

    cpu.set_d(register_index, result, op_size)

    cycles = 8 if op_size == OP_SIZE_LONG else 6
    cpu.increment_cycles(cycles + (shift_amount << 1))


def lsl_lsr_to_mem(cpu, direction, ea_mode, ea_register):
    """
    Logical shift left/right by 1 bit to memory.

    Operation size is always Word.

    Parameters
    ----------
    direction: int
        Determines the shift direction. 0 means right, 1 means left.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the
        shifted operand.
    """
    if not ea.is_memory_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_WORD)
    value = ea_get(cpu, ea_address)

    result = _shift_value(
        cpu, value, 1, OP_SIZE_WORD, direction, is_arith=False)

    ea_set(cpu, ea_address, result)

    cpu.increment_cycles(8 + ea_cycles)


def move(cpu, dst_mode, dst_register, src_mode, src_register, op_size):
    """
    Move a value from source to destination.

    dst_mode, dst_register, src_mode, src_register: int
        Effective address mode and register for the source and destination
        operands.

    op_size: int
        Size of the operation. ``1`` means Byte, ``3`` means Word and ``2``
        means Long Word.
    """
    if op_size == 0:
        raise IllegalInstruction()
    if not (ea.is_valid(src_mode, src_register)
            and (op_size != 1 or src_mode != EA_MODE_REG_A)):
        _raise_ea_error(src_mode, src_register)
    if not ea.is_data_alterable(dst_mode, dst_register):
        _raise_ea_error(dst_mode, dst_register)

    # Convert to normal values for op_size
    if op_size == 1:
        op_size = OP_SIZE_BYTE
    elif op_size == 2:
        op_size = OP_SIZE_LONG
    else:
        op_size = OP_SIZE_WORD

    # Resolve effective addresses
    src_get, _, src_address, src_cycles = ea.accessors(
        cpu, src_mode, src_register, op_size)
    _, dst_set, dst_address, dst_cycles = ea.accessors(
        cpu, dst_mode, dst_register, op_size)

    # Move value
    value = src_get(cpu, src_address)
    dst_set(cpu, dst_address, value)

    # Set CCR
    msb_mask = _bit_masks(op_size)[1]
    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(value & msb_mask),
                z=not(value),
                v=0, c=0)

    # Set cycles
    cpu.increment_cycles(
        4 + dst_cycles + src_cycles
        - (2 if dst_mode == EA_MODE_A_PREDEC else 0))


def movea(cpu, dst_register, src_mode, src_register, op_size):
    """
    Move a value from source to destination address register.

    dst_register: int
        Index of the destination address register.

    src_mode, src_address: int
        Effective address mode and register for the source operands.

    op_size: int
        Size of the operation. ``1`` means Byte, ``3`` means Word and ``2``
        means Long Word.
    """
    if op_size < 2:
        raise IllegalInstruction()
    if not ea.is_valid(src_mode, src_register):
        _raise_ea_error(src_mode, src_register)

    # Convert to normal values for op_size
    elif op_size == 2:
        op_size = OP_SIZE_LONG
    else:
        op_size = OP_SIZE_WORD

    # Resolve effective addresses
    src_get, _, src_address, src_cycles = ea.accessors(
        cpu, src_mode, src_register, op_size)

    # Move value
    value = src_get(cpu, src_address)
    if op_size == OP_SIZE_WORD:
        value = int_utils.sign_extend_16_to_32(value)
    cpu.set_a(dst_register, value)

    # Set cycles
    cpu.increment_cycles(4 + src_cycles)


def move_to_ccr(cpu, ea_mode, ea_register):
    """
    Move a value to CCR.

    Parameters
    ----------
    ea_mode, ea_register: int
        Define the effective address of the source operand.
    """
    if not ea.is_data(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_WORD)

    value = ea_get(cpu, ea_address)

    cpu.set_ccr(CCR_ALL,
                x=bool(value & CCR_X),
                n=bool(value & CCR_N),
                z=bool(value & CCR_Z),
                v=bool(value & CCR_V),
                c=bool(value & CCR_C))

    cpu.increment_cycles(12 + ea_cycles)


def move_from_sr(cpu, ea_mode, ea_register):
    """
    Move a value from SR.

    Parameters
    ----------
    ea_mode, ea_register: int
        Define the effective address of the destination operand. Size is always
        word.
    """
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    _, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_WORD)

    ea_set(cpu, ea_address, cpu.get_sr_full())

    cpu.increment_cycles((8 + ea_cycles) if ea_mode != EA_MODE_REG_D else 6)


def move_to_sr(cpu, ea_mode, ea_register):
    """
    Move to status register.

    Priviliged instruction. Only affects the bits of the status register,
    that are not constant.
    """
    if not cpu.get_s():
        raise PrivilegeError()
    if not ea.is_data(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_WORD)
    value = ea_get(cpu, ea_address)
    cpu.set_ccr(CCR_ALL,
                int_utils.select_bits(value, 4),
                int_utils.select_bits(value, 3),
                int_utils.select_bits(value, 2),
                int_utils.select_bits(value, 1),
                int_utils.select_bits(value, 0))
    cpu.set_sr(SR_ALL,
               int_utils.select_bits(value, 15),
               int_utils.select_bits(value, 13),
               int_utils.select_bits(value, 8, 10))
    cpu.increment_cycles(12 + ea_cycles)


def move_usp(cpu, register_index, direction):
    """
    Move the user stack pointer.

    Priviliged instruction.

    Parameters
    ----------
    register_index: int
        Index of the address register to use.

    direction: int
        If this is ``0``, the content of the address register with index
        ``register_index`` will be moved to the USP register. Otherwise, the
        USP value will be moved to the address register.
    """
    if not cpu.get_s():
        raise PrivilegeError()

    if direction == 0:
        cpu.set_usp(cpu.get_a(register_index))
    else:
        cpu.set_a(register_index, cpu.get_usp())
    cpu.increment_cycles(4)


def movem(cpu, direction, op_size, ea_mode, ea_register):
    """
    Move multiple registers.

    Parameters
    ----------
    direction: int
        Whether to transfer registers to memory (0) or memory to registers (1).

    op_size: int
        Size of the operation. ``0`` means Word, ``1`` means Long Word.

    ea_mode, ea_register: int
        Define the address of the start location for the transfer.
    """
    if not ((ea.is_control(ea_mode, ea_register)
             and ea.is_alterable(ea_mode, ea_register))
            or (ea_mode == EA_MODE_OTHER and ea_register < 2)
            # Predecrement mode is allowed for register-to-memory
            or (direction == 0 and ea_mode == EA_MODE_A_PREDEC)
            # Postincrement mode is allowed for memory-to-register
            or (direction == 1 and ea_mode == EA_MODE_A_POSTINC)):
        _raise_ea_error(ea_mode, ea_register)

    mask = cpu.fetch_next()
    offset = 2 * (op_size + 1)
    amount = 0
    is_special_mode = \
        ea_mode == EA_MODE_A_POSTINC \
        or ea_mode == EA_MODE_A_PREDEC
    # Mask for the register mask
    mask_mask = 1  # lol
    # Adjust 'op_size' to be like in most other instructions
    op_size = OP_SIZE_LONG if op_size == 1 else OP_SIZE_WORD

    if is_special_mode:
        base_address = cpu.get_a(ea_register)
        ea_cycles = 8 if op_size == OP_SIZE_LONG else 4
    else:
        _, _, base_address, ea_cycles = ea.accessors(
            cpu, ea_mode, ea_register, op_size)

    if direction == 0:
        # Register to memory
        for mask_index in range(16):
            mask_bit = mask & mask_mask
            mask_mask = mask_mask << 1
            if mask_bit:
                amount += 1

                # Get the register value
                if is_special_mode:
                    # Predecrement mode. Uses inverted mask bits
                    base_address -= offset
                    if mask_index < 8:
                        value = cpu.get_a(7 - mask_index)
                    else:
                        value = cpu.get_d(15 - mask_index, OP_SIZE_LONG)
                else:
                    # Normal mode
                    if mask_index < 8:
                        value = cpu.get_d(mask_index, OP_SIZE_LONG)
                    else:
                        value = cpu.get_a(mask_index - 8)

                # 'value' contains Long value to write
                if op_size == OP_SIZE_WORD:
                    # Only write lower word
                    # Is truncated automatically
                    cpu.mem.write(base_address, value)
                else:
                    cpu.mem.write(base_address, value >> 16)
                    cpu.mem.write(base_address + 2, value)

                if not is_special_mode:
                    # Increment base now
                    base_address += offset
    else:
        # Memory to register
        for mask_index in range(16):
            mask_bit = mask & mask_mask
            mask_mask = mask_mask << 1
            if mask_bit:
                amount += 1

                # Get the memory value
                first = cpu.mem.read(base_address)
                if op_size == OP_SIZE_WORD:
                    value = int_utils.sign_extend_16_to_32(first)
                else:
                    value = (first << 16) | cpu.mem.read(base_address + 2)

                # 'value' contains the Long Word to write
                if mask_index < 8:
                    cpu.set_d(mask_index, value, OP_SIZE_LONG)
                else:
                    cpu.set_a(mask_index - 8, value)

                base_address += offset

    if op_size == OP_SIZE_LONG:
        cycles_base = amount * 8
    else:
        cycles_base = amount * 4 + 4
    if direction == 1:
        cycles_base += 4
    cpu.increment_cycles(cycles_base + ea_cycles)

    if is_special_mode:
        # Write the last base address to the register
        cpu.set_a(ea_register, base_address)


def movep(cpu, data_register, address_register, direction, op_size):
    """
    Move peripheral data.

    Parameters
    ----------
    data_register, address_register: int
        Indices of the data and address registers to use. Always uses address
        register indirect with displacement addressing mode.

    direction: int
        Whether to write to (1) or from (0) memory.

    op_size: int
        Whether to write Long Word (1) or Word (0).
    """
    displacement = int_utils.sign_extend_16_to_32(cpu.fetch_next())
    base_address = (cpu.get_a(address_register) + displacement) & 0xFFFFFFFF
    if direction == 0:
        # Memory to register
        # Read the next two values, only consider the upper byte
        value = \
            (cpu.mem.read(base_address) & 0xFF00) \
            | (cpu.mem.read(base_address + 2) >> 8)
        if op_size == 1:
            # Read 2 more values. The ones before are the upper word
            value = (value << 16) |\
                (cpu.mem.read(base_address + 4) & 0xFF00) \
                | (cpu.mem.read(base_address + 6) >> 8)

        cpu.set_d(data_register,
                  value,
                  OP_SIZE_LONG if op_size == 1 else OP_SIZE_WORD)
    else:
        # Register to memory
        value = cpu.get_d(data_register, OP_SIZE_LONG)
        if op_size == 1:
            # First write the upper word
            original = cpu.mem.read(base_address)
            cpu.mem.write(
                base_address,
                (original & 0xFF) | ((value >> 16) & 0xFF00))
            original = cpu.mem.read(base_address + 2)
            cpu.mem.write(
                base_address + 2,
                (original & 0xFF) | ((value >> 8) & 0xFF00))
            # Change the base address so that the next step writes to the
            # correct position
            base_address = base_address + 4

        # Write the registers lower word
        original = cpu.mem.read(base_address)
        cpu.mem.write(
            base_address,
            (original & 0xFF) | (value & 0xFF00))
        original = cpu.mem.read(base_address + 2)
        cpu.mem.write(
            base_address + 2,
            (original & 0xFF) | ((value << 8) & 0xFF00))

    cpu.increment_cycles(24 if op_size == 1 else 16)


def moveq(cpu, register_index, value):
    """
    Move quick.

    Parameters
    ----------
    register_index: int
        Index of the data register to move the value to.

    value: int
        8-bit signed integer to move into the data register with the given
        index.
    """
    cpu.set_d(register_index,
              int_utils.sign_extend_8_to_32(value),
              OP_SIZE_LONG)
    cpu.increment_cycles(4)


def muls(cpu, register_index, ea_mode, ea_register):
    """
    Signed multiply.

    Parameters
    ----------
    register_index: int
        Index of the destination data register. Only the lower word is
        considered for the multiplication, but all 32-bits are written with the
        result.

    ea_mode, ea_register: int
        Define the effective address of the source operand word.
    """
    if not ea.is_data(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    v0 = cpu.get_d(register_index, OP_SIZE_WORD)
    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_WORD)
    v1 = ea_get(cpu, ea_address)

    result = (int_utils.sign_extend_16_to_32(v0)
              * int_utils.sign_extend_16_to_32(v1)) & 0xFFFFFFFF
    cpu.set_d(register_index, result, OP_SIZE_LONG)

    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(result & 0x80000000),
                z=not result,
                v=0, c=0)  # Overflow cannot occur

    # Amount of cycles = 38 + 2*n
    # let x = v1 << 1
    # n = amount of "01"s or "10"s in x

    # We iterate over each bit in v1.
    # matcher_xx is 'True' when the last bit matched the pattern so far
    # 'matcher_10' starts as 'True' since we append a '0' to v1 from the right.
    matcher_01 = False
    matcher_10 = True

    amount_01 = 0
    amount_10 = 0

    for _ in range(16):
        bit_value = v1 & 1
        v1 = v1 >> 1
        if matcher_01 and not bit_value:
            # Found a "01" pattern
            amount_01 += 1
        elif matcher_10 and bit_value:
            # Found a "10" pattern
            amount_10 += 1
        # Set the matchers for the next loop
        matcher_01 = bool(bit_value)
        matcher_10 = not bit_value

    cpu.increment_cycles(38 + 2 * (amount_01 + amount_10) + ea_cycles)


def mulu(cpu, register_index, ea_mode, ea_register):
    """
    Signed multiply.

    Parameters
    ----------
    register_index: int
        Index of the destination data register. Only the lower word is
        considered for the multiplication, but all 32-bits are written with the
        result.

    ea_mode, ea_register: int
        Define the effective address of the source operand word.
    """
    if not ea.is_data(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    v0 = cpu.get_d(register_index, OP_SIZE_WORD)
    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_WORD)
    v1 = ea_get(cpu, ea_address)

    result = v0 * v1
    cpu.set_d(register_index, result, OP_SIZE_LONG)

    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(result & 0x80000000),
                z=not result,
                v=0, c=0)  # Overflow cannot occur

    # Amount of cycles = 38 + 2*n
    # n = amount of "1"s in v1
    amount_1s = 0
    for _ in range(16):
        bit_value = v1 & 1
        v1 = v1 >> 1
        if bit_value:
            amount_1s += 1

    cpu.increment_cycles(38 + 2 * amount_1s + ea_cycles)


def nbcd(cpu, ea_mode, ea_register):
    """
    Negate decimal with extend.

    Parameters
    ----------
    ea_mode, ea_register: int
        The effective address of the operand to negate.
    """
    # TODO rework algorithm
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_BYTE)
    value = ea_get(cpu, ea_address)
    # We assume that 'value' is a valid BCD
    dec_value = (value & 0xF) + ((value >> 4) * 10)
    result_raw = 99 - dec_value  # 9s complement
    result_10 = result_raw & 0xFF
    if not cpu.get_x():
        # 10s complement
        result_10 += 1
    # Convert back to BCD
    first_digit = result_10 % 10
    second_digit = ((result_10 - first_digit) // 10)
    if second_digit > 9:
        second_digit = 0
    result = first_digit | (second_digit << 4)

    ea_set(cpu, ea_address, result)

    # Set CCR
    ccr_mask = CCR_X | CCR_C
    c_bit = value != 0
    if result:
        ccr_mask |= CCR_Z
    cpu.set_ccr(ccr_mask, x=c_bit, z=0, c=c_bit)

    cpu.increment_cycles(6 if ea_mode == EA_MODE_REG_D else (8 + ea_cycles))


def neg(cpu, op_size, ea_mode, ea_register):
    """
    Negate an integer.

    Parameters
    ----------
    op_size: int
        The size of the operation.

    ea_mode, ea_register: int
        Define the effective address of the target operand.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)
    value = ea_get(cpu, ea_address)

    msb_mask = _bit_masks(op_size)[1]
    if value == msb_mask:
        # Overflow
        v_bit = True
        result = value
    else:
        v_bit = False
        result = ~value + 1

    ea_set(cpu, ea_address, result)

    c_bit = bool(result)
    cpu.set_ccr(CCR_ALL,
                x=c_bit,
                n=bool(result & msb_mask),
                z=not c_bit,
                v=v_bit,
                c=c_bit)

    if ea_mode == EA_MODE_REG_D:
        cycles = 6 if op_size == OP_SIZE_LONG else 4
    else:
        cycles = (12 if op_size == OP_SIZE_LONG else 8) + ea_cycles
    cpu.increment_cycles(cycles)


def negx(cpu, op_size, ea_mode, ea_register):
    """
    Negate an integer with extend.

    Parameters
    ----------
    op_size: int
        The size of the operation.

    ea_mode, ea_register: int
        Define the effective address of the target operand.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)
    value = ea_get(cpu, ea_address)
    x_value = cpu.get_x()

    mask, msb_mask = _bit_masks(op_size)
    if value == msb_mask and not x_value:
        # Overflow
        v_bit = True
        result = value
    else:
        v_bit = False
        result = (~(value + x_value) + 1) & mask

    ea_set(cpu, ea_address, result)

    c_bit = bool(result)
    ccr_mask = CCR_ALL
    # Do not change Z if the result is 0, else set it to False
    if not c_bit:
        ccr_mask = ccr_mask ^ CCR_Z
    cpu.set_ccr(ccr_mask,
                x=c_bit,
                n=bool(result & msb_mask),
                z=False,
                v=v_bit,
                c=c_bit)

    if ea_mode == EA_MODE_REG_D:
        cycles = 6 if op_size == OP_SIZE_LONG else 4
    else:
        cycles = (12 if op_size == OP_SIZE_LONG else 8) + ea_cycles
    cpu.increment_cycles(cycles)


def nop(cpu):
    """Do nothing."""
    cpu.increment_cycles(4)


def not_(cpu, op_size, ea_mode, ea_register):
    """
    Logical negation.

    Parameters
    ----------
    op_size: int
        The size of the operation.

    ea_mode, ea_register: int
        Define the effective address of the target operand.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)

    mask, msb_mask = _bit_masks(op_size)

    result = ~ea_get(cpu, ea_address) & mask
    ea_set(cpu, ea_address, result)

    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(result & msb_mask),
                z=not result,
                v=0,
                c=0)

    if ea_mode == EA_MODE_REG_D:
        cycles = 6 if op_size == OP_SIZE_LONG else 4
    else:
        cycles = (12 if op_size == OP_SIZE_LONG else 8) + ea_cycles
    cpu.increment_cycles(cycles)


def or_(cpu, register_index, op_type, op_size, ea_mode, ea_register):
    """
    Build logical disjunction of two values.

    Parameters
    ----------
    register_index: int
        Value from 0 to 7 that indicates the register index for either the
        source (``op_type == 1``) or the destination (``op_type == 0``).

    op_type: int
        Determines whether the effective address and the register are
        source or destination. 0 means register is the destination, 1 means
        register is the source.

    op_size: int
        Defines the size of the operands.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    # When writing to effective address, only memory mode is valid
    write_to_ea = (op_type == 1)
    if not ((write_to_ea and ea.is_memory_alterable(ea_mode, ea_register))
             or (not write_to_ea and ea.is_data(ea_mode, ea_register))):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, ea_set, address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)
    v0 = ea_get(cpu, address)
    v1 = cpu.get_d(register_index, op_size)

    # Mask for the relevant bits of the result
    mask, msb_mask = _bit_masks(op_size)

    result = (v0 | v1) & mask

    # Set CCR
    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(result & msb_mask),
                z=not result,
                v=False,
                c=False)

    _binary_op_write_result(cpu,
                            result,
                            op_size,
                            register_index,
                            address,
                            write_to_ea,
                            ea_mode, ea_set, ea_cycles)


def ori(cpu, op_size, ea_mode, ea_register):
    """
    Build logical disjunction with an immediate value.

    Parameters
    ----------
    op_size: int
        Defines the size of the operation.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the destination
        operand.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    v0 = _load_immediate(cpu, op_size)
    mask, msb_mask = _bit_masks(op_size)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)

    result = (v0 | ea_get(cpu, ea_address)) & mask

    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(result & msb_mask),
                z=not result,
                v=False,
                c=False)

    ea_set(cpu, ea_address, result)

    if ea_mode < 2:
        cycles = 16 if op_size == OP_SIZE_LONG else 8
    else:
        cycles = (20 if op_size == OP_SIZE_LONG else 12) + ea_cycles
    cpu.increment_cycles(cycles)


def ori_to_ccr(cpu):
    """
    Build logical disjunction with an immediate value and CCR.

    The immediate value is always 8-bit and located in the next instruction
    word.
    """
    value = cpu.get_sr_full() | _load_immediate(cpu, OP_SIZE_WORD)
    cpu.set_ccr(CCR_ALL,
                int_utils.select_bits(value, 4),
                int_utils.select_bits(value, 3),
                int_utils.select_bits(value, 2),
                int_utils.select_bits(value, 1),
                int_utils.select_bits(value, 0))
    cpu.increment_cycles(20)


def ori_to_sr(cpu):
    """
    Build logical disjunction with status register.

    Priviliged instruction. Takes the next instruction word as the second
    operand. Only affects the bits of the status register, that are not
    constant.
    """
    if not cpu.get_s():
        raise PrivilegeError()
    value = cpu.get_sr_full() | _load_immediate(cpu, OP_SIZE_WORD)
    cpu.set_ccr(CCR_ALL,
                int_utils.select_bits(value, 4),
                int_utils.select_bits(value, 3),
                int_utils.select_bits(value, 2),
                int_utils.select_bits(value, 1),
                int_utils.select_bits(value, 0))
    cpu.set_sr(SR_ALL,
               int_utils.select_bits(value, 15),
               int_utils.select_bits(value, 13),
               int_utils.select_bits(value, 8, 10))
    cpu.increment_cycles(20)


def pea(cpu, ea_mode, ea_register):
    """
    Push effective address.

    Parameters
    ----------
    ea_mode, ea_register: int
        Define the effective address to push onto the stack.
    """
    if not ea.is_control(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    _, _, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_LONG)
    cpu.push(ea_address, OP_SIZE_LONG)
    extra_cycles = \
        2 if (ea_mode == EA_MODE_A_INDX
              or (ea_mode == EA_MODE_OTHER
                  and ea_register == EA_REGISTER_PC_INDX)) \
        else 0
    cpu.increment_cycles(ea_cycles + 4 + extra_cycles)


def reset(cpu):
    """Reset external devices."""
    # Does not do anything
    cpu.increment_cycles(132)


def rol_ror_to_data(
        cpu, register_index, rotate_amount, op_type, op_size, direction):
    """
    Rotate to data register.

    Parameters
    ----------
    register_index: int
        Index of the data register to rotate.

    rotate_amount: int
        Amount of bits to rotate (0 means an amount of 8) if ``op_type == 0``
        or the index of the data register that contains the amount of bits to
        rotate (taken modulo 64 before).

    op_type: int
        Determines whether ``rotate_amount`` is the amount of bits to rotate
        (0) or the index of the data register that contains it (1).

    op_size: int
        The size of the operation.

    direction: int
        Whether to rotate right (0) or left (1).
    """
    if op_size == 0b11:
        raise IllegalInstruction()

    if op_type == 0:
        rotate_amount = 8 if rotate_amount == 0 else rotate_amount
    else:
        # Amount is supposed to be taken modulo 64, but this will leave us with
        # a multiple of the register size.
        # This way, we keep the contract and still guarantee, that
        # rotate_amount is not larger than it should be.
        # Same as 'amount % bit_amount'
        bit_amount = 32 if op_size == OP_SIZE_LONG else (8 + 8*op_size)
        rotate_amount = cpu.get_d(rotate_amount) & (bit_amount - 1)

    value = cpu.get_d(register_index, op_size)

    result = _rotate_value(cpu, value, rotate_amount, op_size, direction)

    cpu.set_d(register_index, result, op_size)
    cpu.increment_cycles(
        (8 if op_size == OP_SIZE_LONG else 6) + 2 * rotate_amount)


def rol_ror_to_mem(cpu, direction, ea_mode, ea_register):
    """
    Rotate to memory.

    Parameters
    ----------
    direction: int
        Whether to rotate right (0) or left (1).

    ea_mode, ea_register: int
        Define the effective address of the value to rotate by 1 bit.
    """
    if not ea.is_memory_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_WORD)
    value = ea_get(cpu, ea_address)

    result = _rotate_value(cpu, value, 1, OP_SIZE_WORD, direction)

    ea_set(cpu, ea_address, result)

    cpu.increment_cycles(8 + ea_cycles)


def roxl_roxr_to_data(
        cpu, register_index, rotate_amount, op_type, op_size, direction):
    """
    Rotate to data register with extend.

    Parameters
    ----------
    register_index: int
        Index of the data register to rotate.

    rotate_amount: int
        Amount of bits to rotate (0 means an amount of 8) if ``op_type == 0``
        or the index of the data register that contains the amount of bits to
        rotate (taken modulo 64 before).

    op_type: int
        Determines whether ``rotate_amount`` is the amount of bits to rotate
        (0) or the index of the data register that contains it (1).

    op_size: int
        The size of the operation.

    direction: int
        Whether to rotate right (0) or left (1).
    """
    if op_size == 0b11:
        raise IllegalInstruction()

    if op_type == 0:
        rotate_amount = 8 if rotate_amount == 0 else rotate_amount
    else:
        # Amount is supposed to be taken modulo 64, but this will leave us with
        # a multiple of the register size.
        # This way, we keep the contract and still guarantee, that
        # rotate_amount is not larger than it should be.
        # Same as 'amount % bit_amount'
        bit_amount = 32 if op_size == OP_SIZE_LONG else (8 + 8*op_size)
        rotate_amount = cpu.get_d(rotate_amount) & (bit_amount - 1)

    value = cpu.get_d(register_index, op_size)

    result = _rotate_value_extend(
        cpu, value, rotate_amount, op_size, direction)

    cpu.set_d(register_index, result, op_size)
    cpu.increment_cycles(
        (8 if op_size == OP_SIZE_LONG else 6) + 2 * rotate_amount)


def roxl_roxr_to_mem(cpu, direction, ea_mode, ea_register):
    """
    Rotate to memory with extend.

    Parameters
    ----------
    direction: int
        Whether to rotate right (0) or left (1).

    ea_mode, ea_register: int
        Define the effective address of the value to rotate by 1 bit.
    """
    if not ea.is_memory_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_WORD)
    value = ea_get(cpu, ea_address)

    result = _rotate_value_extend(cpu, value, 1, OP_SIZE_WORD, direction)

    ea_set(cpu, ea_address, result)

    cpu.increment_cycles(8 + ea_cycles)


def rte(cpu):
    """Return from exception."""
    if not cpu.get_s():
        raise PrivilegeError("RTE")

    status_register = cpu.pop()
    new_pc = cpu.pop(OP_SIZE_LONG)

    cpu.set_pc(new_pc)

    cpu.set_ccr(CCR_ALL,
                int_utils.select_bits(status_register, 4),
                int_utils.select_bits(status_register, 3),
                int_utils.select_bits(status_register, 2),
                int_utils.select_bits(status_register, 1),
                int_utils.select_bits(status_register, 0))
    cpu.set_sr(SR_ALL,
               int_utils.select_bits(status_register, 15),
               int_utils.select_bits(status_register, 13),
               int_utils.select_bits(status_register, 8, 10))

    cpu.increment_cycles(20)


def rtr(cpu):
    """Return and restore."""
    status_register = cpu.pop()
    new_pc = cpu.pop(OP_SIZE_LONG)

    cpu.set_pc(new_pc)

    cpu.set_ccr(CCR_ALL,
                int_utils.select_bits(status_register, 4),
                int_utils.select_bits(status_register, 3),
                int_utils.select_bits(status_register, 2),
                int_utils.select_bits(status_register, 1),
                int_utils.select_bits(status_register, 0))

    cpu.increment_cycles(20)


def rts(cpu):
    """Return from subroutine."""
    new_pc = cpu.pop(OP_SIZE_LONG)

    cpu.set_pc(new_pc)

    cpu.increment_cycles(16)


def sbcd(cpu, register_dst, register_src, op_type):
    """
    Subtract decimal with extend bit.

    Always subtracts source from destination (destination - source - X).

    Parameters
    ----------
    register_dst, register_src: int
        Indices of the source and destination registers. If ``op_size == 0``,
        these are data registers that contain the operands. Otherwise, they are
        address registers which will be used with predecrement addressing mode
        to reference the operands in memory.

    op_type: int
        Whether the register indices are for data registers (0) or for address
        registers, that will be used with predecrement addressing (1).
    """
    use_memory = op_type == 1
    ea_mode = EA_MODE_A_PREDEC if use_memory else EA_MODE_REG_D

    src_get, _, src_address, _ = ea.accessors(
        cpu, ea_mode, register_src, OP_SIZE_BYTE)
    dst_get, dst_set, dst_address, _ = ea.accessors(
        cpu, ea_mode, register_dst, OP_SIZE_BYTE)

    src = src_get(cpu, src_address)
    dst = dst_get(cpu, dst_address)

    src_dec = 10 * ((src & 0xF0) >> 4) + (src & 0xF)
    dst_dec = 10 * ((dst & 0xF0) >> 4) + (dst & 0xF)
    result_dec = dst_dec - src_dec - cpu.get_x()
    if result_dec < 0:
        result_dec += 100

    first_digit = result_dec % 10
    second_digit = (result_dec - first_digit) // 10
    result = (second_digit << 4) | first_digit

    dst_set(cpu, dst_address, result)

    # Set CCR
    c_bit = src_dec > dst_dec
    ccr_mask = CCR_ALL
    if not result:
        ccr_mask = ccr_mask ^ CCR_Z
    cpu.set_ccr(ccr_mask, x=c_bit, z=False, c=c_bit)

    cpu.increment_cycles(18 if use_memory else 6)


def scc(cpu, condition, ea_mode, ea_register):
    """
    Set conditionally.

    Parameters
    ----------
    condition: int
        The code of the condition to check.

    ea_mode, ea_register: int
        Define the effective address of the value to set.
    """
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    value = 0xFF if _evaluate_condition(cpu, condition) else 0
    _, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_BYTE)
    ea_set(cpu, ea_address, value)

    cpu.increment_cycles(
        (6 if value else 4)
        if ea_mode == EA_MODE_REG_D
        else (8 + ea_cycles))


def stop(cpu):
    """Stop execution of instructions."""
    if not cpu.get_s():
        raise PrivilegeError("STOP")
    status_register = cpu.fetch_next()

    cpu.set_ccr(CCR_ALL,
                int_utils.select_bits(status_register, 4),
                int_utils.select_bits(status_register, 3),
                int_utils.select_bits(status_register, 2),
                int_utils.select_bits(status_register, 1),
                int_utils.select_bits(status_register, 0))
    cpu.set_sr(SR_ALL,
               int_utils.select_bits(status_register, 15),
               int_utils.select_bits(status_register, 13),
               int_utils.select_bits(status_register, 8, 10))

    cpu.set_stopped()
    cpu.increment_cycles(4)


def sub(cpu, register_index, op_type, op_size, ea_mode, ea_register):
    """
    Subtract two values.

    Always calculates destination - source.

    Parameters
    ----------
    register_index: int
        Value from 0 to 7 that indicates the register index for either the
        source (``op_type == 1``) or the destination (``op_type == 0``).

    op_type: int
        Determines whether the effective address and the register are
        source or destination. 0 means register is the destination, 1 means
        register is the source.

    op_size: int
        Defines the size of the operands.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    # When writing to effective address, only memory mode is valid
    write_to_ea = (op_type == 1)
    if not ((write_to_ea and ea.is_memory_alterable(ea_mode, ea_register))
             or (not write_to_ea and 
                 (ea.is_valid(ea_mode, ea_register)
                  and (op_size != OP_SIZE_BYTE
                       or ea_mode != EA_MODE_REG_A)))):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)
    v0 = ea_get(cpu, ea_address)
    v1 = cpu.get_d(register_index, op_size)

    dst, src = (v0, v1) if write_to_ea else (v1, v0)

    result = _subtract_set_ccr(cpu, dst, src, op_size, set_x=True)

    _binary_op_write_result(cpu,
                            result,
                            op_size,
                            register_index,
                            ea_address,
                            write_to_ea,
                            ea_mode, ea_set, ea_cycles)


def suba(cpu, register_index, op_size, ea_mode, ea_register):
    """
    Subtract from address register.

    Parameters
    ----------
    register_index: int
        Index of the address register to subtract from.

    op_size: int
        0 for word-sized source operand with sign-extension, else long
        word.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the source.
    """
    # All valid effective address modes are allowed
    if not ea.is_valid(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    is_word_op = op_size == 0
    ea_get, _, ea_address, ea_cycles = ea.accessors(
        cpu,
        ea_mode, ea_register,
        OP_SIZE_WORD if is_word_op else OP_SIZE_LONG)
    src = ea_get(cpu, ea_address)

    if is_word_op:
        src = int_utils.sign_extend_16_to_32(src)

    dst = cpu.get_a(register_index)

    result = dst - src

    cpu.set_a(register_index, result)

    # Increment cycle
    if is_word_op:
        cycles = 8
    else:
        # Needs 2 more cycles if effective address is register direct or
        # immediate
        extra_cycles = \
            2 if (ea_mode < 2
                  or (ea_mode == EA_MODE_OTHER
                      and ea_register == EA_REGISTER_IMMEDIATE)) \
            else 0
        cycles = 6 + extra_cycles
    # Cycles for effective address calculation are always added on top
    cpu.increment_cycles(cycles + ea_cycles)


def subi(cpu, op_size, ea_mode, ea_register):
    """
    Subtract immediate.

    Parameters
    ----------
    op_size:
        Defines the size of the immediate and destination operands.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the
        destination.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    # Read the immediate operand before resolving the effective address!
    v0 = _load_immediate(cpu, op_size)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)
    v1 = ea_get(cpu, ea_address)

    result = _subtract_set_ccr(cpu, v1, v0, op_size, set_x=True)

    ea_set(cpu, ea_address, result)

    cycles = 16 if op_size == OP_SIZE_LONG else 8
    if ea_mode != EA_MODE_REG_D:
        cycles += 4
    cpu.increment_cycles(cycles + ea_cycles)


def subq(cpu, value, op_size, ea_mode, ea_register):
    """
    Subtract quick.

    Parameters
    ----------
    value: int
        Value to add to the destination. 0 means to add 8.

    op_size:
        Defines the size of the destination operand, if it is not address
        register direct, in which case it is always long word.

    ea_mode, ea_register: int
        Values from 0 to 7. Define the effective address of the
        destination.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ((ea.is_alterable(ea_mode, ea_register)
             or (ea_mode == EA_MODE_OTHER and ea_register < 2))
            and (op_size != OP_SIZE_BYTE or ea_mode != EA_MODE_REG_A)):
        _raise_ea_error(ea_mode, ea_register)

    to_address = ea_mode == EA_MODE_REG_A
    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_LONG if to_address else op_size)

    v0 = ea_get(cpu, ea_address)
    v1 = 8 if value == 0 else value

    if to_address:
        result = v0 - v1
    else:
        result = _subtract_set_ccr(cpu, v0, v1, op_size, set_x=True)

    ea_set(cpu, ea_address, result)

    # Set cycles
    if ea_mode < 2:
        cycles = 8 if (op_size == OP_SIZE_LONG) or to_address else 4
    else:
        cycles = (12 if op_size == OP_SIZE_LONG else 8) + ea_cycles
    cpu.increment_cycles(cycles)


def subx(cpu, register_dst, register_src, op_type, op_size):
    """
    Add with extend bit.

    Parameters
    ----------
    register_src, register_dst: int
        Index of the source and destination registers.

    op_type: int
        If 0, the register indices are for data registers, else they are
        for address registers that will be dereferenced with predecrement
        addressing mode.

    op_size: int
        Defines the size of the operands.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    use_address = op_type == 1
    if use_address:
        ea_mode = EA_MODE_A_PREDEC
    else:
        ea_mode = EA_MODE_REG_D

    dst_get, dst_set, dst_address, _ = ea.accessors(
        cpu, ea_mode, register_dst, op_size)
    src_get, _, src_address, _ = ea.accessors(
        cpu, ea_mode, register_src, op_size)

    dst = dst_get(cpu, dst_address)
    src = src_get(cpu, src_address) + cpu.get_x()

    result = _subtract_set_ccr(cpu, dst, src, op_size, set_x=True, always_set_z=False)

    dst_set(cpu, dst_address, result)

    # Write result
    if use_address:
        cycles = 30 if op_size == OP_SIZE_LONG else 18
    else:
        cycles = 8 if op_size == OP_SIZE_LONG else 4
    cpu.increment_cycles(cycles)


def swap(cpu, register_index):
    """
    Swap register halves.

    Parameters
    ----------
    register_index: int
        The index of the register to swap halves in.
    """
    value = cpu.get_d(register_index, OP_SIZE_LONG)
    result = (value >> 16) | ((value & 0xFFFF) << 16)
    cpu.set_d(register_index, result, OP_SIZE_LONG)

    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=bool(0x80000000 & result),
                z=not result,
                v=False, x=False)

    cpu.increment_cycles(4)


def tas(cpu, ea_mode, ea_register):
    """
    Test and set a value.

    Parameters
    ----------
    ea_mode, ea_register: int
        Define the effective address of the value to test and set.
    """
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)
    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, OP_SIZE_BYTE)
    value = ea_get(cpu, ea_address)

    n_bit = bool(value & 0x80)
    if not n_bit:
        ea_set(cpu, ea_address, value | 0x80)

    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=n_bit,
                z=not value,
                v=False, c=False)

    cpu.increment_cycles(4 if ea_mode == EA_MODE_REG_D else (14 + ea_cycles))


def trap(cpu, vector_number):
    """
    Cause a trap.

    Parameters
    ----------
    vector_number: int
        Value from 0 to 7 that indicates which TRAP to execute.
    """
    cpu.cause_trap(32 + vector_number)
    cpu.increment_cycles(34)


def trapv(cpu):
    """Cause a trap on overflow."""
    if cpu.get_v():
        cpu.cause_trap(7)
        cycles = 34
    else:
        cycles = 4
    cpu.increment_cycles(cycles)


def tst(cpu, op_size, ea_mode, ea_register):
    """
    Test a value.

    Parameters
    ----------
    op_size: int
        The size of the operation.

    ea_mode, ea_register: int
        Define the effective address of the value to test.
    """
    if op_size == 0b11:
        raise IllegalInstruction()
    if not ea.is_data_alterable(ea_mode, ea_register):
        _raise_ea_error(ea_mode, ea_register)

    ea_get, ea_set, ea_address, ea_cycles = ea.accessors(
        cpu, ea_mode, ea_register, op_size)
    value = ea_get(cpu, ea_address)

    mask, msb_mask = _bit_masks(op_size)
    n_bit = bool(value & msb_mask)

    cpu.set_ccr(CCR_ALL ^ CCR_X,
                n=n_bit,
                z=not (value & mask),
                v=False, c=False)

    cpu.increment_cycles(4  + ea_cycles)


def unlk(cpu, register_index):
    """
    Unlink.

    Parameters
    ----------
    register_index: int
        The address register that contains the address of the stack to use.
        The top of that stack will be pop-ed into it.
    """
    stack_pointer = cpu.get_a(register_index)
    if register_index != 7:
        cpu.set_a(7, stack_pointer)
    cpu.set_a(register_index, cpu.pop(OP_SIZE_LONG))
    cpu.increment_cycles(12)
