# -*- coding: utf-8 -*-
"""
The entry point for the application.

Created on Fri Sep 15 18:22:26 2023

@author: Simon Romanowski
"""

import os
import sys

from rpython.rlib import rpath
import megadrive.console


_DEFAULT_SCALE_FACTOR = 3.0

_EXIT_SUCCESS = 0
_EXIT_HELP = 1
_EXIT_VAL_SCALE_FACTOR = 2
_EXIT_NO_FILE = 3
_EXIT_WRONG_ARGS = 4
_EXIT_FILE_MISSING = 5
_EXIT_ARG_SCALE_FACTOR = 6
_EXIT_ARG_SILENT_CYCLES = 7
_EXIT_VAL_SILENT_CYCLES = 8
_EXIT_ARG_QUIT_AFTER = 9

_F_INF = float("inf")
_F_NIN = float("-inf")
_F_NAN = float("nan")


def entry_point(argv):
    """
    Entry point for the application.

    Parse the arguments and start.
    """
    # Transform to list so we can remove already parsed arguments
    args = list(argv[1:])

    if len(argv) < 2 or _pop_flag(args, ["-h", "--help"]):
        _print_usage(argv[0].split(rpath.sep)[-1])
        return _EXIT_HELP

    scale_factor_str = _pop_arg(args, ["-s", "--scale_factor"])

    try:
        scale_factor = \
            _DEFAULT_SCALE_FACTOR \
            if scale_factor_str is None \
            else float(scale_factor_str)
    except ValueError:
        print("Illegal value for -s/--scale-factor: %s" % scale_factor_str)
        return _EXIT_ARG_SCALE_FACTOR

    if scale_factor < 1 or scale_factor in (_F_INF, _F_NIN, _F_NAN):
        print("Illegal scale factor: %f" % scale_factor)
        return _EXIT_VAL_SCALE_FACTOR

    no_display = _pop_flag(args, ["--no-display"])
    no_sync = _pop_flag(args, ["--no-sync"])

    quit_on_stop = _pop_flag(args, ["--quit-on-stop"])

    verbose = _pop_flag(args, ["-v", "--verbose"])

    print_stats = _pop_flag(args, ["--show-stats"])

    dump_m68k_ram = _pop_flag(args, ["--dump-m68k-ram"])
    dump_vdp_vram = _pop_flag(args, ["--dump-vdp-vram"])
    dump_vdp_cram = _pop_flag(args, ["--dump-vdp-cram"])
    dump_z80_ram = _pop_flag(args, ["--dump-z80-ram"])
    dump_rom = _pop_flag(args, ["--dump-rom"])

    fail_on_invalid = _pop_flag(args, ["--fail-invalid-address"])

    silent_cycles_str = _pop_arg(args, ["--silent-for"])

    debug_mode = _pop_flag(args, ["-d", "--debug-mode"])

    try:
        silent_cycles = \
            0 if silent_cycles_str is None \
            else int(silent_cycles_str)
    except ValueError:
        print("Illegal value for --silent-for: %s" % silent_cycles_str)
        return _EXIT_ARG_SILENT_CYCLES

    if silent_cycles < 0:
        print("Illegal amount of silent cycles: %d" % silent_cycles)
        return _EXIT_VAL_SILENT_CYCLES

    quit_after_str = _pop_arg(args, ["--quit-after"])
    try:
        quit_after = -1 if quit_after_str is None else int(quit_after_str)
    except ValueError:
        print("Illegal amount for --quit-after given: %s" % quit_after_str)
        return _EXIT_ARG_QUIT_AFTER

    quit_after = max(-1, quit_after)

    if not args:
        print("No file name found")
        return _EXIT_NO_FILE
    elif len(args) > 1:
        print("Unrecognized arguments: '%s'" % "', '".join(args))
        return _EXIT_WRONG_ARGS
    else:
        file_name = args[0]

    if not os.path.isfile(file_name):
        print("The file %s does not exist" % file_name)
        return _EXIT_FILE_MISSING

    megadrive.console.run(file_name,
                          scale_factor,
                          no_display,
                          no_sync,
                          quit_on_stop,
                          verbose,
                          print_stats,
                          dump_m68k_ram,
                          dump_vdp_vram,
                          dump_vdp_cram,
                          dump_z80_ram,
                          dump_rom,
                          fail_on_invalid,
                          silent_cycles,
                          quit_after,
                          debug_mode)
    return _EXIT_SUCCESS


def _print_usage(program_name):
    print("""\
Usage:
%s [-s/--scale scale_factor] [--no-display] [--quit-on-stop] [-v/--verbose]
  file_name

Arguments:

file_name
        The path to the Mega Drive ROM to execute.

-s/--scale scale_factor (default: %f)
        A positive integer that indicates the size of the window to display.
        The default screen for the Mega Drive is 320x224 pixels. The scale
        factor multiply the size of the window with that value.

--no-display
        Set this flag to display showing a window. This is useful for debugging
        purpouses.
        Note, that most screen operations (like the memory map, HBLANK and
        VBLANK) will still work properly.

--quit-on-stop
        Set this flag to quit the emulator when the M68k encounters a STOP
        instruction.

-v/--verbose
        Set this flag to include the M68k processor state after each
        instruction.

--show-stats
        Set this flag to print some stats of the emulation after it finishes.

--dump-m68k-ram, --dump-vdp-vram, --dump-vdp-cram, --dump-z80-ram, --dump-rom
        These flags will cause the corresponding memory device to be dumped to
        the console after emulation finishes.

--fail-invalid-address
        Set this flag to stop emulation if an illegal memory access happens.
        This means that an address that is not part of the memory map is
        written or read.

--silent-for cycles (default: 0)
        Define an amount of M68k cycles to omit console output for.
        Has no effect if -v is not set.

--quit-after cycles (default: -1)
        Define a number of M68k cycles after which to quit the emulation.
        Default is -1. Specifying a negative value will cause the emulation to
        never stop based on cycle count.
        The first instruction will always be executed.

-d/--debug-mode
        Set this flag to enable stepping through the emulation instruction by
        instruction.

""" % (program_name, _DEFAULT_SCALE_FACTOR))


def _pop_arg(args,
             names,
             required=False):
    if not names:
        raise ValueError("No names given")
    found_value = False
    value = None
    for name in names:
        if name in args:
            if found_value:
                raise ValueError("Argument %s was specified multiple times"
                                 % "/".join(names))
            name_index = args.index(name)
            value_index = name_index + 1
            if len(args) <= value_index:
                raise ValueError("Expected value after %s" % name)
            value = args.pop(value_index)
            args.pop(name_index)

            found_value = True

    if not found_value and required:
        raise ValueError("Could not find value for argument %s"
                         % "/".join(names))

    return value


def _pop_flag(args, names):
    if not names:
        raise ValueError("No names given")
    found_value = False
    for name in names:
        if name in args:
            if found_value:
                raise ValueError("Argument %s was specified multiple times"
                                 % "/".join(names))
            name_index = args.index(name)
            args.pop(name_index)

            found_value = True

    return found_value


def target(*_):
    """Return main function for RPython."""
    return entry_point, None


if __name__ == "__main__":
    entry_point(sys.argv)
