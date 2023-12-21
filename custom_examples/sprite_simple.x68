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
    ; System) and enable vertical interrupts
    MOVE.W  #0x8164, (A1)
    ; Set sprite table to VRAM address 0x2000
    MOVE.W  #0x8510, (A1)
    ; Set background color to first index in CRAM
    MOVE.W  #0x8700, (A1)
    ; Auto increment value for the VDP after each read or
    ; write
    MOVE.W  #0x8F02, (A1)


main:
    ; Set colors
    MOVE.L  #0xC0000000, (A1)
    MOVE.W  #0x0FFF, (A0)
    MOVE.W  #0x000D, (A0)
    MOVE.W  #0x0DD0, (A0)
    MOVE.W  #0x0D00, (A0)
    MOVE.W  #0x0000, (A0)

    ; Set sprites
    ; Set VRAM write to 0x2800
    MOVE.L  #0x68000000, (A1)

    ; Sprite #0 (upper left)
    MOVE.L  #0x00000333, (A0)
    MOVE.L  #0x00033222, (A0)
    MOVE.L  #0x00322222, (A0)
    MOVE.L  #0x03222222, (A0)
    MOVE.L  #0x03222222, (A0)
    MOVE.L  #0x32222222, (A0)
    MOVE.L  #0x32222222, (A0)
    MOVE.L  #0x32222222, (A0)

    ; Sprite #1 (lower left)
    MOVE.L  #0x32222222, (A0)
    MOVE.L  #0x32222222, (A0)
    MOVE.L  #0x32222222, (A0)
    MOVE.L  #0x03222222, (A0)
    MOVE.L  #0x03222222, (A0)
    MOVE.L  #0x00322222, (A0)
    MOVE.L  #0x00033222, (A0)
    MOVE.L  #0x00000333, (A0)

    ; Sprite #2 (upper right)
    MOVE.L  #0x33300000, (A0)
    MOVE.L  #0x22233000, (A0)
    MOVE.L  #0x22222300, (A0)
    MOVE.L  #0x22112230, (A0)
    MOVE.L  #0x21111230, (A0)
    MOVE.L  #0x21111223, (A0)
    MOVE.L  #0x22112223, (A0)
    MOVE.L  #0x22222223, (A0)

    ; Sprite #3 (lower right)
    MOVE.L  #0x22222223, (A0)
    MOVE.L  #0x22222223, (A0)
    MOVE.L  #0x22222223, (A0)
    MOVE.L  #0x22222230, (A0)
    MOVE.L  #0x22222230, (A0)
    MOVE.L  #0x22222300, (A0)
    MOVE.L  #0x22233000, (A0)
    MOVE.L  #0x33300000, (A0)

    ; Sprite #4 (small square)
    MOVE.L  #0x11111111, (A0)
    MOVE.L  #0x12222221, (A0)
    MOVE.L  #0x13222221, (A0)
    MOVE.L  #0x13322221, (A0)
    MOVE.L  #0x13332221, (A0)
    MOVE.L  #0x13333221, (A0)
    MOVE.L  #0x13333321, (A0)
    MOVE.L  #0x11111111, (A0)

    ; Set sprite table
    ; Set VRAM write to 0x2000
    MOVE.L  #0x60000000, (A1)
    ; Y coordinate in the plane (upper left corner is (128,128) = (0x80, 0x80))
    MOVE.W  #0x0080, (A0)
    ; Size (2x2) and 'next' field (0 -> last entry)
    MOVE.W  #(0x0500 + 0x0001), (A0)
    ; Graphics info
    ; Priority 0
    ; Palette line 0
    ; Vertical flip 0
    ; Horizontal flip 0
    ; VRAM tile number = Sprite data address / 0x20 = 0x2800/0x20 = 0x140
    MOVE.W #(0x0140), (A0)
    ; X coordinate in the plane
    MOVE.W #(0x0080), (A0)

    ; Y coordinate in the plane (upper left corner is (128,128) = (0x80, 0x80))
    MOVE.W  #0x0080, (A0)
    ; Size (1x1) and 'next' field (0 -> last entry)
    MOVE.W  #(0x0000 + 0x0000), (A0)
    ; Graphics info
    ; Priority 0
    ; Palette line 0
    ; Vertical flip 0
    ; Horizontal flip 0
    ; VRAM tile number = Sprite data address / 0x20 = 0x2880/0x20 = 0x144
    MOVE.W #(0x0144), (A0)
    ; X coordinate in the plane
    MOVE.W #(0x00C0), (A0)

    MOVE.W #0x80, (0xFFFFFE).L

    ; Enable interrupts
    ANDI  #0xF8FF, SR

stall:
    BRA stall


just_rte:
    RTE


vblank_handler:
    MOVE.W (0xFFFFFE).L, D0
    ADDQ  #3, D0
    MOVE.W D0, 0xFFFFFE
    ; Set sprite table
    ; Set VRAM write to 0x2000
    MOVE.L  #0x60000000, (A1)
    ; Y coordinate in the plane (upper left corner is (128,128) = (0x80, 0x80))
    MOVE.W  D0, (A0)
    ; Size (2x2) and 'next' field (0 -> last entry)
    MOVE.W  #(0x0500 + 0x0001), (A0)
    ; Graphics info
    ; Priority 0
    ; Palette line 0
    ; Vertical flip 0
    ; Horizontal flip 0
    ; VRAM tile number = Sprite data address / 0x20 = 0x2800/0x20 = 0x140
    MOVE.W #(0x0140), (A0)
    ; X coordinate in the plane
    MOVE.W D0, (A0)
    RTE
