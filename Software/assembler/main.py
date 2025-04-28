import sys
from core.assembler import MIPSAssembler

def main():
    if len(sys.argv) != 3:
        print("Usage: python assembler/assembleMain.py <input.asm> <output.bin>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    assembler = MIPSAssembler()
    
    try:
        print(f"Assembling {input_file}...")
        assembler.assemble(input_file, output_file)
        print(f"Done")
    except Exception as e:
        print(f"Assembly failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
