from encoders.encoder import InstructionEncoder
from parsers.register_parser import RegisterParser
from parsers.imm_parser import ImmediateParser
from parsers.instruction_parser import InstructionParser

class ITypeEncoder(InstructionEncoder):
    OPCODES = {
        'SLLI': 1, 'SRLI': 2, 'SRAI': 3, 'RORI': 4,
        'ADDI': 5, 'SLTI': 6, 'SLTIU': 7, 'SEQI': 8,
        'XORI': 9, 'ORI': 10, 'ANDI': 11, 'NORI': 12,
        'SET': 13, 'SSET': 14, 'JALR': 15, 'LW': 16}
    
    def encode(self, instruction, symbol_table, current_pc):
        opcode = self.OPCODES[instruction.opcode]

        needs_signed = instruction.opcode in ['ADDI', 'SLTI', 'SEQI', 'JALR', 'LW', 'SET', 'SSET']
        
        if instruction.opcode in ['SET', 'SSET']:
            rd = RegisterParser.parse(instruction.operands[0])
            imm = ImmediateParser.parse(instruction.operands[1], signed=True)
            return (imm << 16) | (0 << 11) | (rd << 6) | opcode
        
        if instruction.opcode == 'LW':
            rd = RegisterParser.parse(instruction.operands[0])
            offset = ImmediateParser.parse(instruction.operands[1])
            rs1 = RegisterParser.parse(instruction.operands[2])
            return (offset << 16) | (rs1 << 11) | (rd << 6) | opcode

 
        if instruction.opcode == 'JALR':
            rd = RegisterParser.parse(instruction.operands[0])
            rs1 = RegisterParser.parse(instruction.operands[1])
            imm_operand = instruction.operands[2]
            
            try:
                imm = ImmediateParser.parse(imm_operand, signed=True)
            except ValueError:
                if imm_operand not in symbol_table:
                    raise ValueError(f"undefined")
                target_addr = symbol_table[imm_operand]
                imm = target_addr 
            imm = imm & 0xFFFF #ensure it is 16 bit
            return (imm << 16) | (rs1 << 11) | (rd << 6) | opcode
        
        rd = RegisterParser.parse(instruction.operands[0])
        rs1 = RegisterParser.parse(instruction.operands[1])
        
        if instruction.opcode in ['SLLI', 'SRLI', 'SRAI', 'RORI']:
            sa = ImmediateParser.parse(instruction.operands[2], signed=False)
            return (0 << 21) | (sa << 16) | (rs1 << 11) | (rd << 6) | opcode

        imm = ImmediateParser.parse(
            instruction.operands[2],
            signed=needs_signed
        )
        
        return (imm << 16) | (rs1 << 11) | (rd << 6) | opcode