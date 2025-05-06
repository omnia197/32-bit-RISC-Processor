# Snake Game for RISC Processor
# Memory Map:
# 0x0000-0x3FFF: Program Code
# 0x4000-0x43FF: Display Buffer (32x32 grid, 1 word per pixel)
# 0x4400:       Direction Input (0=up, 1=right, 2=down, 3=left)
# 0x4404:       Game Status (0=running, 1=game over)
# 0x4408:       Random Seed
# 0x440C:       Score
# Registers Used:
# R28 = Display base (0x4000)
# R27 = Grid width (32)
# R30 = Stack pointer
# R29 = I/O base (0x4400)


SET R30, 0x4000     #sp 
SET R29, 0x4400     #I/O base address
SET R28, 0x4000     #buffer base
SET R27, 32        
SET R0, 0     

start:
	SET R1, 16          # x position
        SET R2, 16          # y position
        SET R3, 0           # dir(0=up)
        SET R4, 1           # seg value
        
        #calculate and store head position (16,16)
        MUL R5, R2, R27    
        ADD R5, R5, R1     
        ADD R5, R5, R28    
        SW R4, 0(R5)      
        
        #second segment (16,17)
        ADD R5, R5, R27    
        SW R4, 0(R5)
        
        #third segment (16,18)
        ADD R5, R5, R27 
        SW R4, 0(R5)

        #first food
        JALR R7, R0, generate_food

game_loop:
        #input direction
        LW R5, 0(R29)      
        
        #ensure direction change (can't reverse)
        #Up (0) can't follow Down(2)
        SET R6, 0           # Temporary comparison register
        SEQ R6, R5, R6      # Check if input is up (0)
        BNE R6, R0, check_up
        SET R6, 2
        SEQ R6, R5, R6      # Check if input is down (2)
        BNE R6, R0, check_down
        SET R6, 1
        SEQ R6, R5, R6      # Check if input is right (1)
        BNE R6, R0, check_right
        SET R6, 3
        SEQ R6, R5, R6      # Check if input is left (3)
        BNE R6, R0, check_left
        JALR R7, R0, skip_input
        
check_up:
        SET R6, 2
        BNE R3, R6, set_dir  # Current dir not down? OK to change
        JALR R7, R0, skip_input
check_down:
        SET R6, 0
        BNE R3, R6, set_dir  # Current dir not up? OK to change
        JALR R7, R0 skip_input
check_right:
        SET R6, 3
        BNE R3, R6, set_dir  # Current dir not left? OK to change
        JALR R7, R0, skip_input
check_left:
        SET R6, 1
        BNE R3, R6, set_dir  # Current dir not right? OK to change
        JALR R7, R0, skip_input
        
set_dir:
        ADD R3, R5, R0      # Update direction
        
skip_input:
        # Move snake based on direction
        SET R6, 0
        BEQ R3, R6, move_up
        SET R6, 1
        BEQ R3, R6, move_right
        SET R6, 2
        BEQ R3, R6, move_down
        JALR R7, R0, move_left

move_up:
        ADDI R2, R2, -1     # Y = Y-1
        JALR R7, R0, after_move
move_right:
        ADDI R1, R1, 1      # X = X+1
        JALR R7, R0, after_move
move_down:
        ADDI R2, R2, 1      # Y = Y+1
        JALR R7, R0, after_move
move_left:
        ADDI R1, R1, -1     # X = X-1
        JALR R7, R0, after_move

after_move:
        # Check wall collision
        SLTU R6, R1, R27    # X < 32?
        BEQ R6, R0, game_over
        SLTU R6, R2, R27    # Y < 32?
        BEQ R6, R0, game_over
        
        # Check self collision or food
        MUL R7, R2, R27     # y * 32
        ADD R7, R7, R1      # + x
        ADD R7, R7, R28     # + display base
        LW R8, 0(R7)        # Read display at new head position
        
        BEQ R8, R0, no_collision # 0=empty
        SET R9, 2
        BEQ R8, R9, eat_food # 2=food
        JALR R7, R0, game_over          # Otherwise collision with self

eat_food:
        # Increase score
        LW R10, 12(R29)    # Current score
        ADDI R10, R10, 1    # Increment score
        SW R10, 12(R29)    # Store new score
        
        # Generate new food
        JALR R7, R0, generate_food
        JALR R7, R0, update_snake      # Skip tail removal when growing

no_collision:
        # Remove tail segment logic would go here
        # (Would need to track full snake body positions)
        
update_snake:
        # Update snake head position
        SW R4, 0(R7)        # Store new head position
        
        # Delay for game speed
        SET R11, 100    # Delay counter
delay_loop:
        ADDI R11, R11, -1
        BNE R11, R0, delay_loop
        
        # Repeat game loop
        JALR R7, R0, game_loop

game_over:
        SET R12, 1
        SW R12, 4(R29)    # Set game over status
        JALR R7, R0, start             # Restart game

# Subroutine: Generate food at random position
# Subroutine: Generate food at random position
generate_food:
        # Prologue
        SW R31, -4(R30)     # Save return address
        ADDI R30, R30, -4   # Adjust stack
        
        # Load constants for random number generator
        SET R20, 16645      # High part of 1664525 (0x19660D)
        SET R21, 25         # Low part of 1664525 (0x19660D)
        SET R22, 1013 # Increment constant
        SET R23, 31         # MOD mask (0x1F)

        # Load and update random seed
        LW R13, 8(R29)      # Load random seed from 0x4408
        
        # Multiply seed by 1664525 (split into two operations)
        # First multiply by high part
        MUL R24, R13, R20   # R24 = R13 * 16645
        # Then multiply by low part and add
        MUL R25, R13, R21   # R25 = R13 * 25
        ADD R13, R24, R25   # Combine results
        
        # Add increment
        ADD R13, R13, R22   # R13 += 1013904223
        SW R13, 8(R29)      # Store new seed back to memory
        
        # Get X position (0-31) - MOD 32
        AND R14, R13, R23   # R14 = R13 & 31

        # Get Y position (0-31)
        SRLI R15, R13, 8    # Shift right by 8 bits
        AND R15, R15, R23   # R15 = (R13 >> 8) & 31

        # Calculate display address
        MUL R16, R15, R27   # y * 32
        ADD R16, R16, R14   # + x
        ADD R16, R16, R28   # + display base

        # Check if position is empty
        LW R17, 0(R16)
        BNE R17, R0, generate_food # Try again if not empty

        # Place food (value=2)
        SET R18, 2
        SW R18, 0(R16)

        # Epilogue
        LW R31, 0(R30)      # Restore return address
        ADDI R30, R30, 4    # Restore stack
        JALR R0, R31, 0       # Return