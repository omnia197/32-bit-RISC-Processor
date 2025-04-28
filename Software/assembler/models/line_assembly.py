from dataclasses import dataclass
from typing import Optional
from models.instruction import Instruction
from models.label import Label

@dataclass
class AssemblyLine:
    content: str
    line_number: int
    instruction: Optional[Instruction] = None
    label: Optional[Label] = None





