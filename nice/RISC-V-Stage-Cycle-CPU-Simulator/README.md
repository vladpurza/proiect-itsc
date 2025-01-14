# CA_project

## RISC-V Assembler and Simulator

This project involves the creation of an assembler and simulator for a RISC-V architecture, consisting of **6 classes of instructions**. The interconnectivity of these classes forms a simulator, allowing the execution of a variety of operations. The supported instructions include:

- **AND:** Performs a bitwise AND operation on two registers and stores the result in the destination register (rd).
- **OR:** Performs a bitwise OR operation on two registers and stores the result in the destination register (rd).
- **ADD:** Adds the values of two registers and stores the result in the destination register (rd).
- **SUB:** Subtracts the value in register rs2 from the value in register rs1 and stores the result in the destination register (rd).
- **ADDI:** Adds an immediate value to the content of register rs1 and stores the result in the destination register (rd).
- **BEQ:** Branches to a specified location if the values in registers rs1 and rs2 are equal.
- **LW (Load Word):** Loads a value from memory and stores it in the destination register (rd).
- **SW (Store Word):** Stores the value of register rs2 into memory.
- **SLL (Logical Left Shift):** Performs a logical left shift operation on the value in register rs1 by 5 lower bits of rs2.
- **SRA (Arithmetic Right Shift):** Performs an arithmetic right shift operation on the value in register rs1 by 5 lower bits of rs2.

### Usage

To use the simulator, simply run the **`CPU` class** in any Python compiler.

### Simulator Pipeline

The simulator follows a basic **five-stage pipeline** commonly found in modern processors:

1. **Fetch (F):**
   - The simulator fetches the instruction from the instruction memory.

2. **Decode (D):**
   - Extracts the opcode from the instruction and determines the instruction type.
   - Proceeds to the corresponding execution stage based on the instruction type.

3. **Execute (X):**
   - Handles the execution of instructions based on their types.
   - Calculates results for R-type and I-type instructions.
   - Determines memory addresses for S-type instructions.
   - Handles branches for SB-type instructions.

4. **Memory (M):**
   - Handles memory-related operations.
   - Writes data to memory for S-type instructions.
   - Writes data to the memory-mapped register (MMR) for NOC-type instructions.

5. **Writeback (W):**
   - Updates the register file or memory-mapped register based on the result of the execution.
   - Sets the corresponding register as not in use.

### Pipeline Management

- The simulator includes **latches (IF/ID, ID/EX, EX/MEM, MEM/WB)** to store intermediate results between stages, helping handle data dependencies and control hazards.
- Pipeline is managed through **conditional statements**, checking for data hazards and handling stalls appropriately.
- Stalls are tracked in the **`graph_data` dictionary**, used later to generate graphs showing stalls versus cycles.

### Graph Plotter

The simulator includes a graph plotter with functions to generate graphs for:

- **Instruction Types:**
  - Bar graph showing the frequency of different instruction types executed.
  - X-axis: Instruction types, Y-axis: Frequency.

- **Stalls versus Cycles:**
  - Line graph indicating the occurrence of stalls during different cycles.
  - X-axis: Cycles, Y-axis: Number of stalls.

- **Memory Accesses:**
  - Bar graph displaying the frequency of memory reads and writes.
  - X-axis: Memory access types, Y-axis: Frequency.

These graphs provide a visual overview of the simulator's performance, aiding in the analysis and optimization of its behavior.


