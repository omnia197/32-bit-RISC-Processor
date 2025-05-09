# 32-bit RISC Processor Design Project

## Important Links

-  **[Project Documentation](https://github.com/omnia197/32-bit-RISC-Processor/tree/master/Project_files)**  

-  **[Video Single Cycle CANVA](https://www.canva.com/design/DAGl7qpneN4/hM22F8vpWSDxCd_imp6EEQ/watch?utm_content=DAGl7qpneN4&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h994518c5a2)**  

- **[Video Pipeline CANVA](https://www.canva.com/design/DAGm3YxovQk/uA6eLk6PSclDhGr_uXWKtw/watch?utm_content=DAGm3YxovQk&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h29ccf036eb)**  

-  **[Youtube tuturial](https://youtube.com/playlist?list=PLTd3BxCcSmCJD9BI92Br9cAg-PBU4CLYs&si=vmfUzdXWoByNKYGH)**  

---

## Overview

This project explores the complete design of a **32-bit RISC processor**, starting from a basic single-cycle implementation and evolving into a fully pipelined architecture. It aims not only to build a working processor in hardware, but also to make it **efficient, and developer-friendly** by adding an assembler and enhancing performance through **branch prediction techniques**.

The goal is to simulate real-world processor design, offering hands-on understanding of datapath creation, control logic, pipeline optimization, and performance enhancement. This project is ideal for students interested in computer architecture.

---

##  Goals

-  **Design a Single-Cycle 32-bit RISC Processor**:  
  Implement all instruction execution stages (Fetch → Decode → Execute → Memory → Write-Back) within a single clock cycle. This helps lay the foundation for understanding processor behavior and instruction execution flow.

-  **Implement a 5-Stage Pipelined Processor**:  
  To improve performance, the single-cycle processor is extended to use pipelining. This allows multiple instructions to be in different execution stages at the same time, increasing throughput.

-  **Build a Custom Assembler**:  
  Instead of manually converting assembly code to hexadecimal, a software assembler is developed to automate this process, improving developer productivity and reducing errors.

-  **Integrate a 2-Bit Branch Predictor**:  
  Control hazards (especially due to branching) are reduced using a dynamic predictor based on a 2-bit saturating counter. This helps the pipelined processor make educated guesses about branch outcomes.

---

##  Architecture Details

###  Single-Cycle Processor

The single-cycle RISC processor is the simplest implementation of the architecture, where each instruction completes all of its stages—fetch, decode, execute, memory access, and write-back—within one clock cycle. This design ensures that the control unit and datapath remain minimalistic and easy to trace, making it highly suitable for educational purposes or for early-stage functional testing. The processor executes each instruction sequentially, with no instruction overlap, thus avoiding any form of hazards. However, its main limitation lies in the requirement that the clock cycle duration must accommodate the slowest instruction in the instruction set. For instance, memory operations or complex branches may take longer, forcing the entire processor to slow down to match that timing even for faster instructions like register additions.

Despite the speed limitation, this design successfully supports essential RISC operations such as arithmetic and logic instructions (like ADD, SUB, AND, OR), memory operations (LOAD, STORE), and simple control flow instructions like BEQ (branch if equal) and BNE (branch if not equal). The core components include an Arithmetic Logic Unit (ALU), a Register File, instruction decoding logic, and a simple control unit. This processor forms the backbone for later enhancements and allows a clear understanding of instruction flow and signal dependencies without the added complexity of pipelining or hazard management.


###  Pipelined Processor

To overcome the inefficiencies of the single-cycle model, the architecture is extended into a 5-stage pipelined processor, inspired by classic RISC pipelines. In this design, instruction execution is divided into five discrete stages: Instruction Fetch (IF), Instruction Decode (ID), Execute (EX), Memory Access (MEM), and Write-Back (WB). Each stage processes a part of a different instruction in parallel, so while one instruction is being decoded, another can be fetched, and yet another can be executed. This overlapping of instruction execution drastically increases instruction throughput, allowing the CPU to handle one instruction per clock cycle in steady state.

However, pipelining introduces several new challenges. Data hazards occur when instructions depend on the results of previous instructions still in the pipeline. To resolve these, forwarding units (also known as bypassing) are implemented to pass results from later stages back to earlier ones, along with a hazard detection unit that stalls the pipeline when necessary. Control hazards, which arise from branch and jump instructions, are addressed through the implementation of a 2-bit branch predictor, which guesses the direction of branch execution based on historical patterns, reducing unnecessary stalls. Additionally, pipeline registers such as IF/ID, ID/EX, EX/MEM, and MEM/WB are introduced to hold the data and control signals between pipeline stages, ensuring data consistency and timing accuracy.

While this version adds complexity to both the datapath and the control logic, it significantly improves processor performance and mirrors how real-world processors achieve high efficiency. It builds on the solid foundation of the single-cycle processor while incorporating robust mechanisms for hazard resolution, making it a high-performance, instruction-level parallel processor.


---

##  Enhancements

###  Custom Assembler

The assembler converts human-readable assembly into hexa instructions for simulation or loading into instruction memory. It:
- Parses different instruction formats (R-type, I-type, J-type)
- Resolves **labels and jumps**
- Supports **immediate values**, pseudoinstructions, and macros
- Outputs a memory-compatible hexa file

This tool removes the need for manual translation, speeding up testing and reducing syntax errors.

###  2-Bit Branch Predictor

Branch instructions cause control hazards because the outcome (taken or not taken) isn't known until the EX stage. A naive solution would be to stall or flush, but this hurts performance.

The integrated branch predictor uses a **2-bit saturating counter** for each branch:
- 00: Strongly not taken
- 01: Weakly not taken
- 10: Weakly taken
- 11: Strongly taken

The predictor updates its state based on actual branch outcomes, becoming more accurate over time. This significantly reduces pipeline flushes and keeps instruction flow smooth.

---

## Project Structure

```bash
RISC_Processor_Project/
├── Pipeline/                     # all components for the pipelined version
│   ├── Images/                   # images related to pipelined datapath 
│   ├── Testing/                  # testing the pipelin processor
│   ├── Data_Path_Pipelined.circ
│   ├── Data_Path_testBTB.circ
│
├── Project_files/          
│   ├── Project_Spring_2025_Final.pdf         #project requirements
│   ├── RISC_Documentation_singleCycle.pdf    # documentation of the single-cycle design
|   ├── RISC_Documentation_Pipeline.pdf    # documentation of the pipeline design
|   ├── Full_RISC_Documentation.pdf    # fullyDoc
│   └── testCodeImplementation.pdf            # testcode output
│
├── SingleCycle/                
│   ├── ALU/                     # design for the alu
│   ├── DataPaths/               # data paths designs
│   ├── Path/                    # general data path
│   ├── ProjectImages/       
│   ├── RegisterFile/            #refister file design
│   └── Subcircuits/             #subcircuits like shifter arithmetic .. design
│
├── Software/                 
│   ├── assembler/               # assembler code
│   └── testing/                 # test codes for the assembler
