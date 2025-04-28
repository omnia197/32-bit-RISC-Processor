class ImmediateParser:
    @staticmethod
    def parse(imm_str, signed = True) -> int:
            value = int(imm_str, 0)  
            max_signed = 32767

            if value<0:
                return (max_signed+value)+1+pow(2, 15)
            else:
                 return value


# print(ImmediateParser.parse("1"))   
# print(ImmediateParser.parse("-2")) 
# print(ImmediateParser.parse("-3")) 
