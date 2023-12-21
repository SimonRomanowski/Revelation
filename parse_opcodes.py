import sys
import os


OP_SIZE_BYTE = 0
OP_SIZE_WORD = 1
OP_SIZE_LONG = 2

EA_MODE_REG_D = 0
EA_MODE_REG_A = 1
EA_MODE_A_INDIRECT = 2
EA_MODE_A_POSTINC = 3
EA_MODE_A_PREDEC = 4
EA_MODE_A_DISP = 5
EA_MODE_A_INDX = 6
EA_MODE_OTHER = 7

EA_REGISTER_ABS_WORD = 0
EA_REGISTER_ABS_LONG = 1
EA_REGISTER_PC_DISP = 2
EA_REGISTER_PC_INDX = 3
EA_REGISTER_IMMEDIATE = 4

_CONDITION_STRS = (
    "T ",  # 0
    "F ",  # 1
    "HI",  # 2
    "LS",  # 3
    "CC",  # 4
    "LO",  # 5
    "NE",  # 6
    "EQ",  # 7
    "VC",  # 8
    "VS",  # 9
    "PL",  # 10
    "MI",  # 11
    "GE",  # 12
    "LT",  # 13
    "GT",  # 14
    "LE",  # 15
)


class WordList:

    def __init__(self, it):
        self._bytes = tuple(it)

    def __iter__(self):
        for i in range(0, len(self._bytes), 2):
            yield self.__getitem__(i)

    def __getitem__(self, key):
        upper = self._bytes[key] << 8
        lower = self._bytes[key + 1] if (key + 1) < len(self._bytes) else 0
        return upper | lower

    def __len__(self):
        return len(self._bytes)


class Instruction:
    """
    An instruction for the M68000 CPU.

    Parameters
    ----------
    raw_str: str
        The string representation of this instruction.
        It may contain placeholders (in '{}'-style syntax) that will be filled
        with the names of label referenced in this instruction (using
        ``str.format``).

    size: int
        The length of this instruction in bytes.
        Has to be an even, positive number.

    labels: tuple[int], optional
        Sequence of instruction addresses (=labels) that are referenced by this
        instruction. Their names will later be added to the full string
        representation.
        Default is the empty tuple.

    Notes
    -----
    To convert this instruction to a string, one should use the ``get_str``
    method (instead of ``__str__`` or the ``str`` function).
    """

    def __init__(self, raw_str, size, labels=()):
        assert isinstance(raw_str, str)
        assert isinstance(size, int)
        assert not (size & 1)
        assert size > 0
        assert isinstance(labels, tuple)
        self._raw_str = raw_str
        self._size = size
        self._labels = labels

    def get_size(self):
        """Get the length of this instruction in bytes."""
        return self._size

    def get_labels(self):
        """Get all instruction addresses referenced by this instruction."""
        return self._labels

    def get_str(self, label_strs=()):
        """
        Create a string representation for this instruction.

        Parameters
        ----------
        label_strs: tuple[str], optional
            A tuple of label names of the same size and order as the one
            returned by ``get_labels``.
            Default is the empty tuple.

        Raises
        ------
        ValueError
            If ``label_strs`` does not have the right size.
        """
        if len(label_strs) != len(self._labels):
            raise ValueError("Wrong amount of labels passed")
        return self._raw_str.format(*label_strs)


def _parse_instruction(prog, address):
    op_code = prog[address]
    upper_bits = (op_code & 0xF000) >> 12

    if upper_bits == 0:
        ins, is_end = _parse_bit_movep_imm(prog, address, op_code)
    elif upper_bits < 4:
        ins, is_end = _parse_move(prog, address, op_code)
    elif upper_bits == 4:
        ins, is_end = _parse_misc(prog, address, op_code)
    elif upper_bits == 5:
        ins, is_end = _parse_quick_scc_dbcc(prog, address, op_code)
    elif upper_bits == 6:
        ins, is_end = _parse_branch(prog, address, op_code)
    elif upper_bits == 7:
        ins, is_end = _parse_moveq(prog, address, op_code)
    elif upper_bits == 8:
        ins, is_end = _parse_or_div_sbcd(prog, address, op_code)
    elif upper_bits == 9:
        ins, is_end = _parse_sub(prog, address, op_code)
    elif upper_bits == 0xB:
        ins, is_end = _parse_cmp_eor(prog, address, op_code)
    elif upper_bits == 0xC:
        ins, is_end = _parse_and_mul_abcd_exg(prog, address, op_code)
    elif upper_bits == 0xD:
        ins, is_end = _parse_add(prog, address, op_code)
    elif upper_bits == 0xE:
        ins, is_end = _parse_shift_rotate(prog, address, op_code)
    else:
        ins = _invalid_instruction()
        is_end = True
    return ins, is_end


def _parse_bit_movep_imm(prog, address, op_code):
    """Bit manipulation, MOVEP and Immediate instructions."""
    is_end = False
    ea_mode, ea_register = _ea_split(
        _select_bits(op_code, 0, 5))
    upper_byte = _select_bits(op_code, 8, 15)
    bits_6_15 = _select_bits(op_code, 6, 15)
    bits_6_8 = _select_bits(op_code, 6, 8)
    is_data_alterable = _ea_is_data_alterable(ea_mode, ea_register)

    if op_code == 0x3C:
        # ORI to CCR
        imm_text = _parse_imm(prog, address + 2, OP_SIZE_BYTE)[0]
        ins = Instruction("ORI {}, CCR".format(imm_text), 4)

    elif op_code == 0x7C:
        # ORI to SR
        imm_text = _parse_imm(prog, address + 2, OP_SIZE_WORD)[0]
        ins = Instruction("ORI {}, SR".format(imm_text), 4)

    elif upper_byte == 0 and is_data_alterable:
        # ORI
        op_size = _select_bits(op_code, 6, 7)
        imm_text, imm_bytes = _parse_imm(prog, address + 2, op_size)
        ea_text, ea_bytes = _parse_ea(prog,
                                      address + imm_bytes,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        size_text = _size_str(op_size)
        ins = Instruction("ORI{} {}, {}".format(size_text, imm_text, ea_text),
                          2 + imm_bytes + ea_bytes)

    elif op_code == 0x23C:
        # ANDI to CCR
        imm_text = _parse_imm(prog, address + 2, OP_SIZE_BYTE)[0]
        ins = Instruction("ANDI {}, CCR".format(imm_text), 4)

    elif op_code == 0x27C:
        # ANDI to SR
        imm_text = _parse_imm(prog, address + 2, OP_SIZE_WORD)[0]
        ins = Instruction("ANDI {}, SR".format(imm_text), 4)

    elif upper_byte == 2 and is_data_alterable:
        # ANDI
        op_size = _select_bits(op_code, 6, 7)
        imm_text, imm_bytes = _parse_imm(prog, address + 2, op_size)
        ea_text, ea_bytes = _parse_ea(prog,
                                      address + imm_bytes,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        size_text = _size_str(op_size)
        ins = Instruction("ANDI{} {}, {}".format(size_text, imm_text, ea_text),
                          2 + imm_bytes + ea_bytes)

    elif upper_byte == 4 and is_data_alterable:
        # SUBI
        op_size = _select_bits(op_code, 6, 7)
        imm_text, imm_bytes = _parse_imm(prog, address + 2, op_size)
        ea_text, ea_bytes = _parse_ea(prog,
                                      address + imm_bytes,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        size_text = _size_str(op_size)
        ins = Instruction("SUBI{} {}, {}".format(size_text, imm_text, ea_text),
                          2 + imm_bytes + ea_bytes)

    elif upper_byte == 6 and is_data_alterable:
        # ADDI
        op_size = _select_bits(op_code, 6, 7)
        imm_text, imm_bytes = _parse_imm(prog, address + 2, op_size)
        ea_text, ea_bytes = _parse_ea(prog,
                                      address + imm_bytes,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        size_text = _size_str(op_size)
        ins = Instruction("ADDI{} {}, {}".format(size_text, imm_text, ea_text),
                          2 + imm_bytes + ea_bytes)

    elif op_code == 0xA3C:
        # EORI to CCR
        imm_text = _parse_imm(prog, address + 2, OP_SIZE_WORD)[0]
        ins = Instruction("EORI {}, CCR".format(imm_text), 4)

    elif op_code == 0xA7C:
        # EORI to SR
        imm_text = _parse_imm(prog, address + 2, OP_SIZE_WORD)[0]
        ins = Instruction("EORI {}, SR".format(imm_text), 4)

    elif upper_byte == 0xA and is_data_alterable:
        # EORI
        op_size = _select_bits(op_code, 6, 7)
        imm_text, imm_bytes = _parse_imm(prog, address + 2, op_size)
        ea_text, ea_bytes = _parse_ea(prog,
                                      address + imm_bytes,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        size_text = _size_str(op_size)
        ins = Instruction("EORI{} {}, {}".format(size_text, imm_text, ea_text),
                          2 + imm_bytes + ea_bytes)

    elif upper_byte == 0xC and is_data_alterable:
        # CMPI
        op_size = _select_bits(op_code, 6, 7)
        imm_text, imm_bytes = _parse_imm(prog, address + 2, op_size)
        ea_text, ea_bytes = _parse_ea(prog,
                                      address + imm_bytes,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        size_text = _size_str(op_size)
        ins = Instruction("CMPI{} {}, {}".format(size_text, imm_text, ea_text),
                          2 + imm_bytes + ea_bytes)

    elif is_data_alterable and (bits_6_8 == 4 or bits_6_15 == 0x20):
        # BTST
        op_size = OP_SIZE_LONG if ea_mode == EA_MODE_REG_D else OP_SIZE_BYTE
        if upper_byte & 1:
            # With register
            first_value = "D{}".format(_select_bits(op_code, 9, 11))
            offset = 0
        else:
            # With immediate
            first_value, offset = _parse_imm(prog, address + 2, op_size)
        ea_text, ea_bytes = _parse_ea(prog,
                                      address + offset,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        ins = Instruction("BTST {}, {}".format(first_value, ea_text),
                          2 + offset + ea_bytes)

    elif is_data_alterable and (bits_6_8 == 5 or bits_6_15 == 0x21):
        # BCHG
        op_size = OP_SIZE_LONG if ea_mode == EA_MODE_REG_D else OP_SIZE_BYTE
        if upper_byte & 1:
            # With register
            first_value = "D{}".format(_select_bits(op_code, 9, 11))
            offset = 0
        else:
            # With immediate
            first_value, offset = _parse_imm(prog, address + 2, op_size)
        ea_text, ea_bytes = _parse_ea(prog,
                                      address + offset,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        ins = Instruction("BCHG {}, {}".format(first_value, ea_text),
                          2 + offset + ea_bytes)

    elif is_data_alterable and (bits_6_8 == 6 or bits_6_15 == 0x22):
        # BCLR
        op_size = OP_SIZE_LONG if ea_mode == EA_MODE_REG_D else OP_SIZE_BYTE
        if upper_byte & 1:
            # With register
            first_value = "D{}".format(_select_bits(op_code, 9, 11))
            offset = 0
        else:
            # With immediate
            first_value, offset = _parse_imm(prog, address + 2, op_size)
        ea_text, ea_bytes = _parse_ea(prog,
                                      address + offset,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        ins = Instruction("BCLR {}, {}".format(first_value, ea_text),
                          2 + offset + ea_bytes)

    elif is_data_alterable and (bits_6_8 == 7 or bits_6_15 == 0x23):
        # BSET
        op_size = OP_SIZE_LONG if ea_mode == EA_MODE_REG_D else OP_SIZE_BYTE
        if upper_byte & 1:
            # With register
            first_value = "D{}".format(_select_bits(op_code, 9, 11))
            offset = 0
        else:
            # With immediate
            first_value, offset = _parse_imm(prog, address + 2, op_size)
        ea_text, ea_bytes = _parse_ea(prog,
                                      address + offset,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        ins = Instruction("BSET {}, {}".format(first_value, ea_text),
                          2 + offset + ea_bytes)

    elif ea_mode == 1 and _select_bits(op_code, 8) == 1:
        # MOVEP
        displacement = _parse_ea(prog,
                                 address,
                                 EA_MODE_A_DISP,
                                 ea_register,
                                 OP_SIZE_WORD)
        d_register = "D{}".format(_select_bits(op_code, 9, 11))
        if (bits_6_8 >> 1) & 1:
            # Register to memory
            first_value = d_register
            second_value = displacement
        else:
            # Memory to register
            first_value = displacement
            second_value = d_register
        ins = Instruction("MOVEP {}, {}".format(first_value, second_value), 4)

    else:
        ins = _invalid_instruction()
        is_end = True

    return ins, is_end


def _parse_move(prog, address, op_code):
    """MOVE instructions."""
    is_end = False
    size = op_code >> 12
    src_mode, src_register = _ea_split(op_code)
    # Order is swapped here!
    dst_register, dst_mode = _ea_split(op_code >> 6)
    src_valid = _ea_is_valid(src_mode, src_register)

    if src_valid and _ea_is_data_alterable(dst_mode, dst_register):
        # MOVE
        if size == 1:
            op_size = OP_SIZE_BYTE
        elif size == 3:
            op_size = OP_SIZE_WORD
        else:
            op_size = OP_SIZE_LONG
        src_text, src_bytes = _parse_ea(prog,
                                        address,
                                        src_mode,
                                        src_register,
                                        op_size)
        dst_text, dst_bytes = _parse_ea(prog,
                                        address + src_bytes,
                                        dst_mode,
                                        dst_register,
                                        op_size)
        size_text = _size_str(op_size)
        ins = Instruction("MOVE{} {}, {}".format(size_text,
                                                 src_text,
                                                 dst_text),
                          2 + src_bytes + dst_bytes)

    elif src_valid and dst_mode == EA_MODE_REG_A and size != 1:
        # MOVEA
        op_size = OP_SIZE_WORD if size == 3 else OP_SIZE_LONG
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      src_mode,
                                      src_register,
                                      op_size)
        size_text = _size_str(op_size)
        ins = Instruction("MOVEA{} {}, A{}".format(size_text,
                                                   ea_text,
                                                   dst_register),
                          2 + ea_bytes)

    else:
        ins = _invalid_instruction()
        is_end = True

    return ins, is_end


def _parse_misc(prog, address, op_code):
    """Execute various instructions."""
    is_end = False
    bits_6_11 = _select_bits(op_code, 6, 11)
    bits_6_7 = bits_6_11 & 3
    bits_6_8 = bits_6_11 & 7
    bits_8_11 = _select_bits(op_code, 8, 11)

    ea_mode, ea_register = _ea_split(op_code)
    is_data_alterable = _ea_is_data_alterable(ea_mode, ea_register)
    is_data = _ea_is_data(ea_mode, ea_register)
    is_control = _ea_is_control(ea_mode, ea_register)
    is_valid = _ea_is_valid(ea_mode, ea_register)

    if bits_6_11 == 3 and is_data_alterable:
        # MOVE from SR
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      OP_SIZE_WORD)
        ins = Instruction("MOVE {}, SR".format(ea_text),
                          2 + ea_bytes)

    elif bits_6_7 != 3 and bits_8_11 == 0 and is_data_alterable:
        # NEGX
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      bits_6_7)
        size_text = _size_str(bits_6_7)
        ins = Instruction("NEGX{} {}".format(size_text, ea_text),
                          2 + ea_bytes)

    elif bits_6_7 != 3 and bits_8_11 == 2 and is_data_alterable:
        # CLR
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      bits_6_7)
        size_text = _size_str(bits_6_7)
        ins = Instruction("CLR{} {}".format(size_text, ea_text),
                          2 + ea_bytes)

    elif bits_6_11 == 0x13 and is_data:
        # MOVE to CCR
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      OP_SIZE_WORD)
        ins = Instruction("MOVE {}, CCR".format(ea_text),
                          2 + ea_bytes)

    elif bits_6_7 != 3 and bits_8_11 == 4 and is_data_alterable:
        # NEG
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      bits_6_7)
        size_text = _size_str(bits_6_7)
        ins = Instruction("NEG{} {}".format(size_text, ea_text),
                          2 + ea_bytes)

    elif bits_6_7 != 3 and bits_8_11 == 6 and is_data_alterable:
        # NOT
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      bits_6_7)
        size_text = _size_str(bits_6_7)
        ins = Instruction("NOT{} {}".format(size_text, ea_text),
                          2 + ea_bytes)

    elif bits_6_11 == 0x1B and is_data:
        # MOVE to SR
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      OP_SIZE_WORD)
        ins = Instruction("MOVE {}, SR".format(ea_text), 2 + ea_bytes)

    elif ea_mode == 0 and (bits_6_11 == 0x22 or bits_6_11 == 0x23):
        # EXT
        op_size = OP_SIZE_LONG if bits_6_11 & 1 else OP_SIZE_WORD
        size_text = _size_str(op_size)
        ins = Instruction("EXT{} D{}".format(size_text, ea_register), 2)

    elif bits_6_11 == 0x20 and is_data_alterable:
        # NBCD
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      OP_SIZE_BYTE)
        ins = Instruction("NBCD {}".format(ea_text), 2 + ea_bytes)

    elif ea_mode == 0 and bits_6_11 == 0x21:
        # SWAP
        ins = Instruction("SWAP D{}".format(ea_register), 2)

    elif is_control and bits_6_11 == 0x21:
        # PEA
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      OP_SIZE_LONG)
        ins = Instruction("PEA {}".format(ea_text), 2 + ea_bytes)

    elif op_code == 0x4AFC:
        # ILLEGAL
        ins = Instruction("ILLEGAL  ; Intentional ILLEGAL", 2)

    elif is_data_alterable and bits_6_11 == 0x2B:
        # TAS
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      OP_SIZE_BYTE)
        ins = Instruction("TAS {}".format(ea_text), 2 + ea_bytes)

    elif bits_6_7 != 3 and bits_8_11 == 0xA and is_valid:
        # TST
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      bits_6_7)
        size_text = _size_str(bits_6_7)
        ins = Instruction("TST{} {}".format(size_text, ea_text), 2 + ea_bytes)

    elif ea_mode < 2 and bits_6_11 == 0x39:
        # TRAP
        vector = "#0x{:X}".format(_select_bits(op_code, 0, 3))
        ins = Instruction("TRAP {}".format(vector), 2)

    elif ea_mode == 2 and bits_6_11 == 0x39:
        # LINK
        imm_text = _parse_imm(prog, address + 2, OP_SIZE_WORD)[0]
        ins = Instruction("LINK A{}, {}".format(ea_register, imm_text), 4)

    elif ea_mode == 3 and bits_6_11 == 0x39:
        # UNLK
        ins = Instruction("UNLK A{}".format(ea_register), 2)

    elif (ea_mode == 4 or ea_mode == 5) and bits_6_11 == 0x39:
        # MOVE USP
        a_register = "A{}".format(ea_register)
        if ea_mode & 1:
            src_text = "USP"
            dst_text = a_register
        else:
            src_text = a_register
            dst_text = "USP"
        ins = Instruction("MOVE {}, {}".format(src_text, dst_text), 2)

    elif op_code == 0x4E70:
        # RESET
        ins = Instruction("RESET", 2)

    elif op_code == 0x4E71:
        # NOP
        ins = Instruction("NOP", 2)

    elif op_code == 0x4E72:
        # STOP
        imm_text = _parse_imm(prog, address + 2, OP_SIZE_WORD)[0]
        ins = Instruction("STOP {}".format(imm_text), 4)

    elif op_code == 0x4E73:
        # RTE
        ins = Instruction("RTE", 2)
        is_end = True  # Is return

    elif op_code == 0x4E75:
        # RTS
        ins = Instruction("RTS", 2)
        is_end = True  # Is return

    elif op_code == 0x4E76:
        # TRAPV
        ins = Instruction("TRAPV", 2)

    elif op_code == 0x4E77:
        # RTR
        ins = Instruction("RTR", 2)
        is_end = True  # Is return

    elif is_control and bits_6_11 == 0x3A:
        # JSR
        if ea_mode < 7 or ea_register == 3:
            # Variable jump
            ea_text, ea_bytes = _parse_ea(prog,
                                          address,
                                          ea_mode,
                                          ea_register,
                                          OP_SIZE_WORD)  # Does not matter
            ins = Instruction("JSR {}".format(ea_text), 2 + ea_bytes)
        else:
            # Static jump
            if ea_register == 0:
                # (xxx).W
                label = prog[address + 2]
                offset = 2
            elif ea_register == 1:
                # (xxx).L
                label = _read_dword(prog, address + 2)
                offset = 4
            else:
                # (d16, PC) = relative jump
                label = address + 2 + prog[address + 2]
                offset = 2
            labels = (label,)
            # Format label later
            ins = Instruction("JSR {}", 2 + offset, labels)

    elif is_control and bits_6_11 == 0x3B:
        # JMP
        if ea_mode < 7 or ea_register == 3:
            # Variable jump
            ea_text, ea_bytes = _parse_ea(prog,
                                          address,
                                          ea_mode,
                                          ea_register,
                                          OP_SIZE_WORD)  # Does not matter
            ins = Instruction("JMP {}".format(ea_text), 2 + ea_bytes)
        else:
            # Static jump
            if ea_register == 0:
                # (xxx).W
                label = prog[address + 2]
                offset = 2
            elif ea_register == 1:
                # (xxx).L
                label = _read_dword(prog, address + 2)
                offset = 4
            else:
                # (d16, PC) = relative jump
                label = address + 2 + prog[address + 2]
                offset = 2
            labels = (label,)
            # Format label later
            ins = Instruction("JMP {}", 2 + offset, labels)
            is_end = True  # Unconditional jump without return

    elif (ea_mode > 1 and (ea_mode != 7 or ea_register < 2)) \
            and _select_bits(op_code, 11) == 1 \
            and _select_bits(op_code, 7, 9) == 1:
        # MOVEM
        is_reversed = ea_mode == 4
        register_mask = prog[address + 2]
        is_first = True
        register_text = ""
        shift_range = range(15, -1, -1) if is_reversed else range(16)
        # This will *not* join nicely with '-'
        for shift in shift_range:
            mask = 0x8000 >> shift
            if is_reversed:
                register_name = ("A" if shift >= 8 else "D") + str(shift % 8)
            else:
                register_name = \
                    ("A" if shift < 8 else "D") \
                    + str(7 - (shift % 8))
            if register_mask & mask:
                if not is_first:
                    register_text += "/"
                else:
                    is_first = False
                register_text += register_name

        op_size = OP_SIZE_LONG if bits_6_7 & 1 else OP_SIZE_WORD
        ea_text, ea_bytes = _parse_ea(prog,
                                      address + 2,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        size_text = _size_str(op_size)

        if _select_bits(op_code, 10):
            src_text = ea_text
            dst_text = register_text
        else:
            src_text = register_text
            dst_text = ea_text

        ins = Instruction("MOVEM{} {}, {}".format(size_text,
                                                  src_text,
                                                  dst_text),
                          4 + ea_bytes)

    elif is_control and bits_6_8 == 7:
        # LEA
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      OP_SIZE_LONG)
        ins = Instruction("LEA {}, A{}".format(ea_text, bits_8_11 >> 1),
                          2 + ea_bytes)

    elif is_data and bits_6_8 == 6:
        # CHK
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      OP_SIZE_WORD)
        ins = Instruction("CHK {}, D{}".format(ea_text, bits_8_11 >> 1),
                          2 + ea_bytes)

    else:
        ins = _invalid_instruction()
        is_end = True

    return ins, is_end


def _parse_quick_scc_dbcc(prog, address, op_code):
    """ADDQ, SUBQ, Scc or DBcc."""
    is_end = False
    op_size = _select_bits(op_code, 6, 7)
    ea_mode, ea_register = _ea_split(_select_bits(op_code, 0, 5))
    if op_size == 3:
        if ea_mode == EA_MODE_REG_A:
            # DBcc
            displacement = prog[address + 2]
            if displacement & 0x8000:
                # Sign-extension
                displacement = displacement - 0x10000
            labels = (address + 2 + displacement,)
            condition_str = _parse_condition(_select_bits(op_code, 8, 11))
            ins = Instruction("DB{} D{},".format(condition_str, ea_register)
                              + " {}",
                              4,
                              labels)

        else:
            # Scc
            ea_text, ea_bytes = _parse_ea(prog,
                                          address,
                                          ea_mode,
                                          ea_register,
                                          OP_SIZE_BYTE)
            condition_str = _parse_condition(_select_bits(op_code, 8, 11))
            ins = Instruction("S{} {}".format(condition_str, ea_text),
                              2 + ea_bytes)

    else:
        data = _select_bits(op_code, 9, 11)
        data_text = "#{}".format(8 if data == 0 else data)
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        size_text = _size_str(op_size)
        if _select_bits(op_code, 8) == 0:
            # ADDQ
            ins_name = "ADDQ"
        else:
            # SUBQ
            ins_name = "SUBQ"
        ins = Instruction("{}{} {}, {}".format(ins_name,
                                               size_text,
                                               data_text,
                                               ea_text),
                          2 + ea_bytes)

    return ins, is_end


def _parse_branch(prog, address, op_code):
    is_end = False
    condition = _select_bits(op_code, 8, 11)
    offset = op_code & 0xFF
    size = + 2
    if offset == 0:
        # Word offset in extension word
        size += 2
        offset = prog[address + 2]
        if offset & 0x8000:
            # Sign-extension
            offset = offset - 0x10000
    elif offset & 0x80:
        offset = offset - 0x100

    labels = (address + 2 + offset,)

    if condition == 0:
        # BRA
        ins = Instruction("BRA {}", size, labels)
        is_end = True
    elif condition == 1:
        # BSR
        ins = Instruction("BSR {}", size, labels)
    else:
        # Bcc
        condition_str = _parse_condition(condition)
        ins = Instruction("B{}".format(condition_str) + " {}", size, labels)

    return ins, is_end


def _parse_moveq(prog, address, op_code):
    is_end = False
    if not (op_code & 0x100):
        data_text = "#0x{:02X}".format(op_code & 0xFF)
        ins = Instruction("MOVEQ {}, D{}".format(data_text,
                                                 _select_bits(op_code, 9, 11)),
                          2)
    else:
        ins = _invalid_instruction()
        is_end = True

    return ins, is_end


def _parse_or_div_sbcd(prog, address, op_code):
    is_end = False
    ea_mode, ea_register = _ea_split(op_code)
    register_index = _select_bits(op_code, 9, 11)
    bits_6_8 = _select_bits(op_code, 6, 8)

    if bits_6_8 == 3:
        # DIVU
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      OP_SIZE_WORD)
        ins = Instruction("DIVU {}, D{}".format(ea_text, register_index),
                          2 + ea_bytes)

    elif bits_6_8 == 7:
        # DIVS
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      OP_SIZE_WORD)
        ins = Instruction("DIVS {}, D{}".format(ea_text, register_index),
                          2 + ea_bytes)

    elif bits_6_8 == 4 and ea_mode < 2:
        # SBCD
        if ea_mode == 1:
            # Memory to memory
            ins_text = "-(A{}), -(A{})"
        else:
            # Data to data
            ins_text = "D{}, D{}"
        ins = Instruction("SBCD "
                          + ins_text.format(ea_register, register_index),
                          2)

    else:
        # OR
        bit8 = bits_6_8 >> 2
        op_size = bits_6_8 & 3
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        register_text = "D{}".format(register_index)
        size_text = _size_str(op_size)
        if bit8:
            # To memory
            src_text = register_text
            dst_text = ea_text
        else:
            # To data
            src_text = ea_text
            dst_text = register_text
        ins = Instruction("OR{} {}, {}".format(size_text, src_text, dst_text),
                          2 + ea_bytes)

    return ins, is_end


def _parse_sub(prog, address, op_code):
    """SUB, SUBA or SUBX."""
    is_end = False
    ea_mode, ea_register = _ea_split(op_code)
    op_type = _select_bits(op_code, 8)
    op_size = _select_bits(op_code, 6, 7)
    register_index = _select_bits(op_code, 9, 11)
    if op_size == 3:
        # SUBA
        op_size = OP_SIZE_LONG if op_type else OP_SIZE_WORD
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        size_text = _size_str(op_size)
        ins = Instruction("SUBA{} {}, A{}".format(size_text,
                                                  ea_text,
                                                  register_index),
                          2 + ea_bytes)

    elif op_type == 1 and ea_mode < 2:
        # SUBX
        if ea_mode == 1:
            # Memory to memory
            ins_text = "-(A{}), -(A{})"
        else:
            # Data to data
            ins_text = "D{}, D{}"
        size_text = _size_str(op_size)
        ins = Instruction("SUBX{} ".format(size_text)
                          + ins_text.format(ea_register, register_index),
                          2)

    else:
        # SUB
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        register_text = "D{}".format(register_index)
        size_text = _size_str(op_size)
        if op_type:
            # To memory
            src_text = register_text
            dst_text = ea_text
        else:
            # To data
            src_text = ea_text
            dst_text = register_text
        ins = Instruction("SUB{} {}, {}".format(size_text, src_text, dst_text),
                          2 + ea_bytes)

    return ins, is_end


def _parse_cmp_eor(prog, address, op_code):
    is_end = False
    ea_mode, ea_register = _ea_split(op_code)
    size = _select_bits(op_code, 6, 7)
    register_index = _select_bits(op_code, 9, 11)
    bit8 = _select_bits(op_code, 8)

    if size == 3:
        # CMPA
        op_size = OP_SIZE_LONG if bit8 else OP_SIZE_WORD
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        size_text = _size_str(op_size)
        ins = Instruction("CMPA{} {}, A{}".format(size_text,
                                                  ea_text,
                                                  register_index),
                          2 + ea_bytes)

    elif bit8 == 0:
        # CMP
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      size)
        size_text = _size_str(size)
        ins = Instruction("CMP{} {}, D{}".format(size_text,
                                                 ea_text,
                                                 register_index),
                          2 + ea_bytes)

    elif ea_mode == 1:
        # CMPM
        size_text = _size_str(size)
        ins = Instruction("CMPM{} (A{})+, (A{})+".format(size_text,
                                                         ea_register,
                                                         register_index),
                          2)

    else:
        # EOR
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      size)
        size_text = _size_str(size)
        ins = Instruction("EOR{} D{}, {}".format(size_text,
                                                 register_index,
                                                 ea_text),
                          2 + ea_bytes)

    return ins, is_end


def _parse_and_mul_abcd_exg(prog, address, op_code):
    """AND, MUL, ABCD or EXG."""
    is_end = False
    size = _select_bits(op_code, 6, 7)
    op_type = _select_bits(op_code, 8)
    ea_mode, ea_register = _ea_split(op_code & 0x3F)
    register_dst = _select_bits(op_code, 9, 11)

    if size == 3:
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      size)
        if op_type == 0:
            # MULU
            ins_name = "MULU"
        else:
            # MULS
            ins_name = "MULU"
        ins = Instruction("{} {}, D{}".format(ins_name, ea_text, register_dst),
                          2 + ea_bytes)

    elif _select_bits(op_code, 4, 8) == 0x10:
        # ABCD
        if ea_mode == 1:
            # Memory to memory
            ins_text = "-(A{}), -(A{})"
        else:
            # Data to data
            ins_text = "D{}, D{}"
        ins = Instruction("ABCD "
                          + ins_text.format(ea_register, register_dst),
                          2)

    elif op_type == 1 and _select_bits(op_code, 4, 5) == 0:
        # EXG
        op_mode = _select_bits(op_code, 3, 7)
        if op_mode == 0b01001:
            first_register = "A"
        else:
            first_register = "D"
        if op_mode == 0b01000:
            second_register = "D"
        else:
            second_register = "A"
        ins = Instruction("EXG {}{}, {}{}".format(first_register,
                                                  register_dst,
                                                  second_register,
                                                  ea_register),
                          2)

    else:
        # AND
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      size)
        register_text = "D{}".format(register_dst)
        size_text = _size_str(size)
        if op_type:
            # To memory
            src_text = register_text
            dst_text = ea_text
        else:
            # To data
            src_text = ea_text
            dst_text = register_text
        ins = Instruction("AND{} {}, {}".format(size_text, src_text, dst_text),
                          2 + ea_bytes)

    return ins, is_end


def _parse_add(prog, address, op_code):
    """ADD, ADDA or ADDX."""
    is_end = False
    register_index = _select_bits(op_code, 9, 11)
    ea_mode = _select_bits(op_code, 3, 5)
    # Bits 2-0 are the effective address register index
    ea_register = op_code & 7
    # Bit 8 is 'op_type' for ADD and 'op_size' for ADDA
    bit8 = _select_bits(op_code, 8)
    op_size = _select_bits(op_code, 6, 7)
    if op_size == 3:
        # ADDA
        op_size = OP_SIZE_LONG if bit8 else OP_SIZE_WORD
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        size_text = _size_str(op_size)
        ins = Instruction("ADDA{} {}, A{}".format(size_text,
                                                  ea_text,
                                                  register_index),
                          2 + ea_bytes)

    elif not bit8 or ea_mode > 1:
        # ADD
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      op_size)
        register_text = "D{}".format(register_index)
        size_text = _size_str(op_size)
        if bit8:
            # To memory
            src_text = register_text
            dst_text = ea_text
        else:
            # To data
            src_text = ea_text
            dst_text = register_text
        ins = Instruction("ADD{} {}, {}".format(size_text, src_text, dst_text),
                          2 + ea_bytes)

    elif bit8 == 1 and ea_mode < 2 and op_size != 3:
        # ADDX
        if ea_mode == 1:
            # Memory to memory
            ins_text = "-(A{}), -(A{})"
        else:
            # Data to data
            ins_text = "D{}, D{}"
        size_text = _size_str(op_size)
        ins = Instruction("ADDX{} ".format(size_text)
                          + ins_text.format(ea_register, register_index),
                          2)

    return ins, is_end


def _parse_shift_rotate(prog, address, op_code):
    """ASd, LSd, ROXd or ROd."""
    is_end = False
    op_size = _select_bits(op_code, 6, 7)
    shift_amount = _select_bits(op_code, 9, 11)
    direction = _select_bits(op_code, 8)
    ea_register = _select_bits(op_code, 0, 2)

    direction_str = "L" if direction else "R"

    if op_size == 3:
        # Memory shift/rotate
        ea_mode = _select_bits(op_code, 3, 5)
        ea_text, ea_bytes = _parse_ea(prog,
                                      address,
                                      ea_mode,
                                      ea_register,
                                      OP_SIZE_WORD)
        # Register index determines action
        if shift_amount == 0:
            # ASd
            ins_name = "AS"
        elif shift_amount == 1:
            # LSd
            ins_name = "LS"
        elif shift_amount == 2:
            # ROXd
            ins_name = "ROX"
        else:
            # ROd
            ins_name = "RO"
        ins = Instruction("{}{} {}".format(ins_name, direction_str, ea_text),
                          2 + ea_bytes)

    else:
        # Data register shift/rotate
        op_type = _select_bits(op_code, 5)
        # Bits 3-4 determine action
        action_index = _select_bits(op_code, 3, 4)
        size_text = _size_str(op_size)
        if op_type:
            # Shift amount in data register
            amount_text = "D{}".format(shift_amount)
        else:
            # Shift amount is shift_amount
            amount_text = "#{}".format(shift_amount if shift_amount else 8)
        if action_index == 0:
            # ASd
            ins_name = "AS"
        elif action_index == 1:
            # LSd
            ins_name = "LS"
        elif action_index == 2:
            # ROXd
            ins_name = "ROX"
        else:
            # ROd
            ins_name = "RO"
        ins = Instruction("{}{}{} {}, D{}".format(ins_name,
                                                   direction_str,
                                                   size_text,
                                                   amount_text,
                                                   ea_register),
                          2)

    return ins, is_end


# --- Effective address ---

def _parse_ea(prog, address, ea_mode, ea_register, size):
    text = None
    bytes = 0

    if ea_mode < 2:
        if ea_mode == 0:
            reg_name = "D"
        else:
            reg_name = "A"
        text = "{}{}".format(reg_name, ea_register)
    elif ea_mode < 5:
        text = "(A{})".format(ea_register)
        if ea_mode == 3:
            text += "+"
        elif ea_mode == 4:
            text = "-" + text
    elif ea_mode == 7 and ea_register < 2:
        if ea_register == 1:
            bytes = 4
            value = (prog[address + 2] << 16) | prog[address + 4]
            text = "(0x{:08X}).L".format(value)
        else:
            bytes = 2
            value = prog[address + 2]
            text = "(0x{:04X}).W".format(value)
    elif ea_mode == 7 and ea_register == 4:
        text, bytes = _parse_imm(prog, address + 2, size)
    elif (ea_mode == 7 and ea_register in (2, 3)) \
            or (ea_mode in (5, 6)):
        extension = prog[address + 2]
        bytes = 2
        if ea_mode == 7:
            reg_name = "PC"
            has_index = ea_register == 3
        else:
            reg_name = "A{}".format(ea_register)
            has_index = ea_mode == 6

        if has_index:
            value = "{:02X}".format(_select_bits(extension, 0, 7))
            ind_name = "D" if _select_bits(extension, 15) == 0 else "A"
            ind_index = _select_bits(extension, 12, 14)
            ind_size = _size_str(
                OP_SIZE_WORD if _select_bits(extension, 11) == 0
                else OP_SIZE_LONG)
            index = ", {}{}{}".format(ind_name, ind_index, ind_size)
        else:
            value = "{:04X}".format(extension)
            index = ""

        text = "(0x{}, {}{})".format(value, reg_name, index)

    if text is None:
        raise Exception(str((ea_mode, ea_register)))

    return text, bytes


def _ea_split(ea):
    """Split the effective address bits into 'mode' and 'register'."""
    return _select_bits(ea, 3, 5), _select_bits(ea, 0, 2)


def _ea_is_valid(ea, ea_register=None):
    """Check the effective address bits for validity."""
    if ea_register is None:
        ea_mode, ea_register = _ea_split(ea)
    else:
        ea_mode = ea
    return ea_mode != EA_MODE_OTHER or ea_register < 5


def _ea_is_data(ea, ea_register=None):
    """Check, if the effective address bits are data addressing."""
    if ea_register is None:
        ea_mode, ea_register = _ea_split(ea)
    else:
        ea_mode = ea
    return _ea_is_valid(ea_mode, ea_register) and ea_mode != EA_MODE_REG_A


def _ea_is_memory(ea, ea_register=None):
    """Check, if the effective address bits are memory addressing."""
    if ea_register is None:
        ea_mode, ea_register = _ea_split(ea)
    else:
        ea_mode = ea
    return _ea_is_valid(ea_mode, ea_register) and ea_mode > EA_MODE_REG_A


def _ea_is_control(ea, ea_register=None):
    """Check, if the effective address bits are control addressing."""
    if ea_register is None:
        ea_mode, ea_register = _ea_split(ea)
    else:
        ea_mode = ea
    return \
        _ea_is_valid(ea_mode, ea_register) \
        and (ea_mode > 4 or ea_mode == EA_MODE_A_INDIRECT) \
        and (ea_mode != EA_MODE_OTHER or ea_register != EA_REGISTER_IMMEDIATE)


def _ea_is_alterable(ea, ea_register=None):
    """Check, if the effective address bits are alterable addressing."""
    if ea_register is None:
        ea_mode, ea_register = _ea_split(ea)
    else:
        ea_mode = ea
    return ea_mode != EA_MODE_OTHER  # All modes != 7 are valid


def _ea_is_data_alterable(ea, ea_register=None):
    """Check, if the effective address bits are alterable addressing."""
    if ea_register is None:
        ea_mode, ea_register = _ea_split(ea)
    else:
        ea_mode = ea
    return ea_mode != EA_MODE_REG_A \
        and (ea_mode != EA_MODE_OTHER or ea_register < 2)


def _ea_is_memory_alterable(ea, ea_register=None):
    """Check, if the effective address bits are alterable addressing."""
    if ea_register is None:
        ea_mode, ea_register = _ea_split(ea)
    else:
        ea_mode = ea
    return ea_mode > 1 \
        and (ea_mode != EA_MODE_OTHER or ea_register < 2)


# --- Other ---

def _read_dword(prog, address):
    return (prog[address] << 16) | prog[address + 2]


def _parse_imm(prog, address, size):
    first = prog[address]
    if size == OP_SIZE_BYTE:
        bytes = 2
        text = "#0x{:02X}".format(first & 0xFF)
    elif size == OP_SIZE_WORD:
        bytes = 2
        text = "#0x{:04X}".format(first)
    else:
        second = prog[address + 2]
        bytes = 4
        text = "#0x{:08X}".format((first << 16) | second)
    return text, bytes


def _size_str(size):
    if size == OP_SIZE_BYTE:
        return ".B"
    elif size == OP_SIZE_WORD:
        return ".W"
    return ".L"


def _parse_condition(condition):
    condition = condition & 0xF
    return _CONDITION_STRS[condition]


def _select_bits(value, from_, to=-1):
    if to == -1:
        to = from_
    elif from_ > to:
        from_, to = to, from_
    diff = to - from_
    mask = ((1 << (diff + 1)) - 1) << from_
    return (value & mask) >> from_


def _invalid_instruction():
    return Instruction("ILLEGAL  ; Invalid instruction encountered", 2)


def _iter_bytes(f):
    value = f.read(1)
    while value:
        yield value
        value = f.read(1)


def _main(file_name):
    with open(file_name, "rb") as f:
        prog = WordList(map(ord, _iter_bytes(f)))

    initial_pc = _read_dword(prog, 4)

    # Map label addresses to names
    label_locations = {initial_pc: "main"}

    # Map exception names to vector address
    # These are defined in the User's Manual
    exception_vec_to_name = {
        0x8: "bus_error",
        0xC: "address_error",
        0x10: "illegal_instruction",
        0x14: "zero_divide",
        0x18: "chk_instruction",
        0x1C: "trapv_instruction",
        0x20: "privilege_violation",
        0x24: "trace",
        0x28: "line_1010_emulator",
        0x2C: "line_1111_emulator",
        0x3C: "uninitialized_interrupt",
        0x60: "spurious_interrupt",
        0x64: "interrupt_level_1",
        0x68: "interrupt_level_2",
        0x6C: "interrupt_level_3",
        0x70: "hblank",  # Mega Drive specific
        0x74: "interrupt_level_5",
        0x78: "vblank",  # Mega Drive specific
        0x7C: "interrupt_level_7",
    }
    for i in range(16):
        exception_vec_to_name[0x80 + 4*i] = "trap_instruction_" + str(i)
    # We ignore these for now, since they can cause a lot of trouble
    # and are not used by many (any?) Mega Drive programs
    # for i in range(192):
        # exception_vec_to_name[0x100 + 4*i] = "user_interrupt_" + str(i)

    active_handlers = set()

    # We want to avoid having multiple labels for a single handler, since
    # most vectors will have the same generic handler
    generic_handlers = 0
    # Add the exception handlers to the label mapping
    for vec_add, exc in exception_vec_to_name.items():
        if vec_add < initial_pc:
            handler_address = _read_dword(prog, vec_add)
            if handler_address < len(prog) \
                    and handler_address > 0 \
                    and not (handler_address & 1):
                active_handlers.add(vec_add)
                if handler_address not in label_locations:
                    label_locations[handler_address] = "handler_" + exc
                else:
                    # Since the handler is already present, it is highly
                    # likely that this is a generic handler
                    handler_name = label_locations[handler_address]
                    # Skip generic handlers
                    if handler_name.startswith("handler_"):
                        label_locations[handler_address] = \
                            "generic_handler_" + str(generic_handlers)
                        generic_handlers += 1

    # Map addresses to instructions
    instruction_map = {}

    while True:
        # Check if there are any more labels to handle
        for label in label_locations:
            if label not in instruction_map and label < len(prog):
                # print("handling label " + label_locations[label])
                break  # Break for-loop and work with this label
        else:
            break  # Break while-loop, since we are done

        is_end = False
        address = label
        while not is_end:
            # print("address: 0x{:08X}".format(address))
            assert address & 1 == 0
            ins, is_end = _parse_instruction(prog, address)
            # print("text: " + ins._raw_str)
            # print("labels: " + ",".join("0x{:08X}".format(lab)
            #                             for lab in ins.get_labels()))
            # print("is_end: " + ("True" if is_end else "False"))

            # Add the instruction
            instruction_map[address] = ins
            address += ins.get_size()

            # Add the labels mentioned by the instruction
            for lab in ins.get_labels():
                assert lab & 1 == 0
                if lab not in label_locations:
                    label_locations[lab] = "label_0x{:X}".format(lab)

            # Check whether we have already generated code for this address
            if address in instruction_map:
                is_end = True

    print("; Disassembly of " + os.path.basename(file_name))
    print("; Initial SSP\n"
          ".long 0x{:X}".format(_read_dword(prog, 0)))
    print("; Initial PC\n"
          ".long 0x{:X}".format(initial_pc))

    # Address of the first instruction
    start_address = min(label_locations)
    handlers_list = sorted(active_handlers)
    assert not handlers_list or (max(handlers_list) < start_address)
    current_address = 8
    for vec_add in handlers_list:
        if current_address != vec_add:
            assert current_address < vec_add
            for address in range(current_address, vec_add, 2):
                print(".word 0x{:04X}".format(prog[address]))
            print("")
            current_address = vec_add
        handler_address = _read_dword(prog, vec_add)
        handler_label = label_locations[handler_address]
        if not handler_label.startswith("handler_"):
            print("; Handler for " + exception_vec_to_name[vec_add])
        print(".long " + handler_label)
        print("")
        current_address += 4

    print("")

    last_address = max(instruction_map)
    has_skipped = False
    # Accumulate non-opcode values
    acc_amount = 0
    acc_value = None
    assert start_address & 1 == 0, start_address
    while current_address < len(prog):

        # Check whether there is an instruction here
        if current_address not in instruction_map:
            prog_value = prog[current_address]
            if acc_value != prog_value:
                # Clear the accumulated values
                if acc_amount > 4:
                    if acc_value == 0:
                        print(".org 0x{:04X}".format(current_address))
                    else:
                        print(".rept {}\n"
                              ".word 0x{:04X}  ; 0x{:04X} - 0x{:04X}\n"
                              ".endr".format(
                                acc_amount,
                                current_address - 2 - 2*acc_amount,
                                current_address - 2,
                                acc_value))
                else:
                    for i in range(acc_amount):
                        print(".word 0x{:04X}  ; @0x{:04X}".format(
                            acc_value,
                            current_address - 2*(acc_amount - i)))
                acc_amount = 1
                acc_value = prog_value
            else:
                acc_amount += 1

            # Check for labels
            if current_address in label_locations:
                label = label_locations[current_address]
                print("{}:".format(label))
            else:
                label = None
            current_address += 2

            continue

        if acc_value is not None:
            # Clear the accumulated values
            if acc_amount > 4:
                if acc_value == 0:
                    print(".org 0x{:04X}".format(current_address))
                else:
                    print(".rept {}\n"
                          ".word 0x{:04X}  ; 0x{:04X} - 0x{:04X}\n"
                          ".endr".format(
                            acc_amount,
                            current_address - 2 - 2*acc_amount,
                            current_address - 2,
                            acc_value))
            else:
                for i in range(acc_amount):
                    print(".word 0x{:04X}  ; @0x{:04X}".format(
                        acc_value,
                        current_address - 2*(acc_amount - i)))
            acc_amount = 0
            acc_value = None

        # Check for labels
        if current_address in label_locations:
            label = label_locations[current_address]
            print("{}:".format(label))
        else:
            label = None

        ins = instruction_map[current_address]
        # Check which labels are referenced by this instruction
        ins_labels = [label_locations[lab] for lab in ins.get_labels()]
        ins_str = ins.get_str(ins_labels)
        print("\t{}".format(ins_str), end="")
        is_first = False
        current_address += ins.get_size()

        # Add a comment indicating the address, if not apparent
        if label is None or not label.startswith("label_0x"):
            print("  ; @0x{:04X}".format(current_address), end="")
        print()

    if acc_value is not None:
        # Clear the accumulated values
        if acc_amount > 4:
            if acc_value == 0:
                print(".org 0x{:04X}".format(current_address))
            else:
                print(".rept {}\n"
                      ".word 0x{:04X}  ; 0x{:04X} - 0x{:04X}\n"
                      ".endr".format(
                        acc_amount,
                        current_address - 2 - 2*acc_amount,
                        current_address - 2,
                        acc_value))
        else:
            for i in range(acc_amount):
                print(".word 0x{:04X}  ; @0x{:04X}".format(
                    acc_value,
                    current_address - 2*(acc_amount - i)))


if __name__ == "__main__":
    _main(sys.argv[1])
