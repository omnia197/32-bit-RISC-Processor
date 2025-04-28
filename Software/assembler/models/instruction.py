from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Instruction:
    opcode: str
    operands: List[str]