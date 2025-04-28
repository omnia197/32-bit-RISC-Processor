from abc import ABC, abstractmethod
from typing import Dict
from models.instruction import Instruction

class InstructionEncoder(ABC):
    @abstractmethod
    def encode(self, instruction: Instruction, symbol_table: Dict[str, int], current_pc: int) -> int:
        pass