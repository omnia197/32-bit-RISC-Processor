#testing all 37 instructions of our design 

        SET R1, 0x1000     
        SET R2, 10          
        SET R3, 0          
        SSET R3, 0xABCD 

#arrays
arr_loop:
        SW R2, 0(R1)        
        ADDI R1, R1, 1     
        ADDI R2, R2, -1    
        BNE R2, R0, arr_loop

#arithmetic
        SET R4, 5
        SET R5, 3
        ADD R6, R4, R5      
        SUB R7, R4, R5     
        MUL R8, R4, R5     
        ADDI R9, R4, 10     
        ADDI R10, R4, -2   

#logical
        #r_type
        SET R11, 0x1010
        SET R12, 0x1100
        AND R13, R11, R12  
        OR R14, R11, R12   
        XOR R15, R11, R12 
        NOR R16, R11, R12  
        #I_type with immediate values
        ANDI R17, R11, 0x0011
        ORI R18, R11, 0x0011 
        XORI R19, R11, 0x0011 
        NORI R20, R11, 0x0011 

#shifting
        #r_type
        SET R21, 0x0001
        SET R22, 2        
        SLL R23, R21, R22  
        SRL R24, R21, R22   
        SRA R25, R21, R22   
        ROR R26, R21, R22  
        #I_type with immediate values
        SLLI R27, R21, 3   
        SRLI R28, R21, 1   
        SRAI R29, R21, 1   
        RORI R30, R21, 1   

#slt functions
        #r_type
        SLT R31, R4, R5     
        SLTU R1, R4, R5    
        SEQ R2, R4, R5      
        #I_type with immdediate values 
        SLTI R3, R4, 3     
        SLTIU R4, R4, 3     
        SEQI R5, R4, 5     

#using memory
        SET R1, 0x1000      
        LW R6, 0(R1)        
        SW R6, 0x2000(R0)  

#branches
        SET R1, 0
        SET R2, 5
loop:   ADDI R1, R1, 1
        BLT R1, R2, loop    
        SET R1, 0
        BGE R1, R2, break   
        ADDI R1, R1, 100   
        
break:   BNE R1, R0, target  
        ADDI R1, R1, 1     
        
target: BLTU R0, R2, next   
        ADDI R1, R1, 1      
        
next:   BGEU R2, R0, final 
        ADDI R1, R1, 1      

#JAL
final:  JALR R31, R0, 0     
        JALR R0, R31, 0     
        
        JALR R0, R0, 0      