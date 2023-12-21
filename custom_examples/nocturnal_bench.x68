.equiv rom_base, 0x000000
.equiv ram_base, 0xFF0000
.equiv stack_top, ram_base + 0x100

.equiv VdpCtrl, 0xC00004  ; VDP control port
.equiv VdpData, 0xC00000  ; VDP data port

.equiv VRAM_ADDR_CMD, 0x40000000
.equiv CRAM_ADDR_CMD, 0xC0000000
.equiv VSRAM_ADDR_CMD, 0x40000010

.macro SetXramAddr addr, cmd
    MOVE.L  #((((\addr)&0x3FFF)<<16))|(((\addr)&0xC000)>>14)|(\cmd), (A1)
.endm

.macro SetVramAddr addr
    SetXramAddr \addr, VRAM_ADDR_CMD
.endm

.macro SetCramAddr addr
    SetXramAddr \addr, CRAM_ADDR_CMD
.endm

.macro SetVsramAddr addr
    SetXramAddr \addr, VSRAM_ADDR_CMD
.endm

.macro SelectTableEntry table, x, y
    SetVramAddr (\table + \x * 2 + \y * 0x80)
.endm

.macro DrawHouseSmall table, x, y
    ; (x, y) -> Lower left corner of the whole image
    SelectTableEntry (\table), (\x), (\y - 12)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x0006, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x0007, (A0)
    MOVE.W  #0x0000, (A0)

    SelectTableEntry (\table), (\x), (\y - 11)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)
    MOVE.W  #0x0000, (A0)

    SelectTableEntry (\table), (\x), (\y - 10)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)
    MOVE.W  #0x0000, (A0)

    SelectTableEntry (\table), (\x), (\y - 9)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)
    MOVE.W  #0x0000, (A0)

    SelectTableEntry (\table), (\x), (\y - 8)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0003, (A0)
    MOVE.W  #0x0000, (A0)

    SelectTableEntry (\table), (\x), (\y - 7)
    MOVE.W  #0x0000, (A0)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)
    MOVE.W  #0x0000, (A0)

    SelectTableEntry (\table), (\x), (\y - 6)
    MOVE.W  #0x0006, (A0)
    MOVE.W  #0x0001, (A0)
    MOVE.W  #0x0001, (A0)
    MOVE.W  #0x0001, (A0)
    MOVE.W  #0x0001, (A0)
    MOVE.W  #0x0007, (A0)

    SelectTableEntry (\table), (\x), (\y - 5)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 4)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 3)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 2)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 1)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0003, (A0)
.endm

.macro DrawHouseTall table, x, y
    ; (x, y) -> Lower left corner of the whole image
    SelectTableEntry (\table), (\x), (\y - 18)
    MOVE.W  #0x0006, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x0007, (A0)

    SelectTableEntry (\table), (\x), (\y - 17)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 16)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 15)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 14)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 13)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 12)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 11)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 10)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 9)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 8)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 7)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 6)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 5)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 4)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 3)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 2)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 1)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 0)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)
.endm

.macro DrawHouseWide table, x, y
    ; (x, y) -> Lower left corner of the whole image
    SelectTableEntry (\table), (\x), (\y - 10)
    MOVE.W  #0x0006, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x000C, (A0)
    MOVE.W  #0x0007, (A0)

    SelectTableEntry (\table), (\x), (\y - 9)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 8)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 7)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 6)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 5)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 4)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 3)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 2)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y - 1)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)

    SelectTableEntry (\table), (\x), (\y)
    MOVE.W  #0x0002, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0005, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0004, (A0)
    MOVE.W  #0x0003, (A0)
.endm

.org 0x000000
    .long    stack_top
    .long    reset

.org 0x78
    .long vblank_handler

.org 0x100
    .byte "SEGA"

.org 0x400
reset:
    ; TMSS check
    MOVE.L  #"SEGA", (0xA14000).L
    ; Disable interrupts
    MOVE.W  #0x2700, SR
    ; VDP setup
    LEA     VdpData, A0
    LEA     VdpCtrl, A1
    ; Set VDP to normal operation
    MOVE.W  #0x8004, (A1)
    ; Set display mode to Mega Drive (instead of Master System) and enable
    ; vertical interrupts and DMA
    MOVE.W  #0x8164, (A1)
    ; Set plane A name table to VRAM address 0x4000
    MOVE.W  #0x8210, (A1)
    ; Set window plane name table to VRAM address 0x6000
    MOVE.W  #0x8318, (A1)
    ; Set plane B name table to VRAM address 0x2000
    MOVE.W  #0x8401, (A1)
    ; Set sprite table to VRAM address 0x8000
    MOVE.W  #0x8540, (A1)
    ; Set background color to first index in CRAM
    MOVE.W  #0x8700, (A1)
    ; Set scroll mode to mode 2 (8 pixel rows)
    MOVE.W  #0x8B02, (A1)
    ; Enable 320 pixel wide mode
    MOVE.W  #0x8C81, (A1)
    ; Set horizontal scroll data address to 0x9000 (0x9000 / 0x400 = 0x24)
    MOVE.W  #0x8D24, (A1)
    ; Auto increment value for the VDP after each read or write -> 2
    MOVE.W  #0x8F02, (A1)
    ; Set plane size to 512x256
    MOVE.W  #0x9001, (A1)
    ; Set window horizontal position
    MOVE.W  #(0x9100 + 0), (A1)
    ; Set window vertical position
    MOVE.W  #(0x9200 + 1), (A1)


main:
    ; Set colors
    SetCramAddr 0
    ; Palette 0
    MOVE.W  #0x0202, (A0)  ; 0
    MOVE.W  #0x0444, (A0)  ; 1
    MOVE.W  #0x0666, (A0)  ; 2
    MOVE.W  #0x0AAA, (A0)  ; 3
    MOVE.W  #0x0EEE, (A0)  ; 4
    MOVE.W  #0x04CC, (A0)  ; 5
    MOVE.W  #0x0420, (A0)  ; 6
    MOVE.W  #0x0842, (A0)  ; 7
    MOVE.W  #0x0C64, (A0)  ; 8
    MOVE.W  #0x08CC, (A0)  ; 9
    MOVE.W  #0x06AA, (A0)  ; A
    MOVE.W  #0x0808, (A0)  ; 0
    MOVE.W  #0x0202, (A0)  ; 0
    MOVE.W  #0x0CC0, (A0)  ; D
    MOVE.W  #0x0000, (A0)  ; E
    MOVE.W  #0x0000, (A0)  ; F -unused-
    ; Palette 1
    MOVE.W  #0x0000, (A0)  ; 0 -unused-
    MOVE.W  #0x0000, (A0)  ; 1
    MOVE.W  #0x0000, (A0)  ; 2

    ; Set tiles
    SetVramAddr 0x20

    ; Tile #1
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22222222, (A0)

    ; Tile #2
    MOVE.L  #0x11222222, (A0)
    MOVE.L  #0x11222222, (A0)
    MOVE.L  #0x11222222, (A0)
    MOVE.L  #0x11222222, (A0)
    MOVE.L  #0x11222222, (A0)
    MOVE.L  #0x11222222, (A0)
    MOVE.L  #0x11222222, (A0)
    MOVE.L  #0x11222222, (A0)

    ; Tile #3
    MOVE.L  #0x22222211, (A0)
    MOVE.L  #0x22222211, (A0)
    MOVE.L  #0x22222211, (A0)
    MOVE.L  #0x22222211, (A0)
    MOVE.L  #0x22222211, (A0)
    MOVE.L  #0x22222211, (A0)
    MOVE.L  #0x22222211, (A0)
    MOVE.L  #0x22222211, (A0)

    ; Tile #4
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22555522, (A0)
    MOVE.L  #0x22555522, (A0)
    MOVE.L  #0x22555522, (A0)
    MOVE.L  #0x22555522, (A0)
    MOVE.L  #0x22555522, (A0)
    MOVE.L  #0x22555522, (A0)
    MOVE.L  #0x22222222, (A0)

    ; Tile #5
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22666622, (A0)
    MOVE.L  #0x22666622, (A0)
    MOVE.L  #0x22666622, (A0)
    MOVE.L  #0x22666622, (A0)
    MOVE.L  #0x22666622, (A0)
    MOVE.L  #0x22666622, (A0)
    MOVE.L  #0x22222222, (A0)

    ; Tile #6
    MOVE.L  #0x00001111, (A0)
    MOVE.L  #0x00111111, (A0)
    MOVE.L  #0x01112222, (A0)
    MOVE.L  #0x01122222, (A0)
    MOVE.L  #0x11222222, (A0)
    MOVE.L  #0x11222222, (A0)
    MOVE.L  #0x11222222, (A0)
    MOVE.L  #0x11222222, (A0)

    ; Tile #7
    MOVE.L  #0x11110000, (A0)
    MOVE.L  #0x11111100, (A0)
    MOVE.L  #0x22221110, (A0)
    MOVE.L  #0x22222110, (A0)
    MOVE.L  #0x22222211, (A0)
    MOVE.L  #0x22222211, (A0)
    MOVE.L  #0x22222211, (A0)
    MOVE.L  #0x22222211, (A0)

    ; Tile #8
    MOVE.L  #0x00000001, (A0)
    MOVE.L  #0x00000011, (A0)
    MOVE.L  #0x00000112, (A0)
    MOVE.L  #0x00001122, (A0)
    MOVE.L  #0x00011222, (A0)
    MOVE.L  #0x00112222, (A0)
    MOVE.L  #0x01122222, (A0)
    MOVE.L  #0x11222222, (A0)

    ; Tile #9
    MOVE.L  #0x00011222, (A0)
    MOVE.L  #0x00011222, (A0)
    MOVE.L  #0x00112222, (A0)
    MOVE.L  #0x00112222, (A0)
    MOVE.L  #0x01122222, (A0)
    MOVE.L  #0x01122222, (A0)
    MOVE.L  #0x11222222, (A0)
    MOVE.L  #0x11222222, (A0)

    ; Tile #A
    MOVE.L  #0x00000001, (A0)
    MOVE.L  #0x00000001, (A0)
    MOVE.L  #0x00000011, (A0)
    MOVE.L  #0x00000011, (A0)
    MOVE.L  #0x00000112, (A0)
    MOVE.L  #0x00000112, (A0)
    MOVE.L  #0x00001122, (A0)
    MOVE.L  #0x00001122, (A0)

    ; Tile #B -unused-
    MOVE.L  #0x22211000, (A0)
    MOVE.L  #0x22211000, (A0)
    MOVE.L  #0x22221100, (A0)
    MOVE.L  #0x22221100, (A0)
    MOVE.L  #0x22222110, (A0)
    MOVE.L  #0x22222110, (A0)
    MOVE.L  #0x22222211, (A0)
    MOVE.L  #0x22222211, (A0)

    ; Tile #C
    MOVE.L  #0x11111111, (A0)
    MOVE.L  #0x11111111, (A0)
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22222222, (A0)
    MOVE.L  #0x22222222, (A0)

    ; Tile #D
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)

    ; Tile #E
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)

    ; Tile #F
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x34444443, (A0)
    MOVE.L  #0x34444443, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)
    MOVE.L  #0x33333333, (A0)

    ; Tile #10
    MOVE.L  #0x66666666, (A0)
    MOVE.L  #0x68888888, (A0)
    MOVE.L  #0x67777777, (A0)
    MOVE.L  #0x67777777, (A0)
    MOVE.L  #0x66666666, (A0)
    MOVE.L  #0x88886888, (A0)
    MOVE.L  #0x77776777, (A0)
    MOVE.L  #0x77776777, (A0)

    ; Tile #11
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000099, (A0)
    MOVE.L  #0x00000999, (A0)
    MOVE.L  #0x00009999, (A0)
    MOVE.L  #0x00099999, (A0)
    MOVE.L  #0x00999999, (A0)
    MOVE.L  #0x09999999, (A0)
    MOVE.L  #0x09999999, (A0)

    ; Tile #12
    MOVE.L  #0x09999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x9999AA99, (A0)
    MOVE.L  #0x9999AA99, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x09999999, (A0)

    ; Tile #13
    MOVE.L  #0x09999999, (A0)
    MOVE.L  #0x09999999, (A0)
    MOVE.L  #0x00999999, (A0)
    MOVE.L  #0x00099999, (A0)
    MOVE.L  #0x00009999, (A0)
    MOVE.L  #0x00000999, (A0)
    MOVE.L  #0x00000099, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #14
    MOVE.L  #0x09999990, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x9999AAAA, (A0)
    MOVE.L  #0x999AAAAA, (A0)
    MOVE.L  #0x999AAAAA, (A0)
    MOVE.L  #0x9999AAAA, (A0)

    ; Tile #15
    MOVE.L  #0x9999AAAA, (A0)
    MOVE.L  #0x999999AA, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99AA9999, (A0)

    ; Tile #16
    MOVE.L  #0x9AAAA999, (A0)
    MOVE.L  #0x9AAAA999, (A0)
    MOVE.L  #0x99AA9999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x09999990, (A0)

    ; Tile #17
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x99000000, (A0)
    MOVE.L  #0x99900000, (A0)
    MOVE.L  #0x99990000, (A0)
    MOVE.L  #0xA9999000, (A0)
    MOVE.L  #0xAA999900, (A0)
    MOVE.L  #0xAA999990, (A0)
    MOVE.L  #0xAA999990, (A0)

    ; Tile #18
    MOVE.L  #0xAA999990, (A0)
    MOVE.L  #0xA9999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99999999, (A0)
    MOVE.L  #0x99A99999, (A0)
    MOVE.L  #0x99999990, (A0)

    ; Tile #19
    MOVE.L  #0x99999990, (A0)
    MOVE.L  #0x99999990, (A0)
    MOVE.L  #0x99999900, (A0)
    MOVE.L  #0x99999000, (A0)
    MOVE.L  #0x99990000, (A0)
    MOVE.L  #0x99900000, (A0)
    MOVE.L  #0x99000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #1A
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x000000CC, (A0)
    MOVE.L  #0x00000CBD, (A0)
    MOVE.L  #0x00CCCBDD, (A0)
    MOVE.L  #0x0CBBBBBB, (A0)
    MOVE.L  #0x0CBBEBBB, (A0)
    MOVE.L  #0x00CE4ECC, (A0)
    MOVE.L  #0x0000E000, (A0)

    ; Tile #1B
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0xCCCCCC00, (A0)
    MOVE.L  #0xBBBDDBC0, (A0)
    MOVE.L  #0xBBBDDBBC, (A0)
    MOVE.L  #0xBBBBBBBC, (A0)
    MOVE.L  #0xBBBEBBBC, (A0)
    MOVE.L  #0xCCE4ECC0, (A0)
    MOVE.L  #0x000E0000, (A0)

    ; Start ASCII digits
    SetVramAddr (0x20*0x30)

    ; Tile #30 0
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x04000044, (A0)
    MOVE.L  #0x04004404, (A0)
    MOVE.L  #0x04040004, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #31 1
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00044000, (A0)
    MOVE.L  #0x00404000, (A0)
    MOVE.L  #0x04004000, (A0)
    MOVE.L  #0x00004000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #32 2
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x04000044, (A0)
    MOVE.L  #0x00004400, (A0)
    MOVE.L  #0x00440000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #33 3
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00044440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #34 4
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000440, (A0)
    MOVE.L  #0x00044040, (A0)
    MOVE.L  #0x00400040, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x00000040, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #35 5
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x00000004, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #36 6
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00444444, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #37 7
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x00000040, (A0)
    MOVE.L  #0x00000400, (A0)
    MOVE.L  #0x00004000, (A0)
    MOVE.L  #0x00040000, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #38 8
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #39 9
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00444444, (A0)
    MOVE.L  #0x00000004, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Start ASCII digits
    SetVramAddr (0x20*0x41)

    ; Tile #41 A
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00044400, (A0)
    MOVE.L  #0x00400040, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #42 B
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #43 C
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00444444, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x00444444, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #44 D
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #45 E
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #46 F
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #47 G
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00444444, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04000444, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #48 H
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #49 I
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x00004000, (A0)
    MOVE.L  #0x00004000, (A0)
    MOVE.L  #0x00004000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #4A J
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x00000004, (A0)
    MOVE.L  #0x00000004, (A0)
    MOVE.L  #0x00000004, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #4B K
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000040, (A0)
    MOVE.L  #0x04444400, (A0)
    MOVE.L  #0x04000040, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #4C L
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #4D M
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04400044, (A0)
    MOVE.L  #0x04040404, (A0)
    MOVE.L  #0x04004004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #4E N
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04400004, (A0)
    MOVE.L  #0x04040004, (A0)
    MOVE.L  #0x04004004, (A0)
    MOVE.L  #0x04000404, (A0)
    MOVE.L  #0x04000044, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #4F O
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #50 P
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #51 Q
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000404, (A0)
    MOVE.L  #0x04000044, (A0)
    MOVE.L  #0x00444444, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #52 R
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x04000040, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #53 S
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00444444, (A0)
    MOVE.L  #0x04000000, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x00000004, (A0)
    MOVE.L  #0x04444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #54 T
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x00004000, (A0)
    MOVE.L  #0x00004000, (A0)
    MOVE.L  #0x00004000, (A0)
    MOVE.L  #0x00004000, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #55 U
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00444440, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #56 V
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00400040, (A0)
    MOVE.L  #0x00400040, (A0)
    MOVE.L  #0x00044400, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #57 W
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x04004004, (A0)
    MOVE.L  #0x04040404, (A0)
    MOVE.L  #0x04400044, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #58 X
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00400040, (A0)
    MOVE.L  #0x00044400, (A0)
    MOVE.L  #0x00400040, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #59 Y
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04000004, (A0)
    MOVE.L  #0x00400040, (A0)
    MOVE.L  #0x00044400, (A0)
    MOVE.L  #0x00004000, (A0)
    MOVE.L  #0x00004000, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Tile #5A Z
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x00000044, (A0)
    MOVE.L  #0x00004400, (A0)
    MOVE.L  #0x00440000, (A0)
    MOVE.L  #0x04444444, (A0)
    MOVE.L  #0x00000000, (A0)
    MOVE.L  #0x00000000, (A0)

    ; Set Plane B nametable
    ; Set VRAM write to (x, y)
    ; SetVramAddr (0x2000 + x * 2 + y * 0x80)
    ; Moon (0x24, 0x1)
    SetVramAddr (0x2000 + 0x24 * 2 + 1 * 0x80)
    MOVE.W  #0x0011, (A0)
    MOVE.W  #0x0014, (A0)
    MOVE.W  #0x0017, (A0)
    SetVramAddr (0x2000 + 0x24 * 2 + 2 * 0x80)
    MOVE.W  #0x0012, (A0)
    MOVE.W  #0x0015, (A0)
    MOVE.W  #0x0018, (A0)
    SetVramAddr (0x2000 + 0x24 * 2 + 3 * 0x80)
    MOVE.W  #0x0013, (A0)
    MOVE.W  #0x0016, (A0)
    MOVE.W  #0x0019, (A0)

    ; Hill
    SetVramAddr (0x2000 + 0x25 * 2 + 5 * 0x80)
    MOVE.W  #0x2008, (A0)
    MOVE.W  #0x2808, (A0)
    SetVramAddr (0x2000 + 0x24 * 2 + 6 * 0x80)
    MOVE.W  #0x200A, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2808, (A0)
    SetVramAddr (0x2000 + 0x24 * 2 + 7 * 0x80)
    MOVE.W  #0x2009, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2808, (A0)
    SetVramAddr (0x2000 + 0x23 * 2 + 8 * 0x80)
    MOVE.W  #0x200A, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2808, (A0)
    SetVramAddr (0x2000 + 0x23 * 2 + 9 * 0x80)
    MOVE.W  #0x2009, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x280A, (A0)
    SetVramAddr (0x2000 + 0x22 * 2 + 0xA * 0x80)
    MOVE.W  #0x2008, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2809, (A0)
    SetVramAddr (0x2000 + 0x21 * 2 + 0xB * 0x80)
    MOVE.W  #0x2008, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2808, (A0)
    SetVramAddr (0x2000 + 0x20 * 2 + 0xC * 0x80)
    MOVE.W  #0x200A, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2808, (A0)
    SetVramAddr (0x2000 + 0x20 * 2 + 0xD * 0x80)
    MOVE.W  #0x2009, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2001, (A0)
    MOVE.W  #0x2808, (A0)
    ; Fill 8 lines with black
    SetVramAddr (0x2000 + 0 * 2 + 0xE * 0x80)
    MOVE.W  #(8 * 64 - 1), D0
label_bg_fill:
    MOVE.W  #0x2001, (A0)
    DBRA    D0, label_bg_fill

    ; Set Plane A nametable
    ; Draw Houses
    DrawHouseSmall 0x4000, 0, 21
    DrawHouseTall 0x4000, 7, 21
    DrawHouseWide 0x4000, 14, 21
    DrawHouseSmall 0x4000, (25+0), 21
    DrawHouseTall 0x4000, (25+7), 21
    DrawHouseWide 0x4000, (25+14), 21
    DrawHouseSmall 0x4000, (50+0), 21
    DrawHouseTall 0x4000, (50+7), 21
    ; Draw Wall
    SelectTableEntry 0x4000, 0, 22
    MOVE.W  #(3 * 64 - 1), D0
label_fg_wall:
    MOVE.W  #0x0010, (A0)
    DBRA    D0, label_fg_wall
    ; Draw Street
    MOVE.W  #(1 * 64 - 1), D0
label_fg_street_0:
    MOVE.W  #0x000E, (A0)
    DBRA    D0, label_fg_street_0
    MOVE.W  #31, D0
label_fg_street_1:
    MOVE.W  #0x000E, (A0)
    MOVE.W  #0x000F, (A0)
    DBRA    D0, label_fg_street_1
    MOVE.W  #(1 * 64 - 1), D0
label_fg_street_2:
    MOVE.W  #0x000E, (A0)
    DBRA    D0, label_fg_street_2

    ; Set Window plane nametable
    SetVramAddr (0x6000)
    MOVE.W  #"S", (A0)
    MOVE.W  #"P", (A0)
    MOVE.W  #"E", (A0)
    MOVE.W  #"E", (A0)
    MOVE.W  #"D", (A0)
    MOVE.W  #0, (A0)
    MOVE.W  #"2", (A0)
    MOVE.W  #"0", (A0)
    MOVE.W  #"0", (A0)
    MOVE.W  #"K", (A0)
    MOVE.W  #"M", (A0)
    MOVE.W  #"H", (A0)

    ; Set sprite table
    SetVramAddr 0x8000
    MOVE.W  #0x0148, (A0)
    MOVE.W  #0x0400, (A0)
    MOVE.W  #0x081A, (A0)
    MOVE.W  #0x0110, (A0)

    ; Initialize scroll counter
    MOVE.L #0, (0xFF1234).L
    ; Initialize benchmark counter
    MOVE.L #0, (0xFF1238).L

    ; Enable interrupts
    ANDI  #0xF8FF, SR

stall:
    BRA stall


just_rte:
    RTE


vblank_handler:
    ; Increment the scroll counter
    MOVE.L (0xFF1234).L, D0
    SUBI.L #17, D0
    MOVE.L (0xFF1238).L, D7
    ; Benchmark code
    ; Runs for 60*x frames, where x is the amount of seconds of runtime
    CMPI.L #(60*30), D7
    BLE keep_going
    STOP #0x2700
keep_going:
    ADDQ #1, D7
    MOVE.L D7, (0xFF1238).L
    ; End benchmark
    MOVE.L D0, (0xFF1234).L
    
    ; Enable DMA
    MOVE.W  #0x8174, (A1)
    ; Prepare DMA
    MOVE.W  #0x8F02, (A1)  ; Auto increment value
    MOVE.W #0x9300+((0x380>>1)&0xFF), (A1)
    MOVE.W #0x9400+(((0x380>>1)&0xFF00)>>8), (A1)
    MOVE.W #0x9500+((0xFF2000>>1)&0xFF), (A1)
    MOVE.W #0x9600+(((0xFF2000>>1)&0xFF00)>>8), (A1)
    MOVE.W #0x9700+(((0xFF2000>>1)&0x7F0000)>>16), (A1)
    ; Copy the scroll data (0xFF2000) to VRAM (0x9000)
    MOVE.L #0x40000080+((0x9000&0x3FFF)<<16)+((0x9000&0xC000)>>14), (A1)
    ; Disable DMA
    MOVE.W  #0x8164, (A1)

    ; Write the new scroll data
    ; D0 - Moon scroll
    ; D1 - BG scroll
    ; D2 - Houses scroll
    ; D3 - Street scroll
    LSR.L #2, D0
    MOVE.W D0, D3
    LSR.L #2, D0
    MOVE.W D0, D2
    LSR.L #2, D0
    MOVE.W D0, D1
    LSR.L #2, D0

    LEA (0xFF2000).L, A2

    MOVE #(4 - 1), D4
label_scroll_moon:
    MOVE.W D2, (A2)
    MOVE.W D0, (2, A2)
    ADDA #0x20, A2
    DBRA D4, label_scroll_moon

    MOVE #(18 - 1), D4
label_scroll_bg:
    MOVE.W D2, (A2)
    MOVE.W D1, (2, A2)
    ADDA #0x20, A2
    DBRA D4, label_scroll_bg

    MOVE #(6 - 1), D4
label_scroll_street:
    MOVE.W D3, (A2)
    ADDA #0x20, A2
    DBRA D4, label_scroll_street

    RTE
