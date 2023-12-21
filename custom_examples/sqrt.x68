.equiv rom_base, 0x000000
.equiv ram_base, 0xFF0000
.equiv stack_top, ram_base + 0x100
.equiv input, 0x6A2170C5
.equiv amount, 100000

.org 0x000000
    .long stack_top
    .long main

.org 0x400
main:

    MOVE.L #(amount-1), D6
label_try_next:
    ; Set the initial value of the square root calculation
    MOVE.L #input, D0
    ; Calculate the square root
    BSR sqrt
    DBRA D6, label_try_next

    ; Stop emulation
    STOP #0x2700

sqrt:
    ; Based on the 'Binary numeral system (base 2)' square root C algorithm
    ; on https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Binary_numeral_system_(base_2)

    ; D0 = n
    ; D1 = x
    ; > int32_t x = n;
    MOVE.L D0, D1
    ; D2 = c
    ; > int32_t c = 0;
    CLR.L D2
    ; D3 = d
    ; > int32_t d = 1 << 30;
    MOVE.L #0x40000000, D3

    ; > while (d > n) {...}
label_init_d:
    ; Evaluate 'd > n'
    CMP.L D0, D3  ; Calculates d - n
    ; Break when the result is <= 0
    BLE label_init_d_end

    ; Loop body
    ; > d = d >> 2;
    ASR.L #2, D3

    ; Next iteration
    BRA label_init_d

label_init_d_end:

    ; > while (d != 0) {...}
label_calculation:
    ; Evaluate 'd != 0'
    TST.L D3
    ; Brea when the result is = 0
    BEQ label_calculation_end

    ; Loop body
    ; > if (x >= c + d) {...}
    ; Evaluate 'c + d'
    MOVE.L D3, D4
    ADD.L D2, D4
    ; Evaluate 'x >= c + d'
    ; Calculate x - (c + d)
    SUB.L D1, D4  ; (c + d) - x -> D4
    NEG.L D4  ; -D4 = x - (c + d) -> D4
    ; Go to else if result < 0
    BLT label_else

    ; if body
    ; > x = x - (c + d)
    MOVE.L D4, D1
    ; > c = (c >> 1) + d;
    ASR.L #1, D2  ; c >> 1
    ADD.L D3, D2  ; + d

    ; Skip else body
    BRA label_after_if_else

    label_else:
    ; > c = c >> 1;
    ASR.L #1, D2

    ; else body

    label_after_if_else:

    ; > d = d >> 2;
    ASR.L #2, D3

    ; Next iteration
    BRA label_calculation

label_calculation_end:

    ; > return c
    ; We place the return value in D0
    MOVE.L D2, D0
    RTS
