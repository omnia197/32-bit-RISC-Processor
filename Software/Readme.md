# 32-bit RISC Assembler

## Overview
An assembler is a crucial component in the software development toolchain, particularly for low-level programming and processor design. Its main role is to translate human-readable assembly language instructions into machine-readable binary code (also known as object code). Assembly language is a low-level programming language that is closely related to machine instructions for a specific architecture, but it uses instructions (like `ADD`, `SUB`, `BEQ`) instead of raw binary.

By developing my own assembler, I built a tool that automates this translation process, allowing programs written in assembly language to be executed by the processor with **100% accuracy** in encoding all 37 instructions we have.

---

## Structure

### Models

We begin developing the assembler by first identifying all the essential modules and the different 
types of inputs it may receive. This includes analyzing the full content of the input file, then breaking 
it down line by line to extract each instruction. For every line, we determine whether it contains a 
label, and if so, we collect the label and its associated variables.  
This structure helps ensure that the assembler correctly interprets and processes all parts of the input

**Directory: `models/`**
models/ ├── init.py ├── instruction.py ├── label.py └── line_assembly.py

---

### Parsers

After identifying the input structure, we introduce parsers that process the input and extract the 
necessary parameters. In the immediate (IMM) parser, we pass the immediate value while 
considering that we are working with 16-bit signed values. Therefore, the maximum value is 32767
and the minimum value is -32768. If the immediate value is negative, it may require sign extension, 
meaning we must add additional '1' bits to maintain its correct signed representation. 
In the line parser, the input line is cleaned by removing any unnecessary parameters, such as 
extra spaces or comments. It also checks if the line contains a label and processes it accordingly. 
In the register file, when dealing with register inputs, we ensure the register number is within the 
valid range of 0 to 31, following our model's 32-register structure. 
Finally, we have the instruction parser, which extracts the opcode from the instruction and 
determines its format. If the instruction is a simple form like ADD R2, R1, R1, it directly maps the 
registers. However, if the instruction is of a more complex form, such as lw R6, 0(R2), we need 
to further divide the instruction into an offset part and a register part for correct parsing and 
processing.

**Directory: `parsers/`**
parsers/ ├── init.py ├── imm_parser.py ├── instruction_parser.py ├── line_parser.py └── register_parser.py

---

### Encoders

Next, we move on to the encoders, which group all similar methods based on instruction types. 
The encoder starts by fetching the parameters, including the opcode and function code (func). For R
type instructions, it first checks if the instruction exists in the instruction set. Then, it retrieves the 
destination register and operand values. These values are processed by shifting and performing 
bitwise OR operations to assemble the final binary form of the instruction.  
It is totally connected with our ISA design format to be built on

**Directory: `encoders/`**

encoders/ ├── init.py ├── encoder.py ├── i_encoder.py └── sb_encoder.py

---

## GUI

To improve the user experience, we develop a visually appealing and interactive GUI that is both 
functional and easy to navigate. The interface will feature colorful buttons and a clean layout to make 
it intuitive for users to interact with the system. 

### Features

- **File Upload and Saving**: Upload `.asm` files and export output in `.asm` or `.hex` format.
- **Code Editor with Syntax Highlighting**: Highlights keywords, instructions, registers, and labels in different colors.
- **Memory Registers and Labels**: Visually separate memory regions and labels for easier navigation.
- **Output Generation**: Converts assembly into readable output (assembly file or hex).

---

## Testing & Verification

In testing the core, we ensured that all instructions were properly implemented and functioned 
correctly with the appropriate format. These instructions were used to test the general datapath and 
control unit of our RISC processor, ensuring their seamless integration and functionality 

---

---

## Installation

### Prerequisites

- **Python 3.6+**  
  Verify:  
  ```bash
  python --version
  ```  
  [Download Python](https://www.python.org/downloads/)

- **Git**  
  Verify:  
  ```bash
  git --version
  ```  
  [Download Git](https://git-scm.com/downloads)

- **Visual Studio Code (optional)** for convenient editing.

---

## Getting the Project

Clone the repository using:

```bash
git clone https://github.com/omnia197/32-bit-RISC-Processor.git
```

---

## Usage Options

### 1. Command-Line Interface (CLI)

Run from terminal:

```bash
python assembler/main.py input.asm output.asm
```

**Example:**
```bash
python assembler/main.py myprogram.asm myprogram_output.asm
```

---

### 2. Graphical User Interface (GUI)

Run the UI:

```bash
python assembler/UI.py
```

Use the GUI to load your assembly file and process it without using terminal commands.

---

## License

This project is open source and free to use for educational and research purposes.

---
## Authors

- Omnia Ayman Mohamed  
- Alaa Ayman Mohamed  
- Rahma Mostafa  
