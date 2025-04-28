from encoders.encoder import InstructionEncoder
from parsers.register_parser import RegisterParser

class RTypeEncoder(InstructionEncoder):
    FUNCTIONS = {
        'SLL': 0, 'SRL': 1, 'SRA': 2, 'ROR': 3,
        'ADD': 4, 'SUB': 5, 'SLT': 6, 'SLTU': 7,
        'SEQ': 8, 'XOR': 9, 'OR': 10, 'AND': 11,
        'NOR': 12, 'MUL': 13
    }
    
    def encode(self, instruction, symbol_table, current_pc):
        f = self.FUNCTIONS[instruction.opcode]
        d = RegisterParser.parse(instruction.operands[0])
        s1 = RegisterParser.parse(instruction.operands[1])
        s2 = RegisterParser.parse(instruction.operands[2])
        return (f << 21) | (s2 << 16) | (s1 << 11) | (d << 6) | 0