


# Old version using SDL 1, only got it working on linux
class _Rsdl1Display(Display):

    def __init__(self, scale=1):
        if not RSDL_WORKS:
            raise RuntimeError("RSDL is not working on the current platform")
        super(RsdlDisplay, self).__init__(scale)

        # --- Values used for RSDL ---

        self._window = RSDL.SetVideoMode(self.width * scale,
                                         self.height * scale,
                                         32,  # Color depth
                                         0)  # Flags
        # This rectangle will be used to draw pixels
        # Its size is 'scale*scale' and it will be moved to the desired
        # position before drawing
        self._rect = RSDL_helper.mallocrect(0, 0, self._scale, self._scale)

    def draw(self):
        """Draw the image on the screen."""
        # We assume that 'pixels' has been correctly set
        RSDL.LockSurface(self._window)
        for y in range(self.height):
            row = self._pixels[y]
            scaled_y = y * self._scale
            for x in range(self.width):
                if True:  # self._update_pixels[y][x]:
                    self._update_pixels[y][x] = False
                    self._draw_pixel(x * self._scale,
                                     scaled_y,
                                     self._cram.read(row[x]))
        RSDL.UnlockSurface(self._window)
        RSDL.Flip(self._window)

    def _draw_pixel(self, x, y, color):
        # Draws a 'scale*scale' sized pixel
        # Note that this is *super* slow if not compiled by RPython
        rffi.setintfield(self._rect, "c_x",  x)
        rffi.setintfield(self._rect, "c_y",  y)
        RSDL.FillRect(self._window, self._rect, self._to_sdl_color(color))

    def _to_sdl_color(self, color_word):
        """Translate a Mega Drive color to an SDL color."""
        red = int_utils.select_bits(color_word, 1, 3)
        green = int_utils.select_bits(color_word, 5, 7)
        blue = int_utils.select_bits(color_word, 9, 11)
        rgb_9 = (red, green, blue)
        return RSDL.MapRGB(
            self._window.c_format,
            _COLOR_TO_BYTE[red],
            _COLOR_TO_BYTE[green],
            _COLOR_TO_BYTE[blue])