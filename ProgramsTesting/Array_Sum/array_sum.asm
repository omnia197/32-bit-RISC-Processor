SET R1, 0x01   #base
SET R2, 5        #size
SET R3, 0        #sum
        
loop:
LW R4, 0(R1) 
ADD R3, R3, R4 
ADDI R1, R1, 1 
ADDI R2, R2, -1
BNE R2, R0, loop

