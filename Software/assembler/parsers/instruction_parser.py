import re
from models.instruction import Instruction
from parsers.imm_parser import ImmediateParser
from parsers.register_parser import RegisterParser
import re 
class InstructionParser:
    @staticmethod
    def parse(instruction_str: str) -> Instruction:
        parts = re.split(r'[,\s]+', instruction_str)
        op = parts[0].upper()
        operands = []

        for op_part in parts[1:]:
            op_part = op_part.strip()
            if not op_part:
                continue

            mem_match = re.match(r'^(-?\d+)\((\w+)\)$', op_part)
            if mem_match:
                offset = mem_match.group(1)
                register = mem_match.group(2)
                operands.append(offset)
                operands.append(register)
            else:
                operands.append(op_part)
                
        return Instruction(opcode=op, operands=operands)
    
    # @staticmethod
    # def parse_memory_operand(operand):
    #         operand = operand.strip()
    #         if '(' not in operand:
    #             offset = ImmediateParser.parse(operand)
    #             return offset, 0 
    #         offset_str, rs1_str = operand.split('(', 1)
    #         rs1_str = rs1_str.rstrip(')')
    #         offset = ImmediateParser.parse(offset_str.strip())
    #         rs1 = RegisterParser.parse(rs1_str.strip())
    #         return offset, rs1