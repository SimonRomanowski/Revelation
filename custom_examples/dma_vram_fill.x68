.equiv rom_base, 0x000000
.equiv ram_base, 0xFF0000
.equiv stack_top, ram_base + 0x100
.equiv membuf, stack_top

.org 0x000000
    .long    stack_top
    .long    reset

.org 0x78
    .long vblank_handler

.org 0x400
reset:
    ; Disable interrupts
    MOVE.W  #0x2700, SR
    LEA     stack_top, A7
    MOVE.L    A7, USP
    ; VDP setup
    LEA     0xC00000, A0
    LEA     4(A0), A1
    ; Set VDP to normal operation
    MOVE.W  #0x8004, (A1)
    ; Set display mode to Mega Drive (instead of Master
    ; System) and enable vertical interrupts and enable DMA
    MOVE.W  #0x8174, (A1)
    ; Set plane B name table  to VRAM address 0x2000
    MOVE.W  #0x8401, (A1)
    ; Set background color to first index in CRAM
    MOVE.W  #0x8700, (A1)
    ; Set scroll mode to mode 0 (whole screen)
    MOVE.W  #0x8B00, (A1)
    ; Enable shadow/highlight mode
    MOVE.W  #0x8C08, (A1)
    ; Set horizontal scroll data address to 0x3000 (0x3000 / 0x400 = 0xC)
    MOVE.W  #0x8D0C, (A1)
    ; Auto increment value for the VDP after each read or
    ; write
    MOVE.W  #0x8F02, (A1)


main:
    ; Set colors
    MOVE.L  #0xC0000000, (A1)
    MOVE.W  #0x0EEE, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x00E0, (A0)
    MOVE.W  #0x0E00, (A0)

    ; Set tiles
    ; Set VRAM write to 0x800
    MOVE.L  #0x48000000, (A1)

    ; Tile #0 (red X)
    MOVE.L  #0x11000011, (A0)
    MOVE.L  #0x01100110, (A0)
    MOVE.L  #0x00111100, (A0)
    MOVE.L  #0x00011000, (A0)
    MOVE.L  #0x00011000, (A0)
    MOVE.L  #0x00111100, (A0)
    MOVE.L  #0x01100110, (A0)
    MOVE.L  #0x11000011, (A0)

    ; Set Plane B nametable
    ; Set nametable B
    ; Fill 256*224/64=0x380 words
    MOVE.W  #0x937F, (A1)  ; Low byte of length/2
    MOVE.W  #0x9403, (A1)  ; High byte of length/2
    ; Set mode to VRAM fill
    MOVE.W  #0x9780, (A1)
    ; Set VRAM write to 0x2000
    MOVE.L  #0x600000C0, (A1)
    ; Write the fill value to the upper byte of the data port
    MOVE.W  #0x4040, (A0)
    MOVE.W  #0x0101, (A0)

    ; Enable interrupts
    ANDI  #0xF8FF, SR

stall:
    BRA stall


just_rte:
    RTE


vblank_handler:
    RTE
