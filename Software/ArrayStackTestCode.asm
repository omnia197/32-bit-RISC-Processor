SET R1, 5 #size of array
SET R2, 0X00000000
SET R30, 0XFFFFF #setting the stack pointer
ADDI R30, R30, -2 #size of the stack
SW R31, 1(R30) #first element RA
SW R20, 0(R30) #second element ARRAY ELEMENT
SEQ R3, R1, R0
BEQ, R3, R0, zero_size
LW R20, 0(R2)
ADDI R2, R2, 1
ADDI R1, R1, -1
BNE R1, R0, LOOP





