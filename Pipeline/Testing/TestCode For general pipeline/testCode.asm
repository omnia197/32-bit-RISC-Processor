set R1, 0x0384
set R8, 0x1234
sset R8, 0x5678
addi R5, R1, 20
xor R3, R1, R5
add R4, R8, R3
lw R1, 0(R0)
lw R2, 1(R0)
lw R3, 2(R0)
sub, R4, R4, R4
loop1: 
add R4, R2, R4
slt R6, R2, R3
Beq R6, R0, done
add R2, R1, R2
Beq R0, R0, loop1
done: sw R4, 0(R0)
mul R10, R2, R3
Srl R14, R10, R4
Sra R15, R10, R4
RORI R26, R14, 5
JALR R7, R0, func 
set R9, 0x4545
set R10, 0x4545
BGE R10, R9, L1
andi R23, R1, 0xffff
L1: BEQ R0, R0, L1
func: OR R5, R2, R3
lw R1, 0(R0)
LW R2, 5(R1)
LW R3, 6(R1)
AND R4, R2, R3
SW R4, 0(R0)
JALR R0, R7, 0 