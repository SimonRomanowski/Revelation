.equiv rom_base, 0x000000
.equiv ram_base, 0xFF0000
.equiv stack_top, ram_base + 0x100
.equiv amount, 1000

.org 0x000000
    .long stack_top
    .long main

.org 0x400
main:

    MOVE.L #(amount-1), D7
label_try_next:
    MOVE.L D7, -(A7)
    ; Set the initial value of the matrix multiplication
    LEA matrix_a, A0
    LEA matrix_b, A1
    ; Calculate the square root
    BSR matmul
    MOVE.L (A7)+, D7
    DBRA D7, label_try_next

    ; Stop emulation
    STOP #0x2700

matmul:
    ; Multiply two matrices
    ; Input: matrix* a (A0), matrix* b (A1)
    ; Output: matrix* c (A2)
    ; > matrix* c = NULL;
    SUBA.L A2, A2

    ; Width of A has to be height of B
    ; > if (a.width != b.height) return c;
    MOVE.W (2, A0), D0
    CMP.W (A1), D0
    BNE matmul_return

    ; > matrix* c = (matrix*) malloc((4 + 4*a.height*b.width));
    ; A2 = c
    MOVE.W (2, A1), D0
    MULU.W (A0), D0
    ASL.L #2, D0
    ADDQ.W #4, D0
    NEG.L D0  
    MOVE.L D0, A2
    ; Save in A3 for later
    MOVE.L D0, A3

    ; Set width and height
    ; > c.width = b.width;
    ; > c.height = a.height;
    ; Store the width and height of c in D1 and D2
    ; D1 = c.width
    MOVE.W (A1), D1
    MOVE.W D1, (A2)+
    ; D2 = c.height
    MOVE.W (2, A1), D2
    MOVE.W D2, (A2)+

    ; > int i = 0;
    ; D3 = i
    CLR.W D3

    ; Store a.width (= b.height) in D5
    MOVE.W (2, A0), D5

    ; Calculate the elements of c
    ; > for (i = 0; i < c.height; i++) {...}
matmul_loop_row:
    CMP.W D3, D2
    BLE matmul_loop_row_end

    ; Loop body
    ; > int j = 0;
    ; D4 = j
    CLR.W D4

    ; > for (j = 0; j < c.width; j++) {...}
matmul_loop_col:
    CMP.W D4, D1
    BLE matmul_loop_col_end

    ; Loop body

    ; > int32_t sum = 0;
    ; D6 = sum
    CLR.L D6

    ; > int k = 0;
    ; D7 = k
    CLR.W D7

    ; a.values[i][0] = a + 4*a.width*i -> A4
    LEA (4, A0), A4
    MOVE.W D3, D0
    MULU.W D5, D0
    ASL.L #2, D0
    ADDA.L D0, A4
    ; b.values[0][j] = b + 4*j -> A5
    LEA (4, A1), A5
    ADDA.L D4, A5
    ADDA.L D4, A5
    ADDA.L D4, A5
    ADDA.L D4, A5

    ; > for (k = 0; k < a.width; k++) {...}
matmul_loop_elem:
    CMP.W D7, D5
    BLE matmul_loop_elem_end

    ; Loop body

    ; > sum += a[i][k] * b[k][j]
    MOVE.L (A4)+, D0
    ; (2, A5) because of word size
    MULU.W (2, A5), D0
    ADD.L D0, D6

    ; Increment array pointer for b (a already has been incremented)
    ; + b.width*4 for b
    ADDA.L D1, A5
    ADDA.L D1, A5
    ADDA.L D1, A5
    ADDA.L D1, A5

    ; > ... k++) {...}
    ADDQ.W #1, D7
    BRA matmul_loop_elem

matmul_loop_elem_end:

    ; > c[j][i] = sum
    MOVE.L D6, (A2)+

    ; > ... j++) {...}
    ADDQ.W #1, D4
    BRA matmul_loop_col

matmul_loop_col_end:

    ; > ... i++) {...}
    ADDQ.W #1, D3
    BRA matmul_loop_row

matmul_loop_row_end:

    ; > return c;
    ; Restore pointer to c
    MOVE.L A3, A2

matmul_return:
    RTS

; struct matrix {
;   uint16_t width, height;
;   uint32_t[][] values;
; }
matrix_a:
.word 20, 20
.long 1, 1, 5, 6, 6, 4, 5, 4, 2, 1, 3, 0, 2, 9, 3, 2, 7, 3, 0, 9
.long 9, 7, 2, 4, 4, 3, 6, 3, 3, 0, 3, 1, 2, 7, 2, 8, 7, 5, 1, 4
.long 7, 2, 6, 8, 7, 9, 5, 0, 5, 8, 8, 8, 8, 1, 0, 9, 8, 5, 9, 7
.long 5, 3, 6, 4, 9, 2, 3, 1, 8, 9, 4, 7, 5, 9, 1, 4, 6, 8, 2, 6
.long 0, 2, 8, 4, 0, 2, 9, 1, 2, 9, 3, 5, 0, 0, 7, 0, 3, 0, 4, 3
.long 5, 3, 2, 5, 0, 5, 1, 0, 8, 1, 2, 6, 6, 3, 2, 1, 2, 1, 9, 8
.long 0, 0, 9, 1, 4, 5, 7, 3, 3, 9, 4, 0, 3, 9, 3, 3, 1, 1, 4, 6
.long 7, 0, 5, 5, 1, 9, 6, 2, 5, 0, 5, 4, 1, 4, 2, 5, 3, 6, 1, 8
.long 6, 2, 9, 6, 1, 4, 2, 0, 5, 5, 1, 1, 1, 4, 2, 2, 3, 5, 1, 8
.long 1, 2, 6, 2, 6, 2, 3, 3, 7, 8, 7, 9, 0, 5, 0, 3, 9, 2, 6, 5
.long 5, 2, 1, 7, 6, 1, 2, 2, 4, 8, 0, 3, 4, 2, 3, 5, 6, 1, 3, 3
.long 8, 0, 2, 3, 7, 6, 3, 0, 2, 3, 4, 7, 4, 3, 2, 6, 1, 6, 7, 6
.long 5, 8, 3, 4, 8, 3, 9, 9, 6, 3, 4, 5, 2, 4, 2, 1, 5, 4, 7, 3
.long 0, 6, 4, 9, 6, 6, 6, 9, 6, 2, 8, 2, 0, 4, 0, 7, 7, 0, 6, 0
.long 0, 7, 3, 5, 6, 7, 4, 5, 0, 7, 9, 5, 3, 0, 1, 8, 3, 5, 4, 7
.long 2, 3, 8, 6, 6, 3, 9, 2, 5, 3, 9, 6, 7, 8, 5, 1, 6, 0, 2, 1
.long 1, 6, 1, 7, 0, 6, 8, 1, 4, 2, 7, 4, 9, 6, 3, 6, 5, 5, 1, 8
.long 7, 5, 3, 6, 2, 3, 3, 2, 7, 1, 0, 2, 8, 4, 6, 7, 3, 8, 2, 1
.long 2, 7, 8, 0, 1, 8, 2, 6, 4, 7, 3, 6, 0, 7, 6, 6, 0, 6, 5, 5
.long 9, 6, 8, 3, 0, 8, 7, 0, 4, 9, 7, 9, 2, 7, 4, 4, 2, 3, 8, 4
matrix_b:
.word 20, 20
.long 3, 9, 1, 1, 6, 0, 9, 3, 5, 0, 5, 1, 9, 2, 7, 1, 9, 3, 5, 3
.long 7, 0, 2, 7, 1, 3, 8, 1, 0, 8, 2, 1, 1, 3, 5, 9, 9, 1, 1, 7
.long 1, 4, 7, 2, 2, 8, 2, 0, 1, 5, 0, 2, 6, 8, 5, 8, 2, 4, 7, 8
.long 4, 5, 0, 7, 5, 0, 0, 7, 2, 6, 9, 6, 1, 7, 3, 8, 6, 3, 8, 7
.long 9, 4, 4, 0, 9, 5, 8, 6, 6, 0, 6, 9, 5, 3, 6, 3, 5, 8, 3, 8
.long 5, 6, 4, 7, 8, 8, 4, 5, 2, 5, 6, 7, 5, 3, 0, 2, 0, 7, 4, 8
.long 9, 6, 3, 0, 3, 3, 2, 5, 7, 5, 9, 5, 7, 5, 7, 6, 4, 2, 6, 7
.long 1, 2, 9, 6, 1, 0, 3, 8, 8, 3, 3, 9, 8, 9, 7, 3, 5, 4, 1, 7
.long 8, 8, 8, 2, 6, 3, 1, 1, 8, 7, 1, 5, 0, 6, 7, 7, 7, 7, 4, 6
.long 3, 0, 7, 6, 8, 6, 1, 8, 8, 1, 5, 7, 8, 5, 0, 0, 8, 4, 4, 4
.long 5, 0, 7, 4, 6, 6, 3, 0, 9, 7, 4, 8, 5, 3, 3, 3, 4, 2, 4, 5
.long 1, 6, 1, 5, 2, 9, 5, 1, 8, 8, 4, 2, 0, 1, 8, 1, 3, 1, 9, 2
.long 9, 9, 4, 8, 5, 1, 4, 1, 8, 4, 0, 2, 7, 3, 1, 5, 9, 7, 6, 1
.long 0, 8, 2, 4, 7, 6, 0, 8, 4, 9, 6, 0, 2, 9, 1, 3, 7, 3, 4, 7
.long 7, 5, 9, 6, 9, 9, 1, 4, 9, 0, 1, 6, 0, 6, 6, 1, 0, 1, 3, 1
.long 4, 4, 8, 6, 5, 2, 7, 6, 0, 9, 3, 1, 0, 8, 6, 3, 3, 8, 1, 6
.long 0, 5, 8, 3, 6, 7, 6, 2, 9, 4, 1, 0, 6, 3, 2, 5, 5, 7, 3, 1
.long 8, 8, 0, 2, 7, 8, 5, 3, 5, 3, 8, 0, 1, 0, 8, 9, 3, 2, 0, 7
.long 4, 5, 2, 0, 9, 7, 4, 0, 8, 2, 4, 4, 9, 7, 3, 9, 1, 7, 0, 0
.long 1, 6, 2, 1, 5, 2, 4, 8, 5, 3, 2, 2, 3, 8, 8, 3, 3, 9, 0, 6
