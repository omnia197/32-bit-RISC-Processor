# Single-Cycle Processor

## Overview

This project presents the design and implementation of a 32-bit RISC (Reduced Instruction Set Computer) processor following a single-cycle architecture. In a single-cycle design, each instruction is executed in its entirety within one clock cycle—regardless of its complexity. This means that instruction fetch, decode, execution, memory access, and write-back all occur simultaneously within a single clock pulse. While this approach greatly simplifies control logic and provides a clear conceptual understanding of instruction flow, it comes at the cost of performance since the clock cycle must accommodate the longest instruction.

The processor was designed and tested using Logisim Evolution, an educational digital circuit design tool. The architecture supports a custom Instruction Set Architecture (ISA), divided into three main instruction formats: R-type, I-type, and SB-type. The core hardware modules include the register file, Arithmetic Logic Unit (ALU), instruction and data memory, various control units, and necessary wiring and multiplexing logic. This processor forms the foundational phase of a broader project, which later evolves into a more efficient pipelined version.

---

## Objectives

- Design a complete single-cycle processor with 32-bit instructions.
- Support R-type (register), I-type (immediate), and SB-type (store/branch) instructions.
- Ensure instruction correctness with test cases and dataflow validation.

---

## Types Design Details

###  R-Type Instructions
R-type instructions are central to the RISC architecture as they perform operations strictly between registers. These instructions do not involve memory access or immediate values. The processor fetches two operand registers, executes the operation in the ALU, and writes the result to a destination register.

Examples of supported R-type instructions include:
 ADD, SUB, SLT, SLTU, MUL, XOR, AND, NOR, OR, SEQ, etc.

###  I-Type Instructions
I-type instructions extend the capabilities of the processor by allowing it to operate with immediate (constant) values or access memory for loading data. These instructions use one source register and a 16-bit immediate value, which is sign-extended to 32 bits.

Supported I-type instructions include:
SET, SLLI, SRLI, SRAI, RORI, ADDI, SLTI, XORI, ANDI, ORI, NORI, LW, JALR.

###  SB-Type Instructions
SB-type instructions are used primarily for control flow and memory store operations. They enable conditional branching and data storage into memory, critical for implementing loops and conditional structures.

Implemented SB-type instructions include:
SW, BEQ, BNE, BLT, BGE, BLTU, BGEU.

---

## Components Implemented

- **Register File**: 32 registers (R0-R31), with R0 hardwired to 0.
- **ALU**: Handles all arithmetic, logic, shift, and comparison instructions.
- **Instruction Memory**: Fetches instructions using PC.
- **Data Memory**: Used for LW and SW instructions.
- **Control Units**: Main Control Unit, ALU Control Unit, Condition Control Unit.
- **Immediate Extenders**: Support signed and zero extensions.
- **NextPC Logic**: Determines next PC based on control logic and branching.

---

##  Tools Used

- **Logisim** for digital design simulation.
- **Custom Assembler** (Python-based) for converting assembly to binary.
- **GitHub** for version control and documentation.

---

## Authors

- Omnia Ayman Mohamed  
- Alaa Ayman Mohamed  
- Rahma Mostafa  

---

