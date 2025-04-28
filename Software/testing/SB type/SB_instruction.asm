       
        SW R6, 2(R0)  
loop:   
        BLT R1, R2, loop    
       
        BGE R1, R2, break    
        
break:   BNE R1, R0, target   
        
target: BLTU R0, R2, next   
        
        
next:   BGEU R2, R0, final 
       
final: 
