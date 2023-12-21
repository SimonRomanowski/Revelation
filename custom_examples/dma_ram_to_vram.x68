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

    ; Set tiles
    ; Set DMA length
    MOVE.W #0x9300+(((tiles_end-tiles)>>1)&0xFF), (A1)
    MOVE.W #0x9400+((((tiles_end-tiles)>>1)&0xFF00)>>8), (A1)
    ; Set DMA source address
    MOVE.W #0x9500+((tiles>>1)&0xFF), (A1)
    MOVE.W #0x9600+(((tiles>>1)&0xFF00)>>8), (A1)
    MOVE.W #0x9700+(((tiles>>1)&0x7F0000)>>16), (A1)
    ; Set VRAM write to 0x800 and activate DMA
    MOVE.L #0x40000080+((0x800&0x3FFF)<<16)+((0x800&0xC000)>>14), (A1)

    ; Set Plane B nametable
    ; Set VRAM write to 0x2000
    MOVE.L  #0x60000000, (A1)
    ; Set nametable B
    MOVE.W  #(0x0040+0x1A), (A0)
    MOVE.W  #(0x0040+0x07), (A0)
    MOVE.W  #(0x0040+0x04), (A0)
    MOVE.W  #(0x0040+0x0B), (A0)
    MOVE.W  #(0x0040+0x0B), (A0)
    MOVE.W  #(0x0040+0x0E), (A0)
    MOVE.W  #(0x0040+0x1A), (A0)
    MOVE.W  #(0x0040+0x16), (A0)
    MOVE.W  #(0x0040+0x0E), (A0)
    MOVE.W  #(0x0040+0x11), (A0)
    MOVE.W  #(0x0040+0x0B), (A0)
    MOVE.W  #(0x0040+0x03), (A0)
    MOVE.W  #(0x0040+0x19), (A0)

    ; Enable interrupts
    ANDI  #0xF8FF, SR

stall:
    BRA stall


just_rte:
    RTE


vblank_handler:
    RTE

tiles:
    ; Tile #0 (A)
    .long 0x00000000
    .long 0x00004400
    .long 0x00440044
    .long 0x00440044
    .long 0x00444444
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044

    ; Tile #1 (B)
    .long 0x00000000
    .long 0x00444400
    .long 0x00440044
    .long 0x00440044
    .long 0x00444400
    .long 0x00440044
    .long 0x00440044
    .long 0x00444400

    ; Tile #2 (C)
    .long 0x00000000
    .long 0x00004444
    .long 0x00440000
    .long 0x00440000
    .long 0x00440000
    .long 0x00440000
    .long 0x00440000
    .long 0x00004444

    ; Tile #3 (D)
    .long 0x00000000
    .long 0x00444400
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00444400

    ; Tile #4 (E)
    .long 0x00000000
    .long 0x00444444
    .long 0x00440000
    .long 0x00440000
    .long 0x00444444
    .long 0x00440000
    .long 0x00440000
    .long 0x00444444

    ; Tile #5 (F)
    .long 0x00000000
    .long 0x00444444
    .long 0x00440000
    .long 0x00440000
    .long 0x00444444
    .long 0x00440000
    .long 0x00440000
    .long 0x00440000

    ; Tile #6 (G)
    .long 0x00000000
    .long 0x00444444
    .long 0x00440000
    .long 0x00440000
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00444444

    ; Tile #7 (H)
    .long 0x00000000
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00444444
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044

    ; Tile #8 (I)
    .long 0x00000000
    .long 0x00444444
    .long 0x00004400
    .long 0x00004400
    .long 0x00004400
    .long 0x00004400
    .long 0x00004400
    .long 0x00444444

    ; Tile #9 (J)
    .long 0x00000000
    .long 0x00444444
    .long 0x00000044
    .long 0x00000044
    .long 0x00000044
    .long 0x00000044
    .long 0x00000044
    .long 0x00444400

    ; Tile #A (K)
    .long 0x00000000
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00444400
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044

    ; Tile #B (L)
    .long 0x00000000
    .long 0x00440000
    .long 0x00440000
    .long 0x00440000
    .long 0x00440000
    .long 0x00440000
    .long 0x00440000
    .long 0x00444444

    ; Tile #C (M)
    .long 0x00000000
    .long 0x00440044
    .long 0x00444444
    .long 0x00444444
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044

    ; Tile #D (N)
    .long 0x00000000
    .long 0x00440044
    .long 0x00440044
    .long 0x00444044
    .long 0x00444444
    .long 0x00444444
    .long 0x00440444
    .long 0x00440044

    ; Tile #E (O)
    .long 0x00000000
    .long 0x00004400
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00004400

    ; Tile #F (P)
    .long 0x00000000
    .long 0x00444400
    .long 0x00440044
    .long 0x00440044
    .long 0x00444400
    .long 0x00440000
    .long 0x00440000
    .long 0x00440000

    ; Tile #10 (Q)
    .long 0x00000000
    .long 0x00004400
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440444
    .long 0x00004444

    ; Tile #11 (R)
    .long 0x00000000
    .long 0x00444400
    .long 0x00440044
    .long 0x00440044
    .long 0x00444400
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044

    ; Tile #12 (S)
    .long 0x00000000
    .long 0x00004400
    .long 0x00440044
    .long 0x00440000
    .long 0x00004400
    .long 0x00000044
    .long 0x00440044
    .long 0x00004400

    ; Tile #13 (T)
    .long 0x00000000
    .long 0x00444444
    .long 0x00004400
    .long 0x00004400
    .long 0x00004400
    .long 0x00004400
    .long 0x00004400
    .long 0x00004400

    ; Tile #14 (U)
    .long 0x00000000
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00444444

    ; Tile #15 (V)
    .long 0x00000000
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00004400
    .long 0x00004400

    ; Tile #16 (W)
    .long 0x00000000
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00444444
    .long 0x00444444
    .long 0x00440044

    ; Tile #17 (X)
    .long 0x00000000
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00004400
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044

    ; Tile #18 (Y)
    .long 0x00000000
    .long 0x00440044
    .long 0x00440044
    .long 0x00440044
    .long 0x00004400
    .long 0x00004400
    .long 0x00004400
    .long 0x00004400

    ; Tile #19 (Z)
    .long 0x00000000
    .long 0x00444444
    .long 0x00000044
    .long 0x00000044
    .long 0x00004400
    .long 0x00440000
    .long 0x00440000
    .long 0x00444444
tiles_end:
