from encoders.encoder import InstructionEncoder
from parsers.register_parser import RegisterParser
from parsers.instruction_parser import ImmediateParser

class SBTypeEncoder(InstructionEncoder):
    OPCODES = {
        'SW': 17, 'BEQ': 18, 'BNE': 19, 'BLT': 20,
        'BGE': 21, 'BLTU': 22, 'BGEU': 23}
    
    def encode(self, instruction, symbol_table, current_pc):
        opcode = self.OPCODES[instruction.opcode]
        
        if instruction.opcode == 'SW':
            rs2 = RegisterParser.parse(instruction.operands[0])
            offset = ImmediateParser.parse(instruction.operands[1])
            rs1 = RegisterParser.parse(instruction.operands[2])
            immU = (offset >> 5) & 0x7FF   
            immL = offset & 0x1F         

            return (immU << 21) | (rs2 << 16) | (rs1 << 11) | (immL << 6) | opcode
             

        
        
        rs1 = RegisterParser.parse(instruction.operands[0])
        rs2 = RegisterParser.parse(instruction.operands[1])
        label = instruction.operands[2]

        if label not in symbol_table:
            raise ValueError(f"undefined label: {label} at Address value {current_pc}")
        target_addr = symbol_table[label]
        offset = target_addr - (current_pc) 
        offset = offset & 0xFFFF  
        immU = (offset >> 5) & 0x7FF
        immL = offset & 0x1F
        return (immU << 21) | (rs2 << 16) | (rs1 << 11) | (immL << 6) | opcode