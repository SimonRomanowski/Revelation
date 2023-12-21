# -*- coding: utf-8 -*-
"""
The entry point for the application.

Created on Thu Nov  9 18:23:44 2023

@author: Simon Romanowski
"""

import os

from utils import int_utils


class Debugger:

    def __init__(self, cpu68k, mem, display_device):
        self.cpu68k = cpu68k
        self.mem = mem
        self.display_device = display_device
        self._breakpoints = {}
        self._wait_for_breakpoint = False
        self._stop_debugging = False
        self._emulation_stopped = False

    def step(self):
        if self._stop_debugging:
            return
        if self._wait_for_breakpoint:
            if self.cpu68k.get_pc() not in self._breakpoints:
                return
            print("Hit breakpoint")
        old_verbose = self.mem._verbose
        self.mem.set_verbose(False)
        self._wait_for_breakpoint = False
        quit = False
        print("PC = 0x%s"
              % int_utils.to_32x_string(self.cpu68k.get_pc()))
        while not quit:
            os.write(1, "Enter a command...\n")
            command = ""
            while command == "":
                os.write(1, "> ")
                command = os.read(0, 255).strip()
            quit = self._execute_command(command)
            print("")
        self.mem.set_verbose(old_verbose)

    def post_mortem(self):
        self._emulation_stopped = True
        self._wait_for_breakpoint = False
        self.step()

    def _execute_command(self, command):
        quit = False
        command_split = command.lower().split(" ")
        base_command = command_split[0]
        other_args = command_split[1:]
        if base_command in ("h", "help"):
            self._print_help(other_args)
        elif base_command in ("c", "cpu", "68k"):
            self._execute_68k(other_args)
        elif base_command in ("v", "vdp"):
            self._execute_vdp(other_args)
        elif base_command in ("m", "memory"):
            self._print_memory(other_args)
        elif base_command in ("b", "breakpoint"):
            self._set_breakpoint(other_args)
        elif base_command in ("d", "delete"):
            self._delete_breakpoint(other_args)
        elif base_command in ("l", "list"):
            self._list_breakpoints(other_args)
        elif base_command in ("s", "step"):
            if self._emulation_stopped:
                print("Emulation has stopped")
            else:
                quit = True
        elif base_command in ("r", "run"):
            if self._emulation_stopped:
                print("Emulation has stopped")
            else:
                quit = True
                self._wait_for_breakpoint = True
        elif base_command in ("q", "quit"):
            quit = True
            self._stop_debugging = True
        else:
            print("Unknown command: '%s'" % base_command)
            print("Type 'help' for a list of commands.")
        return quit

    def _execute_68k(self, other_args):
        # TODO support more args
        print(self.cpu68k.__str__())

    def _execute_vdp(self, other_args):
        # TODO support more args
        if len(other_args) == 0:
            print(self.display_device.__str__())
            return
        arg = other_args[0]
        mem = None
        name = ""
        if arg in ("c", "cram"):
            mem = self.display_device._cram
            name = "CRAM"
        elif arg in ("v", "vram"):
            mem = self.display_device._vram
            name = "VRAM"
        elif arg in ("s", "sprites"):
            if len(other_args) > 1:
                max_amount, parse_failed = self._parse_int(other_args[1])
                if parse_failed:
                    return
            else:
                max_amount = 16
            entry_address = self.display_device._table_sprite
            for _ in range(max_amount):
                (sprite_x_pos,
                 sprite_y_pos,
                 sprite_width,
                 sprite_height,
                 next_index,
                 is_prio,
                 color_offset,
                 vflip,
                 hflip,
                 sprite_address) = self.display_device._parse_sprite_table(
                    entry_address)
                sprite_index = \
                    (entry_address - self.display_device._table_sprite) >> 3
                print(
                    "#0x%s:\n"
                    "X=%d, Y=%d, %dx%d, data=0x%s, palette=%d, next=%d, "
                    "flags=%s"
                    % (
                        int_utils.to_32x_string(sprite_index)[6:7],
                        sprite_x_pos,
                        sprite_y_pos,
                        sprite_width,
                        sprite_height,
                        int_utils.to_32x_string(sprite_address)[4:],
                        color_offset >> 4,
                        next_index >> 3,
                        "none" if not (vflip or hflip or is_prio)
                        else (
                            ("prio " if is_prio else "")
                            + ("vflip " if vflip else "")
                            + ("hflip" if hflip else "")
                        )
                    ))
                if next_index == 0:
                    print("Reached end of list")
                    break
                entry_address = self.display_device._table_sprite + next_index
            else:
                print("Reached maximum amount of sprites")
        elif arg in ("h", "help"):
            print("""\
<no arguments>
        Print the state of the VDP.

h/help
        Show this message.

c/cram <start_address> [<end_address>]
        Print the contents of the CRAM at the given address range.

v/vram <start_address> [<end_address>]
        Print the contents of the VDP at the given address range.

s/sprites [<max_amount>]
        Print the information on a certain amount of sprites.
        Default for max_amount is 16.
""")
        else:
            print("Unkown VDP args: %s\nType 'vdp help' for a list of commands"
                  % " ".join(other_args))
            return

        if mem is not None:
            if len(other_args) < 2:
                print("Missing address")
                return
            start_address, parse_failed = self._parse_int(other_args[1])
            if parse_failed:
                return
            if len(other_args) > 2:
                end_address, parse_failed = self._parse_int(other_args[2])
                if parse_failed:
                    return
            else:
                end_address = start_address + 1
            if start_address < 0 or end_address < 0:
                print("Negative address is not allowed")
                return
            if start_address >= end_address:
                print("End address has to be bigger than start address")
                return
            for address in range(start_address, end_address, 2):
                value = mem.read(address)
                print("%s[0x%s]: 0x%s | 0b%s | %d"
                      % (name,
                         int_utils.to_32x_string(address),
                         int_utils.to_32x_string(value)[4:],
                         int_utils.to_16b_string(value),
                         value))

    def _print_memory(self, other_args):
        if len(other_args) == 0:
            print("You need to provide an address")
            return
        start_address, parse_failed = self._parse_int(other_args[0])
        if parse_failed:
            return
        if len(other_args) > 1:
            end_address, parse_failed = self._parse_int(other_args[1])
            if parse_failed:
                return
        else:
            end_address = start_address + 1

        end_address = min(end_address, 0x1000000)

        if start_address < 0 or end_address < 0:
            print("Negative address is not allowed")
            return

        if end_address <= start_address:
            print("End address has to be bigger than start address")
            return

        for address in range(start_address, end_address, 2):
            value = self.mem.read(address)
            print("0x%s: 0x%s | 0b%s | %d"
                  % (int_utils.to_32x_string(address),
                     int_utils.to_32x_string(value)[4:],
                     int_utils.to_16b_string(value),
                     value))

    def _set_breakpoint(self, other_args):
        if len(other_args) == 0:
            print("Missing breakpoint address")
            return
        if self._emulation_stopped:
            print("Breakpoints may no longer be defined")
            return
        breakpoint, parse_failed = self._parse_int(other_args[0])
        if parse_failed:
            return
        self._breakpoints[breakpoint] = breakpoint
        print("Added breakpoint " + other_args[0])

    def _delete_breakpoint(self, other_args):
        if len(other_args) == 0:
            print("Missing breakpoint address")
            return
        if self._emulation_stopped:
            print("Breakpoints may no longer be defined")
            return
        breakpoint, parse_failed = self._parse_int(other_args[0])
        if parse_failed:
            return
        if breakpoint in self._breakpoints:
            del self._breakpoints[breakpoint]
            print("Deleted breakpoint " + other_args[0])
        else:
            print("No breakpoint for " + int_utils.to_32x_string(breakpoint))

    def _list_breakpoints(self, other_args):
        print("Breakpoints:")
        bps = list(self._breakpoints)
        for x in bps:
            print("0x" + int_utils.to_32x_string(x))

    def _parse_int(self, value):
        int_value = 0
        if value.startswith("0x"):
            value = value[2:]
            base = 16
        else:
            base = 10
        try:
            int_value = int(value, base)
        except ValueError:
            print(value + " is not a valid number")
            parse_failed = True
        else:
            parse_failed = False
        return int_value, parse_failed

    def _print_help(self, other_args):
        print("""\
Available commands:

h/help
        Print this help message.

c/cpu/68k
        Print the state of the M68k CPU.

v/vdp
        Print the state of the VDP.

m/memory <start_address> [<end_address>]
        Print the value at the given address or the range of addresses.
        End address is inclusive.
        Numbers may be in decimal or in hexadecimal (0x-prefix) notation.

b/breakpoint <pc_value>
        Set a breakpoint for the given value of the program counter.
        Numbers may be in decimal or in hexadecimal (0x-prefix) notation.

d/delete <pc_value>
        Delete the breakpoint for the given value of the program counter.
        Numbers may be in decimal or in hexadecimal (0x-prefix) notation.

l/list
        List all breakpoints.

s/step
        Progress the emulation by one M68k instruction.

r/run
        Run the program until a breakpoint is encountered.

q/quit
        Stop debugging. The program will keep running.
""")
