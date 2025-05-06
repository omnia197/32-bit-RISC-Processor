from collections import defaultdict
from typing import Dict, List
from parsers import line_parser
from models.line_assembly import AssemblyLine
from encoders.r_encoder import RTypeEncoder
from encoders.i_encoder import ITypeEncoder
from encoders.sp_encoder import SBTypeEncoder
from encoders.encoder import InstructionEncoder

class MIPSAssembler:
    def __init__(self):
        self.encoder_map = self._create_encoder_map()
        self.symbol_table = {}
        self.forward_references = defaultdict(list)
        self.output = []
    
    def _create_encoder_map(self) -> Dict[str, InstructionEncoder]:
        return {
            'SLL': RTypeEncoder(), 'SRL': RTypeEncoder(), 'SRA': RTypeEncoder(),
            'ROR': RTypeEncoder(), 'ADD': RTypeEncoder(), 'SUB': RTypeEncoder(),
            'SLT': RTypeEncoder(), 'SLTU': RTypeEncoder(), 'SEQ': RTypeEncoder(),
            'XOR': RTypeEncoder(), 'OR': RTypeEncoder(), 'AND': RTypeEncoder(),
            'NOR': RTypeEncoder(), 'MUL': RTypeEncoder(),
            'SLLI': ITypeEncoder(), 'SRLI': ITypeEncoder(), 'SRAI': ITypeEncoder(),
            'RORI': ITypeEncoder(), 'ADDI': ITypeEncoder(), 'SLTI': ITypeEncoder(),
            'SLTIU': ITypeEncoder(), 'SEQI': ITypeEncoder(), 'XORI': ITypeEncoder(),
            'ORI': ITypeEncoder(), 'ANDI': ITypeEncoder(), 'NORI': ITypeEncoder(),
            'SET': ITypeEncoder(), 'SSET': ITypeEncoder(), 'JALR': ITypeEncoder(),
            'LW': ITypeEncoder(), 'SW': SBTypeEncoder(), 'BEQ': SBTypeEncoder(),
            'BNE': SBTypeEncoder(), 'BLT': SBTypeEncoder(), 'BGE': SBTypeEncoder(),
            'BLTU': SBTypeEncoder(), 'BGEU': SBTypeEncoder()
        }
    
    def first_pass(self, assembly_lines: List[AssemblyLine]) -> None:
        current_address = 0
        for line in assembly_lines:
            if line.label:
                self.symbol_table[line.label.name] = current_address
                line.label.address = current_address
            
            if line.instruction:
                line.instruction.address = current_address
                current_address += 1
    
    def second_pass(self, assembly_lines: List[AssemblyLine]) -> None:
        for line in assembly_lines:
            if not line.instruction:
                continue
            
            encoder = self.encoder_map.get(line.instruction.opcode)
        
            
            machine_code = encoder.encode(
                instruction=line.instruction,
                symbol_table=self.symbol_table,
                current_pc=line.instruction.address)
            self.output.append(machine_code)
    
    def assemble(self, input_file: str, output_file: str) -> None:
        with open(input_file, 'r') as f:
            lines = [line_parser.LineParser.parse(line, i+1) for i, line in enumerate(f.readlines())]
        
        assembly_lines = [line for line in lines if line.content.strip()]
        self.first_pass(assembly_lines)
        self.second_pass(assembly_lines)
        
        with open(output_file, 'wb') as f:
            for instruction in self.output:
                f.write(instruction.to_bytes(4, byteorder='little'))
        
        with open(output_file + '.hex', 'w') as f:
            for i, instruction in enumerate(self.output):
                f.write(f"{i:08x}: {instruction:08x}\n")

   