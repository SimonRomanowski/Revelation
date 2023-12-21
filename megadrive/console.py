# -*- coding: utf-8 -*-
"""
The entry point for the application.

Created on Sat Sep 16 02:20:16 2023

@author: Simon Romanowski
"""

import os

from rpython.rlib import rtime
import m68k.cpu
from megadrive import memory
from megadrive.devices import display
import debug
from utils import rpython_utils


def run(file_name,
        scale,
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
        debug_mode):
    """
    Run the given Mega Drive file.

    Parameters
    ----------
    file_name: str
        The Mega Drive cartidge file that should be executed.
    """
    # Read the file
    if os.name == "nt":
        fp = os.open(file_name, os.O_RDONLY | os.O_BINARY, 0o777)
    else:
        fp = os.open(file_name, os.O_RDONLY, 0o777)
    program = ""
    while True:
        read = os.read(fp, 4096)
        if not read:
            break
        program += read
    os.close(fp)

    if verbose:
        print("start")

    # Verbosity may be omitted for some time
    is_verbose = verbose and silent_cycles <= 0

    if no_display:
        display_device = display.FakeDisplay()
    else:
        display_device = display.RsdlDisplay(scale=scale)

    mem = memory.Memory(program,
                        display_device,
                        verbose=is_verbose,
                        fail_on_invalid=fail_on_invalid)
    cpu68k = m68k.cpu.Cpu(mem, verbose=is_verbose)
    # Set the reference to RAM for Direct Memory Access
    display_device.set_m68k_ram(mem)

    if debug_mode:
        debugger = debug.Debugger(cpu68k, mem, display_device)
    else:
        debugger = None

    quit_ = False
    frames_per_second = 59.92274
    seconds_per_frame = 0 if no_sync else 1/frames_per_second
    # The M68k Cpu is supposed to run at 7.670454MHz, that means
    # 7,670,454 clock cycles per second.
    # The refresh rate of the screen is supposed to be 59.92274Hz, meaning that
    # in one second (on average) 59.92274 frames will be displayed.
    # Each frame consists of 'display_device.height' many lines. That means that
    # the time between each new line being drawn is (on average)
    # 1 / (height * 59.92274).
    # For NTSC, that is 1 / (224 * 59.92274) ~= 0,000074s or about
    # 571.5 M68k clock cycles.
    cycles_per_line = 7670454.0 / (display_device.height * frames_per_second)
    # This counter will contain the cycle of the M68k at which the next line
    # will be drawn.
    cycle_for_next_line = cycles_per_line
    # This will contain the earliest time at which the next frame should be
    # drawn.
    start_time = rtime.time()
    next_frame = 0 if no_sync else start_time + seconds_per_frame

    draw_count = 0

    while not quit_:
        try:
            stop = cpu68k.step()
            if mem.get_z80_reset():
                pass  # Reset the Z80 CPU
            # TODO cpuz80.step()
        except rpython_utils.ExceptionWithMessage as e:
            print(cpu68k.__str__())
            print(display_device.__str__())
            print("A %s occured: %s" % (str(type(e)), e._message))
            if debug_mode:
                debugger.post_mortem()
            break
        if quit_on_stop and stop:
            break

        m68k_cycles = cpu68k.get_cycle()

        if quit_after >= 0 and m68k_cycles >= quit_after:
            if verbose:
                print("Stopping after %d cycles" % quit_after)
            break

        if not is_verbose and verbose and m68k_cycles > silent_cycles:
            cpu68k.set_verbose(True)
            mem.set_verbose(True)

        if m68k_cycles >= int(cycle_for_next_line):
            # Increment the threshold for the next cylce
            cycle_for_next_line += cycles_per_line
            # Draw the line
            # Passing 'next_frame' will delay the drawing of the whole screen
            # until the current time has reached 'next_frame'.
            # Note that it will have no effect if not all lines have been drawn
            # yet.
            try:
                quit_, vblank, hblank, frame_drawn = \
                    display_device.draw_line(next_frame)
            except rpython_utils.ExceptionWithMessage as e:
                print(cpu68k.__str__())
                print(display_device.__str__())
                print("A %s occured: %s" % (str(type(e)), e._message))
                if debug_mode:
                    debugger.post_mortem()
                break

            # Cause VBLANK or HBLANK interrupts
            if vblank:
                cpu68k.cause_interrupt(6)
            elif hblank:
                cpu68k.cause_interrupt(4)

            if frame_drawn:
                # Set the time for the next frame to be drawn
                current_time = rtime.time()
                next_frame = next_frame + seconds_per_frame
                if current_time >= next_frame and not no_sync:
                    next_frame = current_time + seconds_per_frame
                draw_count += 1

        if debug_mode:
            debugger.step()

    total_time = rtime.time() - start_time

    if print_stats:
        print(cpu68k.__str__())
        print(display_device.__str__())
        print("Time taken %fs" % total_time)
        print("%f Hz" % (float(cpu68k.get_cycle()) / total_time))
        print("draw calls %d" % draw_count)
        print("%f average frames per second" % (draw_count/total_time))

    if dump_m68k_ram:
        print("M68k RAM:")
        mem._ram.dump(start_address=0xFF0000)
        print("")
    if dump_vdp_vram:
        print("VDP VRAM:")
        display_device._vram.dump()
        print("")
    if dump_vdp_cram:
        print("VDP CRAM:")
        display_device._cram.dump()
        print("")
    if dump_z80_ram:
        print("Z80 RAM:")
        mem._sound_ram.dump(start_address=0xA00000)
        print("")
    if dump_rom:
        print("ROM:")
        mem._rom.dump()
        print("")

    display_device.stop()
