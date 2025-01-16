import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

# Define constants for the number of registers and memory
NUM_REGISTERS = 8
MEMORY_ROWS = 10
MEMORY_COLS = 10
MEMORY_SIZE = MEMORY_ROWS * MEMORY_COLS

# Define opcode table
OPCODE_TABLE = {
    "ADD": 1,
    "SUB": 2,
    "MUL": 3,
    "DIV": 4,
    "LW": 5,
    "SW": 6,
    "BEQ": 7,
    "BGT": 8,
    "BLT": 9,
    "MOV": 10,
    "SHL": 11,
    "SHR": 12,
    "OUT": 13,
    "HLT": 14,
    "CMP": 15,
    "JMS": 16,
    "RET": 17
}

# RISC-V Simulator Class
class RiscVSimulator:
    def __init__(self, output_callback=None):
        self.registers = [0] * NUM_REGISTERS
        self.memory = [0] * MEMORY_SIZE
        self.pc = 0
        self.running = False
        self.instructions = []
        self.output_callback = output_callback  # Callback for output
        self.stack = []  # Stack to store return addresses
        self.equal_flag = False  # Comparison flag
        self.gt_flag = False  # Greater than flag
        self.lt_flag = False  # Less than flag
        self.eq_flag = False  # Equal flag

    def load_program(self, instructions):
        """Load a program (list of instructions) into memory."""
        self.instructions = instructions
        self.pc = 0  # Reset the program counter
        
        # Load instructions into memory
        for i, instruction in enumerate(instructions):
            parts = instruction.split()
            opcode = OPCODE_TABLE.get(parts[0])
            if opcode is None:
                messagebox.showerror("Error", f"Unknown instruction: {parts[0]}")
                return
            operands = parts[1:]  # Operands are everything after the opcode
            self.memory[i] = f"{opcode} " + " ".join(operands)
        print(f"Loaded program with {len(instructions)} instructions.")
    
    def execute(self):
        """Execute the current instruction."""
        if self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            self._execute_instruction(instruction)
            self.pc += 1
            print(f"Executed instruction: {instruction}")
            return True
        else:
            self.running = False  # Stop when instructions are exhausted
            print("Program finished.")
            return False


    def _execute_instruction(self, instruction):
        """Decode and execute a single RISC-V instruction."""
        parts = instruction.split()
        opcode = parts[0]
        if opcode == "ADD":
            self._add(parts)
        elif opcode == "SUB":
            self._sub(parts)
        elif opcode == "MUL":
            self._mul(parts)
        elif opcode == "DIV":
            self._div(parts)
        elif opcode == "LW":
            self._load(parts)
        elif opcode == "SW":
            self._store(parts)
        elif opcode == "BEQ":
            self._branch_equal(parts)
        elif opcode == "BGT":
            self._branch_greater(parts)
        elif opcode == "BLT":
            self._branch_less(parts)
        elif opcode == "MOV":
            self._move(parts)
        elif opcode == "SHL":
            self._shift_left(parts)
        elif opcode == "SHR":
            self._shift_right(parts)
        elif opcode == "OUT":
            self._out(parts)
        elif opcode == "HLT":
            self._halt()
        elif opcode == "CMP":
            self._cmp(parts)
        elif opcode == "JMS":
            self._jms(parts)
        elif opcode == "RET":
            self._ret()
        else:
            messagebox.showerror("Error", f"Unknown instruction: {opcode}")

    def _add(self, parts):
        """ADD instruction (rd, rs1, rs2 or imm)"""
        rd = int(parts[1][1])
        rs1 = int(parts[2][1])
        if parts[3].startswith("R"):
            rs2 = int(parts[3][1])
            self.registers[rd] = self.registers[rs1] + self.registers[rs2]
        else:
            imm = int(parts[3])
            self.registers[rd] = self.registers[rs1] + imm
    
    def _sub(self, parts):
        """SUB instruction (rd, rs1, rs2)"""
        rd = int(parts[1][1])
        rs1 = int(parts[2][1])
        if parts[3].startswith("R"):
            rs2 = int(parts[3][1])
            self.registers[rd] = self.registers[rs1] - self.registers[rs2]
        else:
            imm = int(parts[3])
            self.registers[rd] = self.registers[rs1] + imm
    
    def _mul(self, parts):
        """MUL instruction (rd, rs1, rs2)"""
        rd = int(parts[1][1])
        rs1 = int(parts[2][1])
        rs2 = int(parts[3][1])
        self.registers[rd] = self.registers[rs1] * self.registers[rs2]
    
    def _div(self, parts):
        """DIV instruction (rd, rs1, rs2)"""
        rd = int(parts[1][1])
        rs1 = int(parts[2][1])
        rs2 = int(parts[3][1])
        if self.registers[rs2] != 0:
            self.registers[rd] = self.registers[rs1] // self.registers[rs2]
        else:
            messagebox.showerror("Error", "Division by zero!")
    
    def _load(self, parts):
        """LW instruction (rd, address)"""
        rd = int(parts[1][1])
        address = int(parts[2])
        if 0 <= address < MEMORY_SIZE:
            self.registers[rd] = self.memory[address]
        else:
            messagebox.showerror("Error", "Memory access out of bounds!")
    
    def _store(self, parts):
        """SW instruction (rs, address)"""
        rs = int(parts[1][1])
        address = int(parts[2])
        if 0 <= address < MEMORY_SIZE:
            self.memory[address] = self.registers[rs]
        else:
            messagebox.showerror("Error", "Memory access out of bounds!")
    
    def _branch_equal(self, parts):
        """BEQ instruction (rs1, rs2, target)"""
        if self.eq_flag:  # Use the comparison flag
            self.pc = int(parts[1]) - 2  # Set PC to the target address
            print(f"Branching to {parts[1]}")

    def _branch_greater(self, parts):
        """BGT instruction (rs1, rs2, target)"""
        if self.gt_flag:  # Use the comparison flag
            self.pc = int(parts[1]) - 2
            print(f"Branching to {parts[1]}")

    def _branch_less(self, parts):
        """BLT instruction (rs1, rs2, target)"""
        if self.lt_flag:  # Use the comparison flag
            self.pc = int(parts[1]) - 2
            print(f"Branching to {parts[1]}")

    def _move(self, parts):
        """MOV instruction (rd, rs1)"""
        rd = int(parts[1][1])
        rs1 = int(parts[2][1])
        self.registers[rd] = self.registers[rs1]


    def _shift_left(self, parts):
        """SHL instruction (rd, rs1): Shift left rs1 by 1 and store in rd."""
        rd = int(parts[1][1])
        rs1 = int(parts[2][1])
        self.registers[rd] = self.registers[rs1] << 1

    def _shift_right(self, parts):
        """SHR instruction (rd, rs1): Shift right rs1 by 1 and store in rd."""
        rd = int(parts[1][1])
        rs1 = int(parts[2][1])
        self.registers[rd] = self.registers[rs1] >> 1
    
    def _out(self, parts):
        """OUT instruction (prints the value of the specified register)."""
        if len(parts) != 2:
            raise ValueError(f"Invalid OUT instruction: {parts}")
        
        reg = int(parts[1][1])  # Extract the register number
        if 0 <= reg < NUM_REGISTERS:
            value = self.registers[reg]
            if self.output_callback:
                self.output_callback(f"{value}\n")
        else:
            messagebox.showerror("Error", f"Register R{reg} out of bounds!")

    def _cmp(self, parts):
        """CMP instruction (rs1, rs2): Compare rs1 and rs2."""
        rs1 = int(parts[1][1])  # Extract register number from string (e.g., R1 -> 1)
        rs2 = int(parts[2][1])

        if self.registers[rs1] > self.registers[rs2]:
            self.gt_flag = True  # Register 1 is greater than Register 2
            self.lt_flag = False
            self.eq_flag = False
        elif self.registers[rs1] < self.registers[rs2]:
            self.gt_flag = False
            self.lt_flag = True  # Register 1 is less than Register 2
            self.eq_flag = False
        else:
            self.gt_flag = False
            self.lt_flag = False
            self.eq_flag = True  # Registers are equal

        print(f"CMP result: {'Greater' if self.gt_flag else ('Less' if self.lt_flag else 'Equal')}")

    def _jms(self, parts):
        """JMS instruction (jump to subroutine)."""
        target = int(parts[1])  # Target address for the jump
        self.stack.append(self.pc + 1)  # Save the return address (next instruction after JMS)
        self.pc = target - 2 # Jump to the subroutine (adjust PC for 0-indexed addressing)
        print(f"Jumping to subroutine at address {target}")

    def _ret(self):
        """RET instruction (return from subroutine)."""
        if self.stack:
            self.pc = self.stack.pop() - 1 # Pop the return address and set PC to it
            print(f"Returning to address {self.pc}")  # Show the next instruction after the JMS
        else:
            messagebox.showerror("Error", "Return address stack is empty!")

    def _halt(self):
        """HLT instruction: Stop program execution but allow stepping to restart."""
        self.running = False
        self.pc = len(self.instructions) - 1
        messagebox.showinfo("Halt", "Program execution halted. You can step to resume.")

    def reset(self):
        """Reset the simulator to its initial state."""
        self.registers = [0] * NUM_REGISTERS
        self.memory = [0] * MEMORY_SIZE
        self.pc = 0
        self.running = False
        print("Simulator reset.")

# GUI Class for the Simulator
class RiscVSimulatorGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("RISC-V Simulator")
        self.simulator = RiscVSimulator(output_callback=self.write_output)  # Pass callback
        self.create_widgets()

    def create_widgets(self):
        # Register display (Horizontal layout)
        self.register_frame = tk.Frame(self.root)
        self.register_frame.pack()
        self.register_labels = []
        for i in range(NUM_REGISTERS):
            label = tk.Label(self.register_frame, text=f"R{i}: 0", width=10)
            label.grid(row=0, column=i)
            self.register_labels.append(label)
        
        # Program input
        self.program_label = tk.Label(self.root, text="Enter instructions (one per line):")
        self.program_label.pack()
        self.program_text = tk.Text(self.root, height=20, width=50)
        self.program_text.pack()
        
        # Memory display (10x10 matrix)
        self.memory_frame = tk.Frame(self.root)
        self.memory_frame.pack()
        self.memory_labels = []
        for i in range(MEMORY_ROWS):
            row_labels = []
            for j in range(MEMORY_COLS):
                label = tk.Label(self.memory_frame, text="", width=10, borderwidth=1, relief="solid")
                label.grid(row=i, column=j)
                row_labels.append(label)
            self.memory_labels.append(row_labels)

        # Flags display (Grid for flags)
        self.flags_frame = tk.Frame(self.root)
        self.flags_frame.pack()
        self.flags_labels = {
            "Equal": tk.Label(self.flags_frame, text="Equal: False", width=15),
            "Greater": tk.Label(self.flags_frame, text="Greater: False", width=15),
            "Less": tk.Label(self.flags_frame, text="Less: False", width=15)
        }
        self.flags_labels["Equal"].grid(row=0, column=0)
        self.flags_labels["Greater"].grid(row=0, column=1)
        self.flags_labels["Less"].grid(row=0, column=2)

        # Buttons for controls
        self.load_button = tk.Button(self.root, text="Load Program", command=self.load_program)
        self.load_button.pack()

        self.run_button = tk.Button(self.root, text="Run Program", command=self.run_program)
        self.run_button.pack()

        self.step_button = tk.Button(self.root, text="Step", command=self.step_program)
        self.step_button.pack()

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_program)
        self.reset_button.pack()

        self.output_label = tk.Label(self.root, text="Output:")
        self.output_label.pack()
        self.output_text = tk.Text(self.root, height=5, width=10, state="disabled", bg="lightgray")
        self.output_text.pack()

    def load_program(self):
        """Load the program into the simulator."""
        program = self.program_text.get("1.0", tk.END).strip().splitlines()
        self.simulator.load_program(program)
        self.update_memory()
    
    def run_program(self):
        """Run the program until completion."""
        while self.simulator.execute():
            self.update_registers()
            self.update_memory()
            if not self.simulator.running:
                break

    def step_program(self):
        """Execute one step of the program."""
        if not self.simulator.running and self.simulator.pc == len(self.simulator.instructions):
            messagebox.showinfo("Info", "Program halted. Reset to run again.")
            return

        instruction = self.simulator.instructions[self.simulator.pc]
        if self.simulator.execute():
            self.update_registers()
            self.update_memory()
            self.update_flags()

    def reset_program(self):
        """Reset the simulator."""
        self.simulator.reset()
        self.update_registers()
        self.update_memory()
        self.clear_flags()
        self.clear_output()
    
    def submit_input(self, instruction):
        parts = instruction.split()
        self.simulator._inp(parts)
        self.update_registers()
        self.update_memory()

    def update_registers(self):
        """Update the displayed register values."""
        for i in range(NUM_REGISTERS):
            self.register_labels[i].config(text=f"R{i}: {self.simulator.registers[i]}")
    
    def update_memory(self):
        """Update the displayed memory values."""
        for i in range(MEMORY_ROWS):
            for j in range(MEMORY_COLS):
                addr = i * MEMORY_COLS + j
                if addr < len(self.simulator.memory):
                    self.memory_labels[i][j].config(text=self.simulator.memory[addr])
                else:
                    self.memory_labels[i][j].config(text="")

                if self.simulator.pc == addr:
                    self.memory_labels[i][j].config(bg="yellow")
                else:
                    self.memory_labels[i][j].config(bg="white")

    def update_flags(self):
        """Update the displayed flags."""
        self.flags_labels["Equal"].config(text=f"Equal: {self.simulator.eq_flag}")
        self.flags_labels["Greater"].config(text=f"Greater: {self.simulator.gt_flag}")
        self.flags_labels["Less"].config(text=f"Less: {self.simulator.lt_flag}")
    
    def clear_flags(self):
        """Clear the flags."""
        self.simulator.eq_flag = False
        self.simulator.gt_flag = False
        self.simulator.lt_flag = False
        self.update_flags()

    def write_output(self, text):
        """Write text to the output box."""
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.config(state="disabled")
        self.output_text.see(tk.END)

    def clear_output(self):
        """Clear the output text box."""
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)  # Clear the text area
        self.output_text.config(state="disabled")

# Main application
def main():
    root = tk.Tk()
    gui = RiscVSimulatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

'''
ADD R0 R1 1
SHL R1 R0 1
OUT R1
CMP R0 R1
BLT 2
JMS 8
HLT
ADD R0 R1 1
RET

'''
