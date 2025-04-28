import re
from models.line_assembly import AssemblyLine
from models.label import Label
from parsers.instruction_parser import InstructionParser

class LineParser:
    def __init__(self):
         pass
    @staticmethod
    def parse(line: str, line_number: int) -> AssemblyLine:
        clean_line = re.sub(r'#.*$', '', line).strip()
        if not clean_line:
            return AssemblyLine(content=line, line_number=line_number)
        
        if ':' in clean_line:
            label_part, rest = clean_line.split(':', 1)
            label = Label(name=label_part.strip(), address=-1)
            if not rest.strip():
                return AssemblyLine(content=line,line_number=line_number,label=label)
            
            instruction = InstructionParser.parse(rest.strip())
            return AssemblyLine(content=line,line_number=line_number,label=label,instruction=instruction)
        
        instruction = InstructionParser.parse(clean_line)
        return AssemblyLine(content=line,line_number=line_number,instruction=instruction)