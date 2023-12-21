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
    ; Set plane A name table to VRAM address 0x4000
    MOVE.W  #0x8210, (A1)
    ; Set plane B name table  to VRAM address 0x2000
    MOVE.W  #0x8401, (A1)
    ; Set background color to first index in CRAM
    MOVE.W  #0x8700, (A1)
    ; Set horizontal scroll mode to 0 (whole screen) and vertical scroll mode
    ; to 1 (16 pixel strips)
    MOVE.W  #0x8B04, (A1)
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
    ; Set VRAM write to 0x2800
    MOVE.L  #0x68000000, (A1)

    ; Tile #0 (red X)
    MOVE.L  #0x11000011, (A0)
    MOVE.L  #0x01100110, (A0)
    MOVE.L  #0x00111100, (A0)
    MOVE.L  #0x00011000, (A0)
    MOVE.L  #0x00011000, (A0)
    MOVE.L  #0x00111100, (A0)
    MOVE.L  #0x01100110, (A0)
    MOVE.L  #0x11000011, (A0)

    ; Tile #1 (blue +)
    MOVE.L  #0x00030000, (A0)
    MOVE.L  #0x00030000, (A0)
    MOVE.L  #0x00030000, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x00030000, (A0)
    MOVE.L  #0x00030000, (A0)
    MOVE.L  #0x00030000, (A0)
    MOVE.L  #0x00030000, (A0)

    ; Set Plane B nametable
    ; Set VRAM write to 0x2000
    MOVE.L  #0x60000000, (A1)
    ; Set nametable B
    ; Repeat 0x400 times
    MOVE.W  #0x3FF, D0
set_nametable_b:
    ; Set nametable entry to point to tile #0
    MOVE.W  #0x0140, (A0)
    DBF D0, set_nametable_b

    ; Set Plane A nametable
    ; Set VRAM write to 0x4000
    MOVE.L  #0x40000001, (A1)
    ; Set nametable A
    ; Repeat 0x400 times
    MOVE.W  #0x3FF, D0
set_nametable_a:
    ; Set nametable entry to point to tile #1
    MOVE.W  #0x0141, (A0)
    DBF D0, set_nametable_a

    ; Enable interrupts
    ANDI  #0xF8FF, SR

    MOVE.W #1, (0xFF1234).L
stall:
    TST.W (0xFF1234).L
    BNE stall
    ; Increment the memory buffer for our vertical scroll values
    JSR vertical_scroll_increment
    MOVE.W #1, (0xFF1234).L
    BRA stall


vertical_scroll_increment:
    ; Select our memory buffer for the scroll value
    LEA (0xFF0000).L, A3
    ; D5 is out counter. We write 2 strips at a time
    MOVE.W #0x3, D5
    ; D6 is our increment value
    MOVE.L #0x00020001, D6

vertical_scroll_increment_loop:
    ; 4 adjacent 16 pixel strips will have the same value
    ADD.L D6, (A3)+
    ADD.L D6, (A3)+
    ADD.L D6, (A3)+
    ADD.L D6, (A3)+
    ADDI.L #0x00020001, D6
    DBF D5, vertical_scroll_increment_loop
    RTS


just_rte:
    RTE


vblank_handler:
    ; Select VSRAM address 0
    MOVE.L  #0x40000010, (A1)
    ; Select our memory buffer for the scroll value
    LEA (0xFF0000).L, A3
    ; We need to move 64 bytes = 16 long words
    MOVE.W #0xF, D5

vblank_handler_loop:
    MOVE.L (A3)+, (A0)
    DBF D5, vblank_handler_loop

    MOVE.W #0, (0xFF1234).L
    RTE
