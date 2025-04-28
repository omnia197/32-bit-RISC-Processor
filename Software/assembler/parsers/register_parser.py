class RegisterParser:
    REGISTERS = {f'R{i}': i for i in range(32)}
    REGISTERS['RZ'] = 0  
    
    @staticmethod
    def parse(reg_str: str) -> int:
        reg = reg_str.upper()
        if reg in RegisterParser.REGISTERS:
            return RegisterParser.REGISTERS[reg]
