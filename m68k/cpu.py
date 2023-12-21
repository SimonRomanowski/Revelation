# -*- coding: utf-8 -*-
"""
Concerned with the execution of 68k instructions.

Created on Fri Sep 15 19:43:18 2023

@author: Simon Romanowski
"""

from utils import rpython_utils

from cpu_utils import register
from utils import int_utils
import m68k.effective_address as ea
import m68k.instructions as ins
from m68k.constants import (
    OP_SIZE_BYTE, OP_SIZE_WORD, OP_SIZE_LONG,
    EA_MODE_REG_A,
    SR_T1, SR_S, SR_I,
)
from m68k.errors import IllegalInstruction, PrivilegeError


# Set to 'True' to force usage of JIT
FAIL_ON_NO_JIT = False

try:
    def get_printable_location(pc, rom):
        return \
            "pc: " + int_utils.to_32x_string(pc) \
            + " | rom[pc]: " + (
                int_utils.to_16b_string(
                    int_utils.select_bits(
                        rom[pc>>3],
                        (pc & 0b111) << 3,
                        (((pc & 0b111) + 1) << 3) - 1
                    )
                )
                if (pc>>3) < len(rom) else "NOT IN ROM"
            )
    from rpython.rlib import jit
    JIT_DRIVER = jit.JitDriver(greens=["pc", "rom"], reds="auto",
                               get_printable_location=get_printable_location)
    USE_JIT = True
except ImportError:
    if FAIL_ON_NO_JIT:
        raise RuntimeError("Could not do JIT setup")
    USE_JIT = False


class Cpu(object):
    """
    Models the Motorola 68000 CPU.

    Contains the state of the cpu and allows single instructions to be
    executed.

    Parameters
    ----------
    memory_interface: megadrive.memory.Memory
        Access to the memory that should be used.

    verbose: bool, optional
        Set this to ``True`` to print all instructions that are executed.
    """

    def __init__(self, memory_interface, verbose=False):
        self.mem = memory_interface
        # 8 32-bit data register
        self.d_registers = [register.Register32() for _ in range(8)]
        # 9 32-bit address registers
        # A7 is the (user-/system-) stack pointer
        # Initial Stack pointer at address 0
        self._user_stack = register.Register32()
        self._system_stack = register.Register32(
            (self.mem.read(0) << 16) | self.mem.read(2))
        self.a_registers = [register.Register32(),
                            register.Register32(),
                            register.Register32(),
                            register.Register32(),
                            register.Register32(),
                            register.Register32(),
                            register.Register32(),
                            self._system_stack]
        # 32-bit program counter
        # Program starts at the address at 0x4 in self.mem
        self._pc = register.Register32(
            (self.mem.read(4) << 16) | self.mem.read(6))
        # 16-bit status register
        # Bit     | 15 | 14 | 13 | 12 | 11 | 10 |  9 |  8 | 7 | 6 | 5 |
        # -------------------------------------------------------------------
        # Meaning | T1 | -- |  S | -- | -- | I2 | I1 | I0 | - | - | - |
        #
        # Bit     | 4 | 3 | 2 | 1 | 0 |
        # -------------------------------------------------------------------
        # Meaning | X | N | Z | V | C |
        # Only bits 4-0 are available in user mode. They are also refered to as
        # 'CCR' or 'Condition Code Register'.
        # All bits marked with "-" are ignored and always 0
        # Initially, the S-Bit is 1 to start in supervisor mode.
        self._stat_register = register.Register16(SR_S << 8)
        # Cycle counter will be updated by each instruction
        self._cycle = 0
        # Priority of the currently pending interrupt, or 0 if there is none
        self._pending_interrupt = 0
        self._stopped = False
        self._verbose = verbose

    # --- Register access ---

    def get_d(self, index, size=OP_SIZE_LONG):
        """
        Get the value of the data register with the given index.

        Parameters
        ----------
        index: int
            Index from 0 to 7 of the data register.

        size: int, optional
            Defines the section of the register, that should be considered.
            0 means only the lowest byte, 1 is the lower word and 3 (default)
            means the full 32 bits.
        """
        return self._get_reg(index, self.d_registers, size)

    def get_a(self, index, size=OP_SIZE_LONG):
        """
        Get the value of the address register with the given index.

        Parameters
        ----------
        index: int
            Index from 0 to 7 of the address register.

        size: int, optional
            Defines the section of the register, that should be considered.
            0 means only the lowest byte, 1 is the lower word and 3 (default)
            means the full 32 bits.
        """
        return self._get_reg(index, self.a_registers, size)

    @staticmethod
    def _get_reg(index, registers, size):
        """Get one of the eight data or address registers."""
        if index > 7:
            raise rpython_utils.RIndexError(
                "No data register with index %d." % index)
        if size > OP_SIZE_LONG:
            raise rpython_utils.RValueError(
                "Invalid size value given: %d" % size)

        reg = registers[index]
        if size == OP_SIZE_BYTE:
            return reg.get_byte()
        elif size == OP_SIZE_WORD:
            return reg.get_word()
        return reg.get()

    def get_pc(self):
        """Get the current program counter."""
        return self._pc.get()

    def get_usp(self):
        """Set the value of the user stack pointer."""
        return self._user_stack.get()

    def get_ssp(self):
        """Set the value of the system stack pointer."""
        return self._system_stack.get()

    def get_t1(self):
        """Get the T1 bit from the condition code register."""
        return self._stat_register.get_bit(15)

    def get_s(self):
        """Get the S bit from the condition code register."""
        return self._stat_register.get_bit(13)

    def get_i(self):
        """Get the I bits from the condition code register."""
        return int_utils.select_bits(self._stat_register.get(), 8, 10)

    def get_x(self):
        """Get the X bit from the condition code register."""
        return self._stat_register.get_bit(4)

    def get_n(self):
        """Get the N bit from the condition code register."""
        return self._stat_register.get_bit(3)

    def get_z(self):
        """Get the Z bit from the condition code register."""
        return self._stat_register.get_bit(2)

    def get_v(self):
        """Get the V bit from the condition code register."""
        return self._stat_register.get_bit(1)

    def get_c(self):
        """Get the C bit from the condition code register."""
        return self._stat_register.get_bit(0)

    def get_sr_full(self):
        """Get value of the entire status register."""
        return self._stat_register.get()

    def get_cycle(self):
        """Get the amount of cycles that have passed so far."""
        return self._cycle

    # --- Setters ---

    def set_d(self, index, value, size=OP_SIZE_LONG):
        """
        Get the value of the data register with the given index.

        Parameters
        ----------
        index: int
            Index from 0 to 7 of the data register.

        value: int
            The new value of the data register.

        size: int, optional
            Defines the section of the register, that should be considered.
            0 means only the lowest byte, 1 is the lower word and 3 (default)
            means the full 32 bits.
        """
        return self._set_reg(index, self.d_registers, value, size)

    def set_a(self, index, value):
        """
        Get the value of the address register with the given index.

        This always sets all 32 bits.

        Parameters
        ----------
        index: int
            Index from 0 to 7 of the address register.

        value: int
            The new value of the address register.
        """
        return self._set_reg(index, self.a_registers, value, OP_SIZE_LONG)

    @staticmethod
    def _set_reg(index, registers, value, size):
        """Get one of the eight data or address registers."""
        if index > 7:
            raise rpython_utils.RIndexError(
                "No data register with index %d." % index)
        if size > OP_SIZE_LONG:
            raise rpython_utils.RValueError(
                "Invalid size value given: %d" % size)

        reg = registers[index]
        if size == OP_SIZE_BYTE:
            reg.set_byte(value)
        elif size == OP_SIZE_WORD:
            reg.set_word(value)
        else:
            reg.set(value)

    def set_pc(self, value):
        """Set the current program counter."""
        self._pc.set(value)

    def set_usp(self, value):
        """Set the value of the user stack pointer."""
        self._user_stack.set(value)

    def set_ssp(self, value):
        """Set the value of the system stack pointer."""
        self._system_stack.set(value)

    # pylint: disable=invalid-name
    def set_ccr(self, mask, x=False, n=False, z=False, v=False, c=False):
        """
        Set the bits of the condition code register.

        Parameters
        ----------
        mask: int
            5-bit value that indicates which condition bit should be changed
            (1) or ignored (0). The order of the bits is the same as the
            parameters have here with ``x`` corresponding to the MSB.

        x, n, z, v, c: bool, optional
            Value of each condition code. Default value is ``False``.
        """
        mask = mask & 0b11111
        self._stat_register.set_bits(
            mask, c + (v << 1) + (z << 2) + (n << 3) + (x << 4))

    def set_sr(self, mask, t1=False, s=False, i=0):
        """
        Set the bits of the status register.

        Parameters
        ----------
        mask: int
            8-bit value that indicates which of the given status register bits
            should be changed (1) or ignored (0). The order of the bits is
            ``t1`` at index 7, ``s`` at index 5 and ``i`` from index 2 to 0.

        t1, s: bool, optional
            The values for the T1 and S bits. Default is ``False``.

        i: int, optional
            3-bit value that represents the bits I2 (MSB) to I0 (LSB). Default
            is ``0``.
        """
        mask = (mask & 0b10100111) << 8
        i &= 7
        self._stat_register.set_bits(mask, (i << 8) + (s << 13) + (t1 << 15))
        # Set Stack pointer according to S bit
        self.a_registers[7] = \
            self._system_stack if self.get_s() else self._user_stack

    # --- Instruction decoding ---

    def step(self, do_trace=True):
        """
        Execute the next instruction as indicated by the program counter.

        Returns ``True`` iff execution should continue.

        Parameters
        ----------
        do_trace: bool, optional
            Whether to ignore tracing or not. Default is ``True``, meaning that
            tracing will occur if the T1 bit is set at the beginning of
            instruction execution.

        Returns
        -------
        stop: bool
            ``True`` iff the execution has stopped.
        """
        # Check for pending interrupts
        if self._pending_interrupt > self.get_i():
            if self._verbose:
                print("### Handling pending interrupt")
            # Execute the interrupt handler now
            self._interrupt_trap(self._pending_interrupt)
            self._pending_interrupt = 0
            # Execution will continue in the next step with the interrupt
            # handler.
            # We do this to let the caller handle the cycles that passed after
            # calling 'self._interrupt_trap'.
            return False

        # Check stopped state
        if self._stopped:
            # Stopped state will be broken as soon as an interrupt arrives
            if self._verbose:
                print("### Waiting for interrupt...")
            # Doing this so the cycle counter never remains stagnant
            self.increment_cycles(1)
            return True

        if USE_JIT:
            JIT_DRIVER.jit_merge_point(pc=self._pc.get(),
                                       rom=self.mem.get_rom_list())

        # Only trace if not disabled from the outside
        # This is not a feature of the CPU, but of this emulator to make
        # testing a little more comfortable
        do_trace &= bool(self.get_t1())

        if self._verbose:
            # Print the state before op code fetch to help if it fails there
            print("###############\n%s" % self.__str__())

        op_code = self.fetch_next()

        if self._verbose:
            pc = self.get_pc()
            print("### Executing opcode: 0x%s\n"
                  "###       0b%s"
                  % (int_utils.to_32x_string(op_code)[4:],
                     int_utils.to_16b_string(op_code)))

        try:
            self._execute(op_code)
            if do_trace:
                if self._verbose:
                    print("### Entering Trace")
                self.cause_trap(9)
                self.increment_cycles(34)
        except IllegalInstruction as e:
            if self._verbose:
                print("### Illegal instruction detected: %s" % e._message)
            upper_bits = (op_code & 0xF000) >> 12
            if upper_bits == 0b1010:
                # Line 1010 Emulator
                vector_number = 10
            elif upper_bits == 0b1111:
                # Line 1111 Emulator
                vector_number = 11
            else:
                # Illegal Instruction
                vector_number = 4
            self.cause_trap(vector_number)
            self.increment_cycles(34)
        except PrivilegeError as e:
            if self._verbose:
                print("### Unprivileged execution: %s" % e._message)
            self.cause_trap(8, pc_offset=-2)
            self.increment_cycles(34)

        if self._stopped and self._verbose:
            print("### Stopping execution")

        return self._stopped

    def fetch_next(self):
        """Increment the PC and read the next instruction word."""
        pc = self.get_pc()
        self.set_pc(pc + 2)
        return self.mem.read(pc)

    def _execute(self, op_code):
        upper_bits = (op_code & 0xF000) >> 12
        execute_method = OP_GROUPS[upper_bits]
        execute_method(self, op_code)

    def _raise_illegal_op_code(self, op_code):
        raise IllegalInstruction(
            "Unknown OP code: 0b%s" % int_utils.to_16b_string(op_code))

    def _execute_bit_movep_imm(self, op_code):
        """Bit manipulation, MOVEP and Immediate instructions."""
        ea_mode, ea_register = ea.split(
            int_utils.select_bits(op_code, 0, 5))
        upper_byte = int_utils.select_bits(op_code, 8, 15)
        bits_6_15 = int_utils.select_bits(op_code, 6, 15)
        bits_6_8 = int_utils.select_bits(op_code, 6, 8)
        is_data_alterable = ea.is_data_alterable(ea_mode, ea_register)

        if op_code == 0x3C:
            # ORI to CCR
            if self._verbose:
                print("### ORI to CCR")
            ins.ori_to_ccr(self)

        elif op_code == 0x7C:
            # ORI to SR
            if self._verbose:
                print("### ORI to SR")
            ins.ori_to_sr(self)

        elif upper_byte == 0 and is_data_alterable:
            # ORI
            if self._verbose:
                print("### ORI")
            ins.ori(self, bits_6_8, ea_mode, ea_register)

        elif op_code == 0x23C:
            # ANDI to CCR
            if self._verbose:
                print("### ANDI to CCR")
            ins.andi_to_ccr(self)

        elif op_code == 0x27C:
            # ANDI to SR
            if self._verbose:
                print("### ANDI to SR")
            ins.andi_to_sr(self)

        elif upper_byte == 2 and is_data_alterable:
            # ANDI
            if self._verbose:
                print("### ANDI")
            ins.andi(self,
                     int_utils.select_bits(op_code, 6, 7),
                     ea_mode, ea_register)

        elif upper_byte == 4 and is_data_alterable:
            # SUBI
            if self._verbose:
                print("### SUBI")
            ins.subi(self, bits_6_8, ea_mode, ea_register)

        elif upper_byte == 6 and is_data_alterable:
            # ADDI
            if self._verbose:
                print("### ADDI")
            op_size = int_utils.select_bits(op_code, 6, 7)
            ins.addi(self, op_size, ea_mode, ea_register)

        elif op_code == 0xA3C:
            # EORI to CCR
            if self._verbose:
                print("### EORI to CCR")
            ins.eori_to_ccr(self)

        elif op_code == 0xA7C:
            # EORI to SR
            if self._verbose:
                print("### EORI to SR")
            ins.eori_to_sr(self)

        elif upper_byte == 0xA and is_data_alterable:
            # EORI
            if self._verbose:
                print("### EORI")
            ins.eori(self,
                     int_utils.select_bits(op_code, 6, 7),
                     ea_mode, ea_register)

        elif upper_byte == 0xC and is_data_alterable:
            # CMPI
            if self._verbose:
                print("### CMPI")
            ins.cmpi(self,
                     int_utils.select_bits(op_code, 6, 7),
                     ea_mode, ea_register)

        elif is_data_alterable and (bits_6_8 == 4 or bits_6_15 == 0x20):
            # BTST
            if self._verbose:
                print("### BTST")
            ins.btst(self,
                     int_utils.select_bits(op_code, 9, 11),
                     upper_byte & 1,
                     ea_mode, ea_register)

        elif is_data_alterable and (bits_6_8 == 5 or bits_6_15 == 0x21):
            # BCHG
            if self._verbose:
                print("### BCHG")
            ins.bchg(self,
                     int_utils.select_bits(op_code, 9, 11),
                     upper_byte & 1,
                     ea_mode, ea_register)

        elif is_data_alterable and (bits_6_8 == 6 or bits_6_15 == 0x22):
            # BCLR
            if self._verbose:
                print("### BCLR")
            ins.bclr(self,
                     int_utils.select_bits(op_code, 9, 11),
                     upper_byte & 1,
                     ea_mode, ea_register)

        elif is_data_alterable and (bits_6_8 == 7 or bits_6_15 == 0x23):
            # BSET
            if self._verbose:
                print("### BSET")
            ins.bset(self,
                     int_utils.select_bits(op_code, 9, 11),
                     upper_byte & 1,
                     ea_mode, ea_register)

        elif ea_mode == 1 and int_utils.select_bits(op_code, 8) == 1:
            # MOVEP
            if self._verbose:
                print("### MOVEP")
            ins.movep(self,
                      int_utils.select_bits(op_code, 9, 11),
                      ea_register,
                      (bits_6_8 >> 1) & 1,
                      bits_6_8 & 1)

        else:
            self._raise_illegal_op_code(op_code)

    def _execute_move(self, op_code):
        """MOVE instructions"""
        size = op_code >> 12
        src_mode, src_register = ea.split(op_code)
        # Order is swapped here!
        dst_register, dst_mode = ea.split(op_code >> 6)
        src_valid = ea.is_valid(src_mode, src_register)

        if src_valid and ea.is_data_alterable(dst_mode, dst_register):
            # MOVE
            if self._verbose:
                print("### MOVE")
            ins.move(
                self, dst_mode, dst_register, src_mode, src_register, size)
        elif src_valid and dst_mode == EA_MODE_REG_A and size != 1:
            # MOVEA
            if self._verbose:
                print("### MOVEA")
            ins.movea(self, dst_register, src_mode, src_register, size)
        else:
            self._raise_illegal_op_code(op_code)

    def _execute_misc(self, op_code):
        """Executes various instructions."""
        bits_6_11 = int_utils.select_bits(op_code, 6, 11)
        bits_6_7 = bits_6_11 & 3
        bits_6_8 = bits_6_11 & 7
        bits_8_11 = int_utils.select_bits(op_code, 8, 11)

        ea_mode, ea_register = ea.split(op_code)
        is_data_alterable = ea.is_data_alterable(ea_mode, ea_register)
        is_data = ea.is_data(ea_mode, ea_register)
        is_control = ea.is_control(ea_mode, ea_register)
        is_valid = ea.is_valid(ea_mode, ea_register)

        if bits_6_11 == 3 and is_data_alterable:
            # MOVE from SR
            if self._verbose:
                print("### MOVE from SR")
            ins.move_from_sr(self, ea_mode, ea_register)
        elif bits_6_7 != 3 and bits_8_11 == 0 and is_data_alterable:
            # NEGX
            if self._verbose:
                print("### NEGX")
            ins.negx(self, bits_6_7, ea_mode, ea_register)
        elif bits_6_7 != 3 and bits_8_11 == 2 and is_data_alterable:
            # CLR
            if self._verbose:
                print("### CLR")
            ins.clr(self, bits_6_7, ea_mode, ea_register)
        elif bits_6_11 == 0x13 and is_data:
            # MOVE to CCR
            if self._verbose:
                print("### MOVE to CCR")
            ins.move_to_ccr(self, ea_mode, ea_register)
        elif bits_6_7 != 3 and bits_8_11 == 4 and is_data_alterable:
            # NEG
            if self._verbose:
                print("### NEG")
            ins.neg(self, bits_6_7, ea_mode, ea_register)
        elif bits_6_7 != 3 and bits_8_11 == 6 and is_data_alterable:
            # NOT
            if self._verbose:
                print("### NOT")
            ins.not_(self, bits_6_7, ea_mode, ea_register)
        elif bits_6_11 == 0x1B and is_data:
            # MOVE to SR
            if self._verbose:
                print("### MOVE to SR")
            ins.move_to_sr(self, ea_mode, ea_register)
        elif ea_mode == 0 and (bits_6_11 == 0x22 or bits_6_11 == 0x23):
            # EXT
            if self._verbose:
                print("### EXT")
            ins.ext(self, ea_register, bits_6_11 & 1)
        elif bits_6_11 == 0x20 and is_data_alterable:
            # NBCD
            if self._verbose:
                print("### NBCD")
            ins.nbcd(self, ea_mode, ea_register)
        elif ea_mode == 0 and bits_6_11 == 0x21:
            # SWAP
            if self._verbose:
                print("### SWAP")
            ins.swap(self, ea_register)
        elif is_control and bits_6_11 == 0x21:
            # PEA
            if self._verbose:
                print("### PEA")
            ins.pea(self, ea_mode, ea_register)
        elif op_code == 0x4AFC:
            # ILLEGAL
            if self._verbose:
                print("### ILLEGAL")
            ins.illegal(self)
        elif is_data_alterable and bits_6_11 == 0x2B:
            # TAS
            if self._verbose:
                print("### TAS")
            ins.tas(self, ea_mode, ea_register)
        elif bits_6_7 != 3 and bits_8_11 == 0xA and is_valid:
            # TST
            if self._verbose:
                print("### TST")
            ins.tst(self, bits_6_7, ea_mode, ea_register)
        elif ea_mode < 2 and bits_6_11 == 0x39:
            # TRAP
            if self._verbose:
                print("### TRAP")
            ins.trap(self, int_utils.select_bits(op_code, 0, 3))
        elif ea_mode == 2 and bits_6_11 == 0x39:
            # LINK
            if self._verbose:
                print("### LINK")
            ins.link(self, ea_register)
        elif ea_mode == 3 and bits_6_11 == 0x39:
            # UNLK
            if self._verbose:
                print("### UNLK")
            ins.unlk(self, ea_register)
        elif (ea_mode == 4 or ea_mode == 5) and bits_6_11 == 0x39:
            # MOVE USP
            if self._verbose:
                print("### MOVE USP")
            ins.move_usp(self, ea_register, ea_mode & 1)
        elif op_code == 0x4E70:
            # RESET
            if self._verbose:
                print("### RESET")
            ins.reset(self)
        elif op_code == 0x4E71:
            # NOP
            if self._verbose:
                print("### NOP")
            ins.nop(self)
        elif op_code == 0x4E72:
            # STOP
            if self._verbose:
                print("### STOP")
            ins.stop(self)
        elif op_code == 0x4E73:
            # RTE
            if self._verbose:
                print("### RTE")
            ins.rte(self)
        elif op_code == 0x4E75:
            # RTS
            if self._verbose:
                print("### RTS")
            ins.rts(self)
        elif op_code == 0x4E76:
            # TRAPV
            if self._verbose:
                print("### TRAPV")
            ins.trapv(self)
        elif op_code == 0x4E77:
            # RTR
            if self._verbose:
                print("### RTR")
            ins.rtr(self)
        elif is_control and bits_6_11 == 0x3A:
            # JSR
            if self._verbose:
                print("### JSR")
            ins.jsr(self, ea_mode, ea_register)
        elif is_control and bits_6_11 == 0x3B:
            # JMP
            if self._verbose:
                print("### JMP")
            ins.jmp(self, ea_mode, ea_register)
        elif (ea_mode > 1 and (ea_mode != 7 or ea_register < 2)) \
                and int_utils.select_bits(op_code, 11) == 1 \
                and int_utils.select_bits(op_code, 7, 9) == 1:
            # MOVEM
            if self._verbose:
                print("### MOVEM")
            ins.movem(self,
                      int_utils.select_bits(op_code, 10),
                      bits_6_7 & 1,
                      ea_mode, ea_register)
        elif is_control and bits_6_8 == 7:
            # LEA
            if self._verbose:
                print("### LEA")
            ins.lea(self, bits_8_11 >> 1, ea_mode, ea_register)
        elif is_data and bits_6_8 == 6:
            # CHK
            if self._verbose:
                print("### CHK")
            ins.chk(self,
                    int_utils.select_bits(op_code, 9, 11),
                    ea_mode, ea_register)
        else:
            self._raise_illegal_op_code(op_code)

    def _execute_quick_scc_dbcc(self, op_code):
        """ADDQ, SUBQ, Scc or DBcc."""
        op_size = int_utils.select_bits(op_code, 6, 7)
        ea_mode, ea_register = ea.split(int_utils.select_bits(op_code, 0, 5))
        if op_size == 3:
            if ea_mode == EA_MODE_REG_A:
                # DBcc
                if self._verbose:
                    print("### DBcc")
                ins.dbcc(self,
                         ea_register,
                         int_utils.select_bits(op_code, 8, 11))
            else:
                # Scc
                if self._verbose:
                    print("### Scc")
                ins.scc(self,
                        int_utils.select_bits(op_code, 8, 11),
                        ea_mode,
                        ea_register)
        else:
            value = int_utils.select_bits(op_code, 9, 11)
            if int_utils.select_bits(op_code, 8) == 0:
                # ADDQ
                if self._verbose:
                    print("### ADDQ")
                ins.addq(self, value, op_size, ea_mode, ea_register)
            else:
                # SUBQ
                if self._verbose:
                    print("### SUBQ")
                ins.subq(self, value, op_size, ea_mode, ea_register)

    def _execute_branch(self, op_code):
        condition = int_utils.select_bits(op_code, 8, 11)
        offset = op_code & 0xFF
        if condition == 0:
            # BRA
            if self._verbose:
                print("### BRA")
            ins.bra(self, offset)
        elif condition == 1:
            # BSR
            if self._verbose:
                print("### BSR")
            ins.bsr(self, offset)
        else:
            # Bcc
            if self._verbose:
                print("### Bcc")
            ins.bcc(self, condition, offset)

    def _execute_moveq(self, op_code):
        if not (op_code & 0x100):
            if self._verbose:
                print("### MOVEQ")
            ins.moveq(self,
                      int_utils.select_bits(op_code, 9, 11),
                      op_code & 0xFF)
        else:
            self._raise_illegal_op_code(op_code)

    def _execute_or_div_sbcd(self, op_code):
        ea_mode, ea_register = ea.split(op_code)
        register_index = int_utils.select_bits(op_code, 9, 11)
        bits_6_8 = int_utils.select_bits(op_code, 6, 8)
        bit8 = bits_6_8 >> 2

        if bits_6_8 == 3:
            # DIVU
            if self._verbose:
                print("### DIVU")
            ins.divu(self, register_index, ea_mode, ea_register)
        elif bits_6_8 == 7:
            # DIVS
            if self._verbose:
                print("### DIVS")
            ins.divs(self, register_index, ea_mode, ea_register)
        elif bits_6_8 == 4 and ea_mode < 2:
            # SBCD
            if self._verbose:
                print("### SBCD")
            ins.sbcd(self, register_index, ea_register, ea_mode)
        else:
            # OR
            if self._verbose:
                print("### OR")
            ins.or_(self,
                    register_index,
                    bit8,
                    bits_6_8 & 3,
                    ea_mode,
                    ea_register)

    def _execute_sub(self, op_code):
        """SUB, SUBA or SUBX."""
        ea_mode, ea_register = ea.split(op_code)
        op_type = int_utils.select_bits(op_code, 8)
        op_size = int_utils.select_bits(op_code, 6, 7)
        register_index = int_utils.select_bits(op_code, 9, 11)
        if op_size == 3:
            # SUBA
            if self._verbose:
                print("### SUBA")
            ins.suba(self, register_index, op_type, ea_mode, ea_register)
        elif op_type == 1 and ea_mode < 2:
            # SUBX
            if self._verbose:
                print("### SUBX")
            ins.subx(self, register_index, ea_register, ea_mode, op_size)
        else:
            # SUB
            if self._verbose:
                print("### SUB")
            ins.sub(
                self, register_index, op_type, op_size, ea_mode, ea_register)

    def _execute_cmp_eor(self, op_code):
        ea_mode, ea_register = ea.split(op_code)
        size = int_utils.select_bits(op_code, 6, 7)
        register_index = int_utils.select_bits(op_code, 9, 11)
        bit8 = int_utils.select_bits(op_code, 8)

        if size == 3:
            # CMPA
            if self._verbose:
                print("### CMPA")
            ins.cmpa(self, register_index, bit8, ea_mode, ea_register)
        elif bit8 == 0:
            # CMP
            if self._verbose:
                print("### CMP")
            ins.cmp_(self, register_index, size, ea_mode, ea_register)
        elif ea_mode == 1:
            # CMPM
            if self._verbose:
                print("### CMPM")
            ins.cmpm(self, register_index, ea_register, size)
        else:
            # EOR
            if self._verbose:
                print("### EOR")
            ins.eor(self, register_index, size, ea_mode, ea_register)

    def _execute_and_mul_abcd_exg(self, op_code):
        """AND, MUL, ABCD or EXG."""
        size = int_utils.select_bits(op_code, 6, 7)
        op_type = int_utils.select_bits(op_code, 8)
        ea_mode, ea_register = ea.split(op_code & 0x3F)
        register_dst = int_utils.select_bits(op_code, 9, 11)

        if size == 3:
            if op_type == 0:
                # MULU
                if self._verbose:
                    print("### MULU")
                ins.mulu(self, register_dst, ea_mode, ea_register)
            else:
                # MULS
                if self._verbose:
                    print("### MULS")
                ins.muls(self, register_dst, ea_mode, ea_register)

        elif int_utils.select_bits(op_code, 4, 8) == 0x10:
            # ABCD
            if self._verbose:
                print("### ABCD")
            register_src = int_utils.select_bits(op_code, 0, 2)
            # Use another bit for op_type
            op_type = int_utils.select_bits(op_code, 3)
            ins.abcd(self, register_src, register_dst, op_type)

        elif op_type == 1 and int_utils.select_bits(op_code, 4, 5) == 0:
            # EXG
            if self._verbose:
                print("### EXG")
            register_src = int_utils.select_bits(op_code, 0, 2)
            ins.exg(self,
                    register_dst,
                    register_src,
                    int_utils.select_bits(op_code, 3, 7))

        else:
            # AND
            if self._verbose:
                print("### AND")
            ins.and_(
                self,
                register_dst,
                op_type,
                size,
                ea_mode, ea_register
            )

    def _execute_add(self, op_code):
        """ADD, ADDA or ADDX"""
        register_index = int_utils.select_bits(op_code, 9, 11)
        ea_mode = int_utils.select_bits(op_code, 3, 5)
        # Bits 2-0 are the effective address register index
        ea_register = op_code & 7
        # Bit 8 is 'op_type' for ADD and 'op_size' for ADDA
        bit8 = int_utils.select_bits(op_code, 8)
        op_size = int_utils.select_bits(op_code, 6, 7)
        if op_size == 3:
            # ADDA
            if self._verbose:
                print("### ADDA")
            ins.adda(self, register_index, bit8, ea_mode, ea_register)
        elif not bit8 or ea_mode > 1:
            # ADD
            if self._verbose:
                print("### ADD")
            ins.add(self, register_index, bit8, op_size, ea_mode, ea_register)
        else:
            # ADDX
            if self._verbose:
                print("### ADDX")
            ins.addx(self, ea_register, register_index, ea_mode, op_size)

    def _execute_shift_rotate(self, op_code):
        """ASd, LSd, ROXd or ROd."""
        op_size = int_utils.select_bits(op_code, 6, 7)
        shift_amount = int_utils.select_bits(op_code, 9, 11)
        direction = int_utils.select_bits(op_code, 8)
        ea_register = int_utils.select_bits(op_code, 0, 2)
        if op_size == 3:
            # Memory shift/rotate
            ea_mode = int_utils.select_bits(op_code, 3, 5)
            # Register index determines action
            if shift_amount == 0:
                # ASd
                if self._verbose:
                    print("### ASd")
                ins.asl_asr_to_mem(self, direction, ea_mode, ea_register)
            elif shift_amount == 1:
                # LSd
                if self._verbose:
                    print("### LSd")
                ins.lsl_lsr_to_mem(self, direction, ea_mode, ea_register)
            elif shift_amount == 2:
                # ROXd
                if self._verbose:
                    print("### ROXd")
                ins.roxl_roxr_to_mem(self, direction, ea_mode, ea_register)
            elif shift_amount == 3:
                # ROd
                if self._verbose:
                    print("### ROd")
                ins.rol_ror_to_mem(self, direction, ea_mode, ea_register)
            else:
                self._raise_illegal_op_code(op_code)
        else:
            # Data register shift/rotate
            op_type = int_utils.select_bits(op_code, 5)
            # Bits 3-4 determine action
            action_index = int_utils.select_bits(op_code, 3, 4)
            if action_index == 0:
                # ASd
                if self._verbose:
                    print("### ASd")
                ins.asl_asr_to_data(self,
                                    ea_register,
                                    shift_amount,
                                    op_type,
                                    op_size,
                                    direction)
            elif action_index == 1:
                # LSd
                if self._verbose:
                    print("### LSd")
                ins.lsl_lsr_to_data(self,
                                    ea_register,
                                    shift_amount,
                                    op_type,
                                    op_size,
                                    direction)
            elif action_index == 2:
                # ROXd
                if self._verbose:
                    print("### ROXd")
                ins.roxl_roxr_to_data(self,
                                      ea_register,
                                      shift_amount,
                                      op_type,
                                      op_size,
                                      direction)
            else:
                # ROd
                if self._verbose:
                    print("### ROd")
                ins.rol_ror_to_data(self,
                                    ea_register,
                                    shift_amount,
                                    op_type,
                                    op_size,
                                    direction)

    # --- Other instance methods ---

    def increment_cycles(self, amount):
        """Increment the cycle counter by the given amount."""
        if amount < 0:
            raise rpython_utils.RValueError("Negative increment amount")
        self._cycle += amount

    def push(self, value, size=OP_SIZE_WORD):
        """Push a value on the currently active stack."""
        if size == OP_SIZE_BYTE:
            # Stack is always aligned to words
            size = OP_SIZE_WORD
        stack_pointer = self.get_a(7) - 2*size  # 4 if long, 2 if word
        if size == OP_SIZE_WORD:
            self.mem.write(stack_pointer, value)
        else:
            self.mem.write(stack_pointer, value >> 16)
            self.mem.write(stack_pointer + 2, value)
        self.set_a(7, stack_pointer)

    def pop(self, size=OP_SIZE_WORD):
        """Pop a vlaue from the currently active stack."""
        stack_pointer = self.get_a(7)
        value = self.mem.read(stack_pointer)
        if size == OP_SIZE_BYTE:
            value = value & 0xFF
            offset = 2
        elif size == OP_SIZE_WORD:
            offset = 2
        else:
            value = (value << 16) | self.mem.read(stack_pointer + 2)
            offset = 4
        self.set_a(7, stack_pointer + offset)
        return value

    def cause_interrupt(self, priority):
        """
        Cause a hardware interrupt with the given priority.

        The execution of the interrupt handler will be executed as soon as
        the interrupt priority register contains a value that is lower than
        the given priority.
        """
        if priority < 1 or priority > 7:
            raise rpython_utils.RValueError("Invalid priority level")
        if self.get_i() < priority:
            self._interrupt_trap(priority)
        else:
            # ??? What happens if more interrupts arrive?
            # We assume that the old one gets lost
            self._pending_interrupt = priority

    def _interrupt_trap(self, priority):
        self.cause_trap(24 + priority)
        self.increment_cycles(72)
        self.set_sr(mask=SR_I, i=priority)

    def cause_trap(self, vector_number, pc_offset=0):
        """
        Cause a software interrupt with the given vector number.

        Stack format:
        ```
        ...
        Lower addresses
        ...
        (SSP) | Status Register |
        ------------------------|
           -2 | PC higher bits  |
           -4 | PC lower bits   |
        ------------------------|
           -6 | Vector offset   |
        ...
        Higher addresses
        ...
        ```

        The value of the PC is normally the one at the time of the function
        call, that is, the address of the instruction that comes *after* the
        one that caused the trap. To change this, ``pc_offset`` may be defined
        and ``self.get_pc() + pc_offset`` will be pushed.

        Note that this does not increment the cycle counter.
        """
        if self._verbose:
            print("### Causing trap %d" % vector_number)
        # Leave stopped state when a trap occurs
        self._stopped = False
        vector_offset = vector_number * 4
        old_sr = self.get_sr_full()
        self.set_sr(SR_T1 | SR_S, t1=False, s=True)
        self.push(self.get_pc() + pc_offset, OP_SIZE_LONG)
        self.push(old_sr)
        new_pc = \
            (self.mem.read(vector_offset) << 16) \
            + self.mem.read(vector_offset + 2)
        self.set_pc(new_pc)

    def set_stopped(self):
        """Set the stopped state to true."""
        self._stopped = True

    def set_verbose(self, verbose):
        self._verbose = bool(verbose)

    def _ram_to_string_save(self, address):
        if address >= 0xFF0000 and address <= 0xFFFFFF:
            return "0x%s" % int_utils.to_32x_string(self.mem.read(address))
        return "NOT IN RAM"

    def __str__(self):
        """Create a string representation of the current state."""
        return ("""\
cycle = %d
------------------------------------
  D0 = 0x%s    A0 = 0x%s
  D1 = 0x%s    A1 = 0x%s
  D2 = 0x%s    A2 = 0x%s
  D3 = 0x%s    A3 = 0x%s
  D4 = 0x%s    A4 = 0x%s
  D5 = 0x%s    A5 = 0x%s
  D6 = 0x%s    A6 = 0x%s
  D7 = 0x%s    A7 = 0x%s
------------------------------------
  USP = 0x%s
  SSP = 0x%s
------------------------------------
  PC = 0x%s
------------------------------------
  T-S--III---XNZVC
  %s
""") % (self.get_cycle(),
        int_utils.to_32x_string(self.d_registers[0].get()),
        int_utils.to_32x_string(self.a_registers[0].get()),
        int_utils.to_32x_string(self.d_registers[1].get()),
        int_utils.to_32x_string(self.a_registers[1].get()),
        int_utils.to_32x_string(self.d_registers[2].get()),
        int_utils.to_32x_string(self.a_registers[2].get()),
        int_utils.to_32x_string(self.d_registers[3].get()),
        int_utils.to_32x_string(self.a_registers[3].get()),
        int_utils.to_32x_string(self.d_registers[4].get()),
        int_utils.to_32x_string(self.a_registers[4].get()),
        int_utils.to_32x_string(self.d_registers[5].get()),
        int_utils.to_32x_string(self.a_registers[5].get()),
        int_utils.to_32x_string(self.d_registers[6].get()),
        int_utils.to_32x_string(self.a_registers[6].get()),
        int_utils.to_32x_string(self.d_registers[7].get()),
        int_utils.to_32x_string(self.a_registers[7].get()),
        int_utils.to_32x_string(self._user_stack.get()),
        int_utils.to_32x_string(self._system_stack.get()),
        int_utils.to_32x_string(self._pc.get()),
        int_utils.to_16b_string(self._stat_register.get()))


OP_GROUPS = [
    Cpu._execute_bit_movep_imm,  # 0
    Cpu._execute_move,  # 1
    Cpu._execute_move,  # 2
    Cpu._execute_move,  # 3
    Cpu._execute_misc,  # 4
    Cpu._execute_quick_scc_dbcc,  # 5
    Cpu._execute_branch,  # 6
    Cpu._execute_moveq,  # 7
    Cpu._execute_or_div_sbcd,  # 8
    Cpu._execute_sub,  # 9
    Cpu._raise_illegal_op_code,  # 0xA
    Cpu._execute_cmp_eor,  # 0xB
    Cpu._execute_and_mul_abcd_exg,  # 0xC
    Cpu._execute_add,  # 0xD
    Cpu._execute_shift_rotate,  # 0xE
    Cpu._raise_illegal_op_code,  # 0xF
]
