# -*- coding: utf-8 -*-
"""
Emulates the Mega Drive VDP.

Created on Fri Sep 29 22:28:27 2023

@author: Simon Romanowski
"""

from rsdl import RSDL, RSDL_helper
from rpython.rtyper.lltypesystem import rffi, lltype
import rpython.rlib.rtime as time

from megadrive.devices import device, ram
from utils import int_utils
from utils import rpython_utils


# Map the 3-bit color to an 8-bit color
_COLOR_TO_BYTE = [
    0x00,  # 0b000
    0x34,  # 0b001
    0x57,  # 0b010
    0x74,  # 0b011
    0x90,  # 0b100
    0xAC,  # 0b101
    0xCE,  # 0b110
    0xFF,  # 0b111
]

_SPRITE_PLANE_SIZE = (512, 512)
_SPRITE_PLANE_START = (128, 128)


# --- Types for rffi ---

UINTP = lltype.Ptr(lltype.Array(rffi.UINT, hints={'nolength': True}))
# These are 'FixedSizeArray' since when translating with RPython, 'Ptr'
# variables cannot be allocated with 'lltype.malloc'.
UINTPP = lltype.FixedSizeArray(rffi.UINTP, 1, hints={'nolength': True})
INTP = lltype.FixedSizeArray(rffi.INT, 1, hints={'nolength': True})


# --- Constants for RSDL ---

_NULL_RECT = lltype.nullptr(RSDL.Rect)
_SDL_TRANSPARENT = rffi.r_uint(0)


class Display(device.Device):
    """
    Provides a display to the Mega Drive's VDP chip.

    Note, that for proper functioning, a ``megadrive.memory.Memory`` is also
    needed to be set with ``Display.set_m68k_ram``.

    Parameters
    ----------
    scale: float
        Value by which to scale the resolution of the display. Default is 1.
        Higher scale influences performance. Scaling currently only uses
        "Nearest Neighbor".
    """

    def __init__(self, scale=1.0):
        # Currently active address
        self._address = 0
        # Address bus is 16-bit, but setting the address requires a long word
        # to be written to the control port.
        # This list will buffer writes that are detected as address writes.
        self._write_buffer = []
        # The index of the scanline that will be drawn next
        self._vcounter = 0
        # This flag will be set to true if a VRAM fill operation was detected.
        # On the next write to the data port, it will be executed.
        self._dma_vram_fill = False

        # --- Values and infos for drawing ---

        # TODO support PAL resolution
        self.width = 256
        self.height = 224
        self._scale = scale
        if self._scale < 1:
            raise rpython_utils.RValueError("Negative scale")
        # Lists of colors
        self._pixels_bg = None
        self._pixels_plane_bg = None
        self._pixels_plane_bg_prio = None
        self._pixels_plane_fg = None
        self._pixels_plane_fg_prio = None
        self._pixels_plane_sp = None
        self._pixels_plane_sp_prio = None
        # List of pixels in order of descending priority
        self._priority = None
        # Limit for pixel list indices
        self._pixel_address_limit = self.width * self.height

        # --- Memory Devices ---

        # Mega Drive color palette RAM (CRAM)
        # Colors with index 62 and 63 are invisible in shadow/highlight mode
        # 62: Highlight all pixels at the same location underneath this
        # 63: Shadow all pixels at the same location underneath this
        self._cram = ram.Ram(64*2)  # One word per color

        # Video RAM (VRAM), 64KB
        self._vram = ram.Ram(64 * 1024)

        # Vertical scrolling RAM (VSRAM), 80B
        self._vsram = ram.Ram(80)

        # Select one of the memory devices for reading/writing with the data
        # port
        self._selected_memory = self._cram

        # Reference to the M68k RAM for Direct Memory Access (DMA)
        # Needs to be set later, because it also needs a reference to this.
        self._m68k_ram = None

        # --- Registers ---

        # --- Register 0, Mode Register 1 ---
        self._disable_display = False
        # ???
        self._freeze_hv_counter = False
        self._low_color_mode = False
        self._do_horizontal_interrupts = False
        # Blank the 8 leftmost pixels
        self._blank_left = False

        # --- Register 1, Mode Register 2 ---
        # Flag for Master System or Mega Drive mode
        self._is_mega_drive_mode = False
        # Flag for PAL or NTSC mode
        self._is_pal = False
        # Enable DMA (direct memory access)
        self._enable_dma = False
        self._do_vertical_interrupts = False
        # Whether to draw only the background color or all layers
        self._enable_tiles_and_sprites = False
        # Use 128kB VRAM
        self._use_extended_vram = False

        # --- Register 2, Plane A Name Table Location ---
        # Address for the name table for plane A (foreground)
        self._table_plane_fg = 0

        # --- Register 3, Window Name Table Location ---
        # Address for the name table for the window plane
        self._table_plane_wn = 0

        # --- Register 4, Plane B Name Table Location ---
        # Address for the name table for plane B (background)
        self._table_plane_bg = 0

        # --- Register 5, Sprite Table Location ---
        self._table_sprite = 0

        # --- Register 7, Background Color ---
        # Address for CRAM
        self._bg_color_ind = 0

        # --- Register 0xA, Horizontal Interrupt Counter ---
        # Number of scanlines between HBLANK
        self._hblank_amount = 1
        # Current counter for HBLANK
        self._hblank_counter = 1

        # --- Register 0xB, Mode Register 3 ---
        # 0 = full screen, 1 = invalid, 2 = 8 pixel rows, 3 = single pixel rows
        self._hscroll_mode = 0
        # 0 = False = full screen, 1 = True = 16 pixel columns
        self._vscroll_mode = False
        # Enable external interrupts
        self._do_external_interrupts = False

        # --- Register 0xC, Mode Register 4 ---
        # 0 = no interlace, 1 = interlace normal resolution, 2 = no interlace,
        # 3 = interlace double resolution
        self._interlace_mode = 0
        # Shadow/Highlight mode
        self._shadow_highlight_mode = False
        # self._use_external_pixel_but = False
        # self._replace_vsync = False
        # self._freeze_hsync = False
        # Whether to use 320 or 256 pixel mode
        self._is_320_mode = False

        # --- Register 0xD, Horizontal Scroll Data Location ---
        self._hscroll_data = 0

        # --- Register 0xF, Auto-Increment Value ---
        # Auto-increment value for the address after each read/write to the
        # data port.
        self._increment_address = 0

        # --- Register 0x10, Plane Size ---
        # Width and height of the foreground and background planes in pixels
        self._plane_width = 256
        self._plane_height = 256

        # --- Register 0x11, Window Plane Horizontal Position ---
        # Horizontal position of the window in pixels
        self._window_pos_hor = 0
        # Draw window to the left (False) / right (True) of the horizontal
        # position
        self._window_draw_right = False

        # --- Register 0x12, Window Plane Vertical Position ---
        # Vertical position of the window in pixels
        self._window_pos_ver = 0
        # Draw window to the top (False) / bottom (True) of the vertical
        # position
        self._window_draw_down = False

        # --- Register 0x13/0x14, DMA Length ---
        # Length for Direct Memory Access (DMA)
        self._dma_length = 0

        # --- Register 0x15/0x16, DMA Source ---
        # Source address for Direct Memory Access (DMA)
        self._dma_address = 0
        # 0 = 1 = RAM to VRAM copy, 2 = VRAM fill, 3 = VRAM to VRAM copy
        self._dma_type = 0

        # --- Post-initialization ---

        # Initialize the pixel fields
        self._create_pixels()

    def _create_pixels(self):
        # This should always be called when the width/height changes
        self._pixels_bg = self._new_pixel_list()
        self._pixels_plane_bg = self._new_pixel_list()
        self._pixels_plane_bg_prio = self._new_pixel_list()
        self._pixels_plane_fg = self._new_pixel_list()
        self._pixels_plane_fg_prio = self._new_pixel_list()
        self._pixels_plane_sp = self._new_pixel_list()
        self._pixels_plane_sp_prio = self._new_pixel_list()
        self._priority = [
            self._pixels_plane_sp_prio,
            self._pixels_plane_fg_prio,
            self._pixels_plane_bg_prio,
            self._pixels_plane_sp,
            self._pixels_plane_fg,
            self._pixels_plane_bg,
        ]
        self._pixel_address_limit = self.width * self.height

    def _new_pixel_list(self):
        return [0 for _ in range(self.width * self.height)]

    def _inc_vcounter(self):
        self._vcounter = (self._vcounter + 1) % self.height

    def draw_line(self, next_frame_time=0.0):
        """Draw the next scan line on the screen."""
        # Draw the line
        # We draw line by line, since the palette and vertical scroll may
        # change during HBLANK (in-between lines)
        self._draw_line_pixels()

        self._inc_vcounter()

        # Check for VBLANK
        vblank = self._vcounter == 0

        hblank = self._check_hblank()

        return (
            False,
            vblank and self._do_vertical_interrupts,
            hblank and self._do_horizontal_interrupts,
            vblank,
        )

    def _draw_line_pixels(self):
        # Store the pixels for the current line in the corresponding list
        # in RGBA8888 format.
        y_pos = self._vcounter
        fg_h_offset, bg_h_offset = self._get_hscroll()
        # Start address for the row of pixels
        pixel_row_address = self.width * y_pos

        # The order in which we draw the pixels does not matter, since we
        # consider the priority of each plane later

        # Draw foreground plane
        self._draw_line_plane(y_pos,
                              fg_h_offset,
                              pixel_row_address,
                              self._pixels_plane_fg,
                              self._pixels_plane_fg_prio,
                              0,
                              self._table_plane_fg,
                              True)
        # Draw background plane
        self._draw_line_plane(y_pos,
                              bg_h_offset,
                              pixel_row_address,
                              self._pixels_plane_bg,
                              self._pixels_plane_bg_prio,
                              1,
                              self._table_plane_bg,
                              False)
        # Draw sprites
        self._draw_line_sprite(pixel_row_address, y_pos)
        # Draw the background color
        self._draw_line_background(pixel_row_address)

    def _to_rgba(self, md_color):
        """Convert from Mega Drive color format to RGBA8888."""
        # Format:
        # | 15|                        ...                            | 0 |
        # | - | - | - | - | b | b | b | - | g | g | g | - | r | r | r | - |
        red = _COLOR_TO_BYTE[int_utils.select_bits(md_color, 1, 3)]
        green = _COLOR_TO_BYTE[int_utils.select_bits(md_color, 5, 7)]
        blue = _COLOR_TO_BYTE[int_utils.select_bits(md_color, 9, 11)]
        return (red << 24) | (green << 16) | (blue << 8) | 0xFF

    def _draw_line_sprite(self, pixel_row_address, y_pos):
        # TODO write directly to the pixel lists
        # Store the colors for each pixel in this list
        row_colors = [0 for _ in range(self.width)]
        row_colors_prio = [0 for _ in range(self.width)]

        # Iterate over all sprites
        next_index = self._insert_sprite_data(self._table_sprite,
                                              y_pos,
                                              row_colors,
                                              row_colors_prio)
        # The amount of sprites that have been drawn yet
        sprite_amount = 1
        sprite_max = 20 if self._is_320_mode else 16
        while next_index != 0 and sprite_amount < sprite_max:
            next_index = self._insert_sprite_data(self._table_sprite
                                                  + next_index,
                                                  y_pos,
                                                  row_colors,
                                                  row_colors_prio)
            sprite_amount += 1

        # Insert the generated colors
        for x_pos in range(self.width):
            pixel_address = pixel_row_address + x_pos
            color_address = row_colors[x_pos]
            color_prio_address = row_colors_prio[x_pos]
            color = \
                0 if color_address == 0 \
                else self._to_rgba(self._cram.read(color_address << 1))
            color_prio = \
                0 if color_prio_address == 0 \
                else self._to_rgba(self._cram.read(color_prio_address << 1))
            self._pixels_plane_sp[pixel_address] = color
            self._pixels_plane_sp_prio[pixel_address] = color_prio

    def _insert_sprite_data(self,
                            entry_address,
                            y_pos,
                            row_colors,
                            row_colors_prio):
        (sprite_x_pos,
         sprite_y_pos,
         sprite_width,
         sprite_height,
         next_index,
         is_prio,
         color_offset,
         vflip,
         hflip,
         sprite_address) = self._parse_sprite_table(entry_address)
        # Check, if the sprite is visible at all
        # The first visible row is 128
        min_x = 128
        # The last visible row is 128 + self.width - 1
        max_x = min_x + self.width

        # Check, if the sprite intersects with the current line at all
        # The first visible row is 128
        plane_y_pos = y_pos + 128
        # Check below the current line
        if sprite_y_pos > plane_y_pos:
            return next_index
        # Check above the current line
        if (sprite_y_pos + sprite_height) <= plane_y_pos:
            return next_index

        pixel_y_pos = plane_y_pos - sprite_y_pos

        # Iterate over the sprites pixels that are on this line
        sprite_start = sprite_x_pos - min_x
        for pixel_x_pos in range(max(0, -sprite_start),
                                 min(sprite_width, max_x - sprite_x_pos)):
            # X coordinate of the pixel on the texture
            x_pos = sprite_start + pixel_x_pos
            # Check if there already is some opaque color
            # Sprites appearing later in the list have lower priority
            if row_colors_prio[x_pos] != 0:
                continue
            if not is_prio and (row_colors[x_pos] != 0):
                continue

            color_index = self._get_sprite_pixel(sprite_address,
                                                 pixel_x_pos,
                                                 pixel_y_pos,
                                                 sprite_width,
                                                 sprite_height,
                                                 vflip,
                                                 hflip)

            # Check for the transparent color
            if color_index == 0:
                continue

            color_address = color_offset + color_index

            if is_prio:
                row_colors_prio[x_pos] = color_address
            else:
                row_colors[x_pos] = color_address

        return next_index

    def _draw_line_background(self, pixel_row_address):
        # Color of the background (not the background plane)
        background_color = self._to_rgba(
            self._cram.read(self._bg_color_ind))
        # Address for the pixel to set in the texture
        for pixel_address in range(pixel_row_address,
                                     pixel_row_address + self.width):
            self._pixels_bg[pixel_address] = background_color

    def _draw_line_plane(self,
                         y_pos,
                         h_offset,
                         pixel_row_address,
                         pixels,
                         prio_pixels,
                         plane_index,
                         table_base,
                         use_window):
        # Current x coordinate of the plane
        # Never leave the current plane size with the indices
        plane_x_pos = h_offset % self._plane_width

        # Remember the last offset to avoid parsing nametable entries multiple
        # times
        last_table_entry_offset = -1

        # Needed for RPython:
        is_prio = 0
        color_offset = 0
        vflip = 0
        hflip = 0
        tile_address = 0

        # 'x_pos' is the column of the pixel on the texture that we draw next,
        # wheras 'plane_x_pos' is the column of the pixel on the plane we are
        # drawing. These are not the same due to scrolling.
        for x_pos in range(self.width):
            v_offset = self._get_vscroll(plane_x_pos, plane_index)
            plane_y_pos = (y_pos + v_offset) % self._plane_height
            # 2 bytes per entry, 'plane_width/8' entries per row
            # One row is for 8 pixels.
            table_row_offset = \
                ((self._plane_width >> 3) << 1) * (plane_y_pos >> 3)
            # Y position of the current pixel inside the tile
            tile_row = plane_y_pos & 0b111
            # Start address of the tile nametable entries
            table_start = table_base + table_row_offset

            # Offset into the nametable for the current column
            # Each entry points to a 8x8 tile, thus we divide by 8
            # Each entry is 2 bytes wide, thus we multiply by 2 afterwards
            table_entry_offset = (plane_x_pos >> 3) << 1

            # Try to use the last table entry
            if last_table_entry_offset != table_entry_offset:
                last_table_entry_offset = table_entry_offset

                (is_prio,
                 color_offset,
                 vflip,
                 hflip,
                 tile_address) = self._load_nametable_entry(
                    table_start + table_entry_offset)

            # X position of the current pixel inside the tile
            pixel_x_pos = plane_x_pos & 0b111

            # Consider horizontal flip
            if hflip:
                pixel_x_pos = 7 - pixel_x_pos

            # Consider vertical flip
            pixel_y_pos = (7 - tile_row) if vflip else tile_row

            # TODO do this cleaner
            # Check for window
            if use_window:
                is_window = (
                    # Vertical position
                    ((self._window_draw_down
                      and y_pos >= self._window_pos_ver)
                     or
                     (not self._window_draw_down
                      and y_pos < self._window_pos_ver))
                    or
                    # Horizontal position
                    ((self._window_draw_right
                      and x_pos >= self._window_pos_hor)
                     or
                     (not self._window_draw_right
                      and x_pos < self._window_pos_hor))
                )
                if is_window:
                    window_offset = \
                        (((self._plane_width >> 3) * (y_pos >> 3)) << 1) \
                        + ((x_pos >> 3) << 1)
                    (is_prio,
                     color_offset,
                     vflip,
                     hflip,
                     tile_address) = self._load_nametable_entry(
                        self._table_plane_wn + window_offset)

                    # X position of the current pixel inside the tile
                    pixel_x_pos = x_pos & 0b111

                    # Consider horizontal flip
                    if hflip:
                        pixel_x_pos = 7 - pixel_x_pos

                    # Y position of the current pixel inside the tile
                    pixel_y_pos = y_pos & 0b111

                    # Consider vertical flip
                    if vflip:
                        pixel_y_pos = 7 - pixel_x_pos

            # Load the pixel
            color_index = \
                color_offset \
                + self._get_tile_color(tile_address,
                                       pixel_x_pos,
                                       pixel_y_pos)

            # Get the color from CRAM and convert it
            # Each color is 2 bytes
            # Color 0 in all palettes is transparent
            color = \
                0 \
                if (color_index & 0xF) == 0 \
                else self._to_rgba(self._cram.read(color_index << 1))

            # Address for the pixel to set in the texture
            pixel_address = pixel_row_address + x_pos

            # Draw the pixel on the plane
            if is_prio:
                prio_pixels[pixel_address] = color
            else:
                prio_pixels[pixel_address] = 0
                pixels[pixel_address] = color

            # Never leave the current plane size with the index (which might
            # otherwise happen due to horizontal scrolling)
            plane_x_pos = (plane_x_pos + 1) % self._plane_width

    def get_pixel(self, pixel_address):
        if pixel_address < 0 or pixel_address >= self._pixel_address_limit:
            raise rpython_utils.RIndexError("Invalid pixel address (%d)"
                                            % (pixel_address))
        for pixels in self._priority:
            color = pixels[pixel_address]
            if color != 0:
                break
        else:
            color = self._pixels_bg[pixel_address]
        return color

    def set_m68k_ram(self, m68k_ram):
        """Set the reference to the M68k RAM."""
        self._m68k_ram = m68k_ram

    def write(self, address, value):
        """
        Write to the VDP controller.

        Supported addresses are:
        0x00:
            Data Port. Byte, Word and Long Word read/writes.
            The address and memory device can be selected through the control
            port. The address that is written to is increased by the value of
            the internal register 0x0F after each read/write.
        0x02:
            Data Port mirror. Can be used to write 2 words at a time by writing
            a Long Word to 0x00.
        0x04:
            Control Port. Byte, Word and Long Word read/write.
            Writing can be used for either writing to one of the 24 internal
            registers (Word or Long Word for 2 registers) or to select a memory
            device and address.
        0x06:
            Control Port mirror. Can be used to write 2 registers at a time or
            to select a device and address together with the value written to
            0x04.
        0x08:
            H/V counter. Read-only.
        0x0A, 0x0C, 0x0E:
            H/V counter mirror. Read-only.
        0x10-0x1E:
            Not yet implemented.

        Parameters
        ----------
        address: int
            The address of the interface to use. This is not the address in the
            currently selected memory, but one of the values mentioned above.

        value: int
            The word to write. The upper byte is the value for address, the
            lower byte is the value for address + 1 (big endian).
        """
        value &= 0xFFFF
        if address < 4:
            # Data Port (and mirror)
            self._selected_memory.write(self._address & ~1, value)
            self._address += self._increment_address

            if self._dma_vram_fill:
                # Execute VRAM fill
                self._vram.fill_bytes(self._address,
                                      self._dma_length,
                                      value >> 8)
        elif address < 8:
            # Control Port
            # The written value might be a long word to select the addressing
            if int_utils.select_bits(value, 13, 15) == 0b100:
                # Write registers
                if self._write_buffer:  # Clear write buffer
                    self._write_buffer.pop()
                self.set_register(
                    int_utils.select_bits(value, 8, 12),
                    value & 0xFF)
            elif address < 6:
                # Change addressing
                # 'value' is upper word of addressing
                if self._write_buffer:
                    lower_word = self._write_buffer.pop()
                    self.set_addressing((value << 16) | lower_word)
                else:
                    self._write_buffer.append(value)
            else:
                # Change addressing
                # 'value' is lower word of addressing
                if self._write_buffer:
                    upper_word = self._write_buffer.pop()
                    self.set_addressing((upper_word << 16) | value)
                else:
                    self._write_buffer.append(value)
        elif address < 0x10:
            # Ignore write to read-only memory
            pass
        elif address < 0x19:
            # PSG Sound Chip
            # TODO implement
            pass
        else:
            raise rpython_utils.RValueError(
                "Unknown VDP write address 0x%s"
                % int_utils.to_32x_string(address))

    def read(self, address):
        """
        Write to the VDP controller.

        Supported addresses are:
        0x00:
            Data Port. Byte, Word and Long Word read/writes.
            The address and memory device can be selected through the control
            port. The address that is read from is increased by the value of
            the internal register 0x0F after each read/write.
        0x02:
            Data Port mirror. Can be used to read 2 words at a time by reading
            a Long Word from 0x00.
        0x04:
            Control Port. Byte, Word and Long Word read/write.
            Reading returns information about the current state of the VDP.
        0x06:
            Control Port mirror. Can be used to read 2 registers at a time.
        0x08:
            H/V counter. Returns the currently drawn scanline.
        0x0A, 0x0C, 0x0E:
            H/V counter mirror.
        0x10-0x1E:
            Not yet implemented.

        Parameters
        ----------
        address: int
            The address of the interface to use. This is not the address in the
            currently selected memory, but one of the values mentioned above.
        """
        if address < 4:
            # Data Port (and mirror)
            target_address = self._address
            self._address += self._increment_address
            return self._selected_memory.read(target_address)
        elif address < 8:
            # Control Port
            # TODO fill with real values
            fifo_empty = True
            fifo_full = False
            is_vinterrupt = self._vcounter == 0
            reached_sprite_limit = False
            sprites_colliding = False  # TODO
            interlaced_odd_frame = False  # TODO
            is_vblank = is_vinterrupt
            is_hblank = not is_vinterrupt
            is_dma = False  # TODO
            is_pal = self.height == 240
            return \
                0x3400 \
                + (0x0200 if fifo_empty else 0) \
                + (0x0100 if fifo_full else 0) \
                + (0x0080 if is_vinterrupt else 0) \
                + (0x0040 if reached_sprite_limit else 0) \
                + (0x0020 if sprites_colliding else 0) \
                + (0x0010 if interlaced_odd_frame else 0) \
                + (0x0008 if is_vblank else 0) \
                + (0x0004 if is_hblank else 0) \
                + (0x0002 if is_dma else 0) \
                + (0x0001 if is_pal else 0)
        elif address < 0x10:
            # Return vcounter|hcounter as a word
            # hcounter is always 0 for us
            if address & 1:
                # Uneven read
                hv_counter = self._vcounter
            else:
                hv_counter = self._vcounter << 8
            return hv_counter
        elif address < 0x19:
            # PSG Sound Chip
            # TODO implement
            return 0
        raise rpython_utils.RValueError(
            "Unknown VDP read address 0x%s"
            % int_utils.to_32x_string(address))

    def set_addressing(self, value):
        """Set the currently active memory device and address."""
        # Set all the ignored value to 0
        value &= 0xFFFF00F3
        memory_code = \
            int_utils.select_bits(value, 30, 31) \
            | int_utils.select_bits(value, 2, 5)
        self._address = \
            int_utils.select_bits(value, 16, 29) \
            + ((value & 0b11) << 14)  # Upper 2 bits
        if memory_code == 0b0011:
            # Write CRAM
            self._selected_memory = self._cram
        elif memory_code == 0b1000:
            # Read CRAM
            self._selected_memory = self._cram
        elif memory_code == 0b0000:
            # Read VRAM
            self._selected_memory = self._vram
        elif memory_code == 0b0001:
            # Write VRAM
            self._selected_memory = self._vram
        elif memory_code == 0b0100:
            # Read VSRAM
            self._selected_memory = self._vsram
        elif memory_code == 0b0101:
            # Write VSRAM
            self._selected_memory = self._vsram
        else:
            raise rpython_utils.RValueError("Unsupported memory space")

        # Direct memory access (DMA)
        do_dma = bool(value & 0x80)
        if do_dma:
            # For VRAM fill mode, we do not start yet. Instead, we wait for
            # the next write to the data port.
            if self._dma_type != 2:
                self._dma_transfer()
            else:
                self._dma_vram_fill = True
        else:
            self._dma_vram_fill = False

    def _dma_transfer(self):
        # We can assume that the DMA type is not VRAM fill
        # Address is always word-aligned and amount is always an even amount of
        # bytes.
        source_device = self._vram if self._dma_type == 3 else self._m68k_ram
        for offset in range(0, self._dma_length, 2):
            source_address = self._dma_address + offset
            target_address = self._address + offset
            value = source_device.read(source_address)
            self._selected_memory.write(target_address, value)

    def set_register(self, register_index, value):
        """Set one of the VDP registers."""
        if register_index == 0:
            # Mode Register 1
            self._disable_display = bool(value & 1)
            self._freeze_hv_counter = bool(value & 2)
            self._low_color_mode = not bool(value & 4)
            self._do_horizontal_interrupts = bool(value & 0x10)
            self._blank_left = bool(value & 0x20)

        elif register_index == 1:
            # Mode Register 2
            self._is_mega_drive_mode = bool(value & 4)
            self._is_pal = bool(value & 8)
            self._enable_dma = bool(value & 0x10)
            self._do_vertical_interrupts = bool(value & 0x20)
            self._enable_tiles_and_sprites = bool(value & 0x40)
            self._use_extended_vram = bool(value & 0x80)

        elif register_index == 2:
            # Plane A Name Table Location
            end_index = 6 if self._use_extended_vram else 5
            # Plane name table is always stored at a multiple of 0x2000
            self._table_plane_fg = \
                int_utils.select_bits(value, 3, end_index) * 0x2000

        elif register_index == 3:
            # Window Name Table Location
            end_index = 6 if self._use_extended_vram else 5
            start_index = 2 if self._is_320_mode else 1
            # Plane name table is always stored at a multiple of 0x800, or
            # 0x1000 if 320 pixel mode is active
            self._table_plane_wn = \
                int_utils.select_bits(value, start_index, end_index) * 0x800

        elif register_index == 4:
            # Plane B Name Table Location
            end_index = 3 if self._use_extended_vram else 2
            # Plane name table is always stored at a multiple of 0x2000
            self._table_plane_bg = \
                int_utils.select_bits(value, 0, end_index) * 0x2000

        elif register_index == 5:
            # Sprite Table Location
            end_index = 7 if self._use_extended_vram else 6
            start_index = 1 if self._is_320_mode else 0
            # Sprite table is always stored at a multiple of 0x200, or
            # 0x400 if 320 pixel mode is active
            self._table_sprite = \
                int_utils.select_bits(value, start_index, end_index) * 0x200

        elif register_index == 6:
            # Extra sprite table bit
            if self._use_extended_vram:
                # Value bit 5 is the address bit 16
                self._table_sprite = \
                    ((value & 0b100000) << 11) | (self._table_sprite & 0xFFFF)

        elif register_index == 7:
            # Background Color
            # Value is the index into the Mega Drive color palette
            # Each color is one word wide, so we multiply by 2
            self._bg_color_ind = (value & 0b00111111) << 1

        elif register_index == 8 or register_index == 9:
            # Unused, ignore
            pass

        elif register_index == 0xA:
            # Horizontal Interrupt Counter
            self._hblank_counter = max(1, value & 0xFF)

        elif register_index == 0xB:
            # Mode Register 3
            self._hscroll_mode = value & 0b11
            self._vscroll_mode = bool(value & 4)
            self._do_external_interrupts = bool(value & 8)

        elif register_index == 0xC:
            # Mode Register 4
            self._interlace_mode = int_utils.select_bits(value, 1, 2)
            self._shadow_highlight_mode = bool(value & 8)
            bit8 = bool(value & 0x80)
            # These bits have to be the same (?)
            if bit8 == bool(value & 1):
                self._update_320_mode(bit8)

        elif register_index == 0xD:
            # Horizontal Scroll Data Location
            end_index = 6 if self._use_extended_vram else 5
            # Value is address divided by 0x400
            self._hscroll_data = \
                int_utils.select_bits(value, 0, end_index) << 10

        elif register_index == 0xE:
            # Extra nametable bits
            if self._use_extended_vram:
                # Bit 4 in value is bit 16 for the foreground table address
                self._table_plane_fg = \
                    ((value & 0x10) << 12) | (self._table_plane_fg & 0xFF)
                # Bit 0 in value is bit 16 for the background table address
                self._table_plane_bg = \
                    ((value & 1) << 16) | (self._table_plane_bg & 0xFF)

        elif register_index == 0xF:
            # Auto-Increment value
            self._increment_address = value & 0xFF

        elif register_index == 0x10:
            # Plane Size
            # 0 = 256, 1 = 512, 2 = invalid, 3 = 1024
            width_code = value & 0b11
            height_code = int_utils.select_bits(value, 4, 5)
            # Ignore invalid values
            if width_code == 2 or height_code == 2:
                return
            # 1024 is only allowed together with 256
            if (width_code == 3 and height_code != 0) \
                    or (height_code == 3 and width_code != 0):
                return
            self._plane_width = (width_code + 1) * 256
            self._plane_height = (height_code + 1) * 256

        elif register_index == 0x11:
            # Window Plane Horizontal Position
            # Location of the window in units of 16 pixels
            self._window_pos_hor = (value & 0x1F) << 4
            self._window_draw_right = bool(value & 0x80)

        elif register_index == 0x12:
            # Window Plane Vertical Position
            # Location of the window in units of 8 pixels
            self._window_pos_ver = (value & 0x1F) << 3
            self._window_draw_down = bool(value & 0x80)

        elif register_index == 0x13:
            # DMA Length Lower Byte
            # Is always word-aligned
            self._dma_length = \
                (self._dma_length & 0x1FE00) | ((value & 0xFF) << 1)

        elif register_index == 0x14:
            # DMA Length High Byte
            # Is always word-aligned
            self._dma_length = \
                ((value & 0xFF) << 9) | (self._dma_length & 0x1FF)

        elif register_index == 0x15:
            # DMA Source Lower Byte
            # Is always word-aligned
            self._dma_address = \
                (self._dma_address & 0xFFFE00) | ((value & 0xFF) << 1)

        elif register_index == 0x16:
            # DMA Source Middle Byte
            # Is always word-aligned
            self._dma_address = \
                (self._dma_address & 0xFE01FF) | ((value & 0xFF) << 9)

        elif register_index == 0x17:
            # DMA Source High Byte and DMA Type
            self._dma_type = int_utils.select_bits(value, 6, 7)
            # Bit 0 of the type is the highest bit of the address for RAM to
            # VRAM copy
            end_index = 6 if self._dma_type < 2 else 5
            address_high = int_utils.select_bits(value, 0, end_index)
            # Address always word-aligned
            self._dma_address = \
                (self._dma_address & 0x1FFFF) | (address_high << 17)

        else:
            raise rpython_utils.RRuntimeError(
                "Register %d is not supported" % register_index)

    def stop(self):
        """Do display-specific cleanup."""
        pass

    def _check_hblank(self):
        self._hblank_counter -= 1
        hblank = self._hblank_counter <= 0
        if hblank:
            # Reset counter
            self._hblank_counter = self._hblank_amount
        return hblank

    def _load_nametable_entry(self, address):
        # Get table entries
        entry = self._vram.read(address)

        # Priority bit
        is_prio = bool(entry & 0x8000)

        # Palette line (bits 13-14) are bits 4-5 in the index of the
        # color to use
        color_offset = (entry & 0x6000) >> 9

        # Vertical and horizontal flip of the tile
        vflip = bool(entry & 0x1000)
        hflip = bool(entry & 0x0800)

        # Prepare the tile address
        # Each pixel is one nibble, each tile is 8x8 pixels
        # -> One tile is 32 bytes -> multiply tile index with 2^5
        tile_address = (entry & 0x07FF) << 5

        return is_prio, color_offset, vflip, hflip, tile_address

    def _get_tile_color(self, tile_address, pixel_x, pixel_y):
        # Tiles are placed row for row in VRAM
        # Each tile is 8x8=64 pixels, each pixel takes one nibble (4 bits)
        # Each row is 4 bytes
        pixel_byte_address = tile_address + (pixel_y << 2) + (pixel_x >> 1)
        # Load the selected byte
        color_byte = self._vram.read(pixel_byte_address) >> 8
        # Select the first or second nibble
        if pixel_x & 1:
            color = color_byte & 0xF
        else:
            color = (color_byte & 0xF0) >> 4
        return color

    def _get_sprite_pixel(self,
                          sprite_address,
                          pixel_x,
                          pixel_y,
                          sprite_width,
                          sprite_height,
                          vflip,
                          hflip):
        # Sprites are composed of multiple tiles.
        # Each tile is 8x8 pixels and is stored in VRAM row for row.
        # Each pixel in a tile takes up 4 bits.
        # The tiles of a sprite are arranged column for column.

        # Adjust for flipping
        if vflip:
            pixel_y = sprite_height - pixel_y - 1
        if hflip:
            pixel_x = sprite_width - pixel_x - 1

        # Find out which tile the pixel belongs to
        tile_address = \
            sprite_address \
            + ((pixel_x >> 3) * ((sprite_height >> 3) << 5)) \
            + ((pixel_y >> 3) << 5)
        # Get the pixel color of the tile
        # X/Y coordinates modulo 8, since tiles are 8x8
        return self._get_tile_color(tile_address,
                                    pixel_x & 0b111,
                                    pixel_y & 0b111)

    def _get_hscroll(self):
        """Get the horizontal scroll value for the current line."""
        if self._hscroll_mode == 0:
            # Is the same for all lines
            fg_scroll = self._vram.read(self._hscroll_data)
            bg_scroll = self._vram.read(self._hscroll_data + 2)
        elif  self._hscroll_mode == 2:
            # 8 pixel strips
            # Memory format is same as for mode 3, but the words for every
            # 2nd to 8th line is the same as the 1st
            base_address = \
                self._hscroll_data + ((self._vcounter & 0xFFF8) << 2)
            fg_scroll = self._vram.read(base_address)
            bg_scroll = self._vram.read(base_address + 2)
        elif  self._hscroll_mode == 3:
            # Individual scroll for every line
            # First word is foreground, next is background
            # First long word is the first line, second long word is for the
            # second line and so on
            base_address = \
                self._hscroll_data + (self._vcounter << 2)
            fg_scroll = self._vram.read(base_address)
            bg_scroll = self._vram.read(base_address + 2)
        else:
            # Sources have different information on whether mode 1 is valid
            raise rpython_utils.RRuntimeError("Unsupported hscroll mode")

        return (0x400 - fg_scroll) & 0x3FF, (0x400 - bg_scroll) & 0x3FF

    def _get_vscroll(self, x_pos, plane_index):
        """
        Get the vertical scroll value for the given column.

        A ``plane_index`` of 0 is for the foreground plane, 1 is for the
        background plane.
        """
        if self._vscroll_mode == 0:
            # Is the same for all X positions
            # At address 0 (fg) and 2 (bg) in VSRAM
            scroll = self._vsram.read(plane_index << 1)
        elif self._vscroll_mode == 1:
            # 16 pixel strips
            # TODO seems to be bugged
            strip_index = ((x_pos >> 4) << 2) + (plane_index << 2)
            scroll = self._vsram.read(strip_index)
        else:
            raise rpython_utils.RRuntimeError("Unsupported vscroll mode")

        return scroll & 0x3FF

    def _parse_sprite_table(self, entry_address):
        # First word is the vertical position
        y_pos = self._vram.read(entry_address) & 0x1FF

        # Second word contains size and next sprite index
        second_word = self._vram.read(entry_address + 2)
        # Width/height are values from 0 to 3, indicating how many tiles the
        # sprite consists of
        # Each sprite is 8 pixels
        sprite_height = (int_utils.select_bits(second_word, 8, 9) + 1) << 3
        sprite_width = (int_utils.select_bits(second_word, 10, 11) + 1) << 3
        # Index of the next sprite to display, offset for the sprite table
        # Each table entry is 8 bytes
        next_index = (second_word & 0x7F) << 3

        # Third word contains information on the graphics
        third_word = self._vram.read(entry_address + 4)
        # Priority bit
        is_prio = bool(third_word & 0x8000)
        # Index of the palette line
        color_offset = int_utils.select_bits(third_word, 13, 14) << 4
        # Vertical and horizontal flip
        vflip = bool(third_word & 0x1000)
        hflip = bool(third_word & 0x0800)
        # Address of the first tile in VRAM, in steps of 0x20
        sprite_address = (third_word & 0x7FF) << 5

        # Fourth word is the horizontal position
        x_pos = self._vram.read(entry_address + 6) & 0x1FF

        return (
            x_pos,
            y_pos,
            sprite_width,
            sprite_height,
            next_index,
            is_prio,
            color_offset,
            vflip,
            hflip,
            sprite_address
        )

    def _update_320_mode(self, is_320_mode):
        self._is_320_mode = is_320_mode
        self.width = 320 if self._is_320_mode else 256
        # Re-create the pixel lists
        self._create_pixels()

    def __str__(self):
        field_lines = [
            "address = 0x%s"
            % int_utils.to_32x_string(self._address),
            "write_buffer = [%s]"
            % int_utils.to_32x_string(self._write_buffer[0])
            if self._write_buffer else "",
            "vcounter = %d"
            % self._vcounter,
            "dma_vram_fill = %s"
            % _bool_to_str(self._dma_vram_fill),
            "width = %d pixels"
            % self.width,
            "height = %d pixels"
            % self.height,
            "scale = %f"
            % self._scale,
            "selected_memory = %s"
            % (
                "VRAM" if self._selected_memory == self._vram
                else (
                    "CRAM" if self._selected_memory == self._cram
                    else (
                        "VSRAM" if self._selected_memory == self._vsram
                        else "unknown"  # Should really never happen
                    )
                )
            ),
            "",
            "### Register 0x00 ###",
            "disable_display = %s"
            % _bool_to_str(self._disable_display),
            "freeze_hv_counter = %s"
            % _bool_to_str(self._freeze_hv_counter),
            "low_color_mode = %s"
            % _bool_to_str(self._low_color_mode),
            "do_horizontal_interrupts = %s"
            % _bool_to_str(self._do_horizontal_interrupts),
            "blank_left = %s"
            % _bool_to_str(self._blank_left),
            "",
            "### Register 0x01 ###",
            "is_mega_drive_mode = %s"
            % _bool_to_str(self._is_mega_drive_mode),
            "is_pal = %s"
            % _bool_to_str(self._is_pal),
            "enable_dma = %s"
            % _bool_to_str(self._enable_dma),
            "do_vertical_interrupts = %s"
            % _bool_to_str(self._do_vertical_interrupts),
            "enable_tiles_and_sprites = %s"
            % _bool_to_str(self._enable_tiles_and_sprites),
            "use_extended_vram = %s"
            % _bool_to_str(self._use_extended_vram),
            "",
            "### Register 0x02 ###",
            "table_plane_fg = 0x%s"
            % int_utils.to_32x_string(self._table_plane_fg),
            "",
            "### Register 0x03 ###",
            "table_plane_wn = 0x%s"
            % int_utils.to_32x_string(self._table_plane_wn),
            "",
            "### Register 0x04 ###",
            "table_plane_bg = 0x%s"
            % int_utils.to_32x_string(self._table_plane_bg),
            "",
            "### Register 0x05 ###",
            "table_sprite = 0x%s"
            % int_utils.to_32x_string(self._table_sprite),
            "",
            "### Register 0x07 ###",
            "bg_color_ind = 0x%s"
            % int_utils.to_32x_string(self._bg_color_ind),
            "",
            "### Register 0x0A ###",
            "hblank_amount = %d"
            % self._hblank_amount,
            "hblank_counter = %d"
            % self._hblank_counter,
            "",
            "### Register 0x0B ###",
            "hscroll_mode = %d"
            % self._hscroll_mode,
            "vscroll_mode = %d"
            % self._vscroll_mode,
            "do_external_interrupts = %s"
            % _bool_to_str(self._do_external_interrupts),
            "",
            "### Register 0x0C ###",
            "interlace_mode = %s"
            % _bool_to_str(self._interlace_mode),
            "shadow_highlight_mode = %s"
            % _bool_to_str(self._shadow_highlight_mode),
            "is_320_mode = %s"
            % _bool_to_str(self._is_320_mode),
            "",
            "### Register 0x0D ###",
            "hscroll_data = 0x%s"
            % int_utils.to_32x_string(self._hscroll_data),
            "",
            "### Register 0x0F ###",
            "increment_address = %d"
            % self._increment_address,
            "",
            "### Register 0x10 ###",
            "plane_width = %d pixels"
            % self._plane_width,
            "plane_height = %d pixels"
            % self._plane_height,
            "",
            "### Register 0x11 ###",
            "window_pos_hor = %d"
            % self._window_pos_hor,
            # position
            "window_draw_right = %s"
            % _bool_to_str(self._window_draw_right),
            "",
            "### Register 0x12 ###",
            "window_pos_ver = %d"
            % self._window_pos_ver,
            # position
            "window_draw_down = %s"
            % _bool_to_str(self._window_draw_down),
            "",
            "### Register 0x13/0x14 ###",
            "dma_length = %d bytes"
            % self._dma_length,
            "",
            "### Register 0x15-0x17 ###",
            "dma_address = 0x%s"
            % int_utils.to_32x_string(self._dma_address),
            "dma_type = %d"
            % self._dma_type,
            "",
            "VSRAM = [%s]"
            % ", ".join([hex(x) for x in self._vsram._qwords])
        ]
        return "Display{\n\t" + "\n\t".join(field_lines) + "\n}"


class _PlaneTexture:
    """Helper class for RsdlDisplay."""

    def __init__(self, renderer, width, height):
        # Every texture needs the texture itself and a pixel and pitch pointer
        # variable:
        # SDL_Texture* texture
        # unsigned int** pixel_pointer
        # int* pitch
        self.texture = RSDL.CreateTexture(
            renderer,
            RSDL.PIXELFORMAT_RGBA8888,
            RSDL.TEXTUREACCESS_STREAMING,
            width,
            height)
        self.pixel_pointer = lltype.malloc(UINTPP, flavor="raw")
        self.pitch_pointer = lltype.malloc(INTP, flavor="raw")
        # Need to cast these to the same type that SDL_LockTexture needs
        self._pixel_pointer_cast = rffi.cast(rffi.VOIDPP, self.pixel_pointer)
        self._pitch_pointer_cast = rffi.cast(rffi.INTP, self.pitch_pointer)

        # Set the blend mode for the texture to allow for transparency
        RSDL.SetTextureBlendMode(self.texture, RSDL.BLENDMODE_BLEND)

    def lock(self):
        RSDL.LockTexture(self.texture,
                         _NULL_RECT,
                         self._pixel_pointer_cast,
                         self._pitch_pointer_cast)

    def unlock(self):
        RSDL.UnlockTexture(self.texture)

    def get_pixels(self):
        """
        List of raw pixel data (write-only). May include row padding.

        Should only be called after locking.
        """
        return self.pixel_pointer[0]

    def get_row_length(self):
        """
        Length (in list entries) for one row of pixels.

        May only be called after locking the texture.
        """
        # pitch = texture width + padding
        return int(self.pitch_pointer[0]) // 4

    def free(self):
        lltype.free(self.pixel_pointer, flavor="raw")
        lltype.free(self.pitch_pointer, flavor="raw")
        RSDL.DestroyTexture(self.texture)


# For 64-Bit Windows the eci.py from rsdl had to be modified to use the x64
# version of SDL 2.0.12
# Other than that, VS 2022 Dev PowerShell v17.7.4 was used with cl.exe
# version 19.37.32824 from Build Tools installation and RPython from Oktober
# 2023.
# Somehow, this only workd from Windows Terminal App, not from standalone
# Developer PowerShell
# Also, some SDL functions and constants have been added to rsdl/RSDL.py and
# rsdl/constants.py
class RsdlDisplay(Display):
    """Display implementation using SDL 2."""

    def __init__(self, scale=1.0):
        Display.__init__(self, scale=scale)

        RSDL.Init(RSDL.INIT_EVERYTHING)

        window_width = int(self.width * self._scale)
        window_height = int(self.height * self._scale)

        self._window = RSDL.CreateWindow("Revelation",
                                         RSDL.WINDOWPOS_CENTERED,
                                         RSDL.WINDOWPOS_CENTERED,
                                         window_width,
                                         window_height,
                                         RSDL.WINDOW_SHOWN)
        self._renderer = RSDL.CreateRenderer(
            self._window, -1, RSDL.RENDERER_ACCELERATED)

        self._event = lltype.malloc(RSDL.Event, flavor="raw")
        # Flag that indicates if the textures are currently locked
        self._is_locked = False

        # The texture to draw on
        self._texture = None

        # Flags for the controller
        self._button_up = False
        self._button_down = False
        self._button_left = False
        self._button_right = False
        self._button_b = False
        self._button_c = False
        self._button_a = False
        self._button_start = False

        self._create_textures()
        self._clear_screen()

    def _create_textures(self):
        self._texture = _PlaneTexture(
            self._renderer,
            self.width,
            self.height)

    def _free_textures(self):
        self._texture.free()

    def stop(self):
        """Free allocated resources and stop SDL."""
        # Free allocated resources
        lltype.free(self._event, flavor="raw")
        self._free_textures()
        # Destroy window and renderer
        RSDL.DestroyRenderer(self._renderer)
        RSDL.DestroyWindow(self._window)

        RSDL.Quit()

    def show_next_frame(self):
        """Draw lines until the next frame will be shown."""
        keep_drawing = True
        while keep_drawing:
            self.draw_line()
            keep_drawing = self._vcounter != 0

    def draw_line(self, next_frame_time=0.0):
        """
        Draw the next line on the screen.

        Note, that the result is only displayed once the last line of the
        screen has been drawn.

        Parameters
        ----------
        next_frame_time: float, optional
            The earliest timestamp at which the next frame should be drawn.
            In other words, when this method is about to draw the frame it has
            created , it will wait until ``time.time()`` is at least
            ``next_frame_time``.
            Default is ``0.0``, meaning that no waiting will ever occur.

        Returns
        -------
        quit_: bool
            ``True`` iff the user requested to quit.

        vblank: bool
            ``True`` iff a VBLANK happens. This usually happens after each drawn
            frame, but it can be disabled.

        hblank: bool
            ``True`` iff an HBLANK happens. This usually happens after each
            drawn line, but it can be disabled and there may be a counter for
            it.

        frame_drawn: bool
            ``True`` iff the last line of the screen has just been drawn. As
            opposed to ``vblank`` this will always be ``True`` when the frame
            has been drawn, regardless of the VDP's settings.
        """
        quit, vblank, hblank, frame_drawn = \
            Display.draw_line(self, next_frame_time)

        if frame_drawn:
            # Handle the SDL events that have been queued up
            quit |= self._handle_events()
            # TODO since we only need one texture now this can be cleaned up
            self._lock_all_textures()
            self._draw_textures()
            self._unlock_all_textures()
            self._copy_textures()
            # Wait for the right time to show the frame
            sleep_duration = next_frame_time - time.time()
            time.sleep(max(0.0, sleep_duration))
            RSDL.RenderPresent(self._renderer)

        return quit, vblank, hblank, frame_drawn

    def _lock_all_textures(self):
        self._texture.lock()
        self._is_locked = True

    def _unlock_all_textures(self):
        self._texture.unlock()
        self._is_locked = False

    def _copy_textures(self):
        # TODO only on texture
        # Copy the texture data to the renderer
        # NULL will use the full area of texture and renderer
        # The textures will be scaled to fit the window size
        RSDL.RenderCopy(self._renderer,
                        self._texture.texture,
                        _NULL_RECT,
                        _NULL_RECT)

    def _draw_textures(self):
        """Draw the current frame on the textures."""
        # We assume the texture has been locked
        pixels = self._texture.get_pixels()
        row_length = self._texture.get_row_length()
        texture_index = 0
        for line_offset in range(0, self._pixel_address_limit, self.width):
            for x_pos in range(self.width):
                color = self._to_sdl_rgba(self.get_pixel(x_pos + line_offset))
                pixels[texture_index + x_pos] = color
            texture_index += row_length

    def _handle_events(self):
        quit_ = False
        event_counter = 6  # Handle only a certain amount of events per frame

        while RSDL.PollEvent(self._event) > 0 and event_counter > 0:
            event_type = rffi.cast(lltype.Unsigned, self._event.c_type)
            if event_type == RSDL.QUIT:
                quit_ = True
            if event_type in (RSDL.KEYDOWN, RSDL.KEYUP):
                keyboard_event = rffi.cast(RSDL.KeyboardEventPtr, self._event)
                keysim = keyboard_event.c_keysym
                sym = rffi.cast(lltype.Unsigned, keysim.c_sym)
                value = event_type == RSDL.KEYDOWN

                # TODO make the key mapping modifiable
                if sym == RSDL.K_UP:
                    self._button_up = value
                elif sym == RSDL.K_DOWN:
                    self._button_down = value
                elif sym == RSDL.K_LEFT:
                    self._button_left = value
                elif sym == RSDL.K_RIGHT:
                    self._button_right = value
                elif sym == RSDL.K_q:
                    self._button_a = value
                elif sym == RSDL.K_w:
                    self._button_b = value
                elif sym == RSDL.K_e:
                    self._button_c = value

            # TODO support more events

            event_counter -= 1

        self._m68k_ram.set_buttons(1,
                                   self._button_up, self._button_down,
                                   self._button_left, self._button_right,
                                   self._button_a, self._button_b,
                                   self._button_c,
                                   self._button_start)

        return quit_

    def _clear_screen(self):
        """Fill the screen with black."""
        bg_rect = RSDL_helper.mallocrect(0, 0,
                                         int(self.width * self._scale),
                                         int(self.height * self._scale))
        RSDL.SetRenderDrawColor(self._renderer, 0, 0, 0, 255)
        RSDL.RenderFillRect(self._renderer, bg_rect)
        RSDL.RenderPresent(self._renderer)
        lltype.free(bg_rect, flavor="raw")

    def _update_320_mode(self, is_320_mode):
        is_change = is_320_mode != self._is_320_mode
        Display._update_320_mode(self, is_320_mode)
        if is_change:
            was_locked = self._is_locked
            if was_locked:
                self._unlock_all_textures()
            # Re-scale all textures
            self._free_textures()
            self._create_textures()
            if was_locked:
                self._lock_all_textures()
        RSDL.SetWindowSize(self._window,
                           int(self.width * self._scale),
                           int(self.height * self._scale))

    def _to_sdl_rgba(self, color):
        return rffi.r_uint(color)



class FakeDisplay(Display):
    """Fake display implementation that does nothing."""

    def draw_line(self, next_frame_time=0.0):
        """Pretend to draw a line."""
        return Display.draw_line(self, next_frame_time)

    def _draw_line_plane(self,
                         y_pos,
                         h_offset,
                         pixel_row_address,
                         pixels,
                         prio_pixels,
                         plane_index,
                         table_base,
                         use_window):
        # To save performance, this method will be disabled, since there are
        # no side effects without displaying the image.
        # We still draw sprites because of collision detection.
        return

    def _draw_line_background(self, pixel_row_address):
        # See above
        return


def _bool_to_str(b):
    return "True" if b else "False"
