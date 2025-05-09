# Pipelined Processor

## Overview

The project builds upon the foundation of the single-cycle RISC processor by implementing a 5-stage pipelined architecture. The goal of pipelining is to improve the overall performance and instruction throughput of the processor by allowing multiple instructions to execute concurrently at different stages of completion. Each instruction is broken down into five well-defined sequential stages:

1. **IF** – Instruction Fetch  
2. **ID** – Instruction Decode/Register Read  
3. **EX** – Execute  
4. **MEM** – Memory Access  
5. **WB** – Write Back

This design introduces pipeline registers between each stage to carry both data and control signals forward.

---

## Objectives

- Implement a fully pipelined RISC processor with correct data flow.
- Handle pipeline hazards: data, structural, and control.
- Integrate a 2-bit branch predictor to reduce stalls due to branch instructions.

---

##  Pipeline Enhancements

###  Pipeline Registers
Each stage passes values and signals to the next using specialized registers:
- **IF/ID**: Holds fetched instruction and PC+4.
- **ID/EX**: Holds decoded instruction, register values, and control signals.
- **EX/MEM**: Stores ALU result and memory/control signals.
- **MEM/WB**: Delivers final result to be written back to the register file.

### Hazard Management
Pipelining introduces timing conflicts known as hazards. These are situations where one instruction may depend on the result or decision of another that has not yet completed. Three main types of hazards are addressed in this project:
**Data Hazards**
These occur when an instruction depends on the result of a previous instruction that has not yet reached the write-back stage. To manage data hazards, we implement:

*Forwarding (Data Bypassing)*: This mechanism reroutes results from later pipeline stages (e.g., EX/MEM or MEM/WB) directly back to the EX stage, bypassing the register file.

*Stalling (Pipeline Freezing)*: In cases where forwarding is not possible—such as with load-use dependencies—a stall is inserted by preventing the PC and IF/ID register from updating for one cycle, allowing the dependent instruction to wait

**Control Hazards**
These arise from branch and jump instructions where the next instruction's address depends on a condition that is not resolved until the EX stage. To address this:

*Branch Prediction* is employed to guess the likely outcome of a branch and continue fetching accordingly.

*Pipeline Flushing and Bubbles*: are used to clear wrongly fetched instructions if a prediction is incorrect. A bubble acts as a "no operation" (NOP) that fills the pipeline temporarily to avoid executing the wrong path.

---

## Branch Prediction

To minimize the performance cost of control hazards, a 2-bit branch prediction mechanism is integrated into the pipeline. This dynamic predictor uses a saturating counter to track the recent outcomes of branch instructions and make informed predictions

---



