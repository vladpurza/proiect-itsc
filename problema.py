import tkinter as tk
from tkinter import messagebox

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
}

# RISC-V Simulator Class
class RiscVSimulator:
    def __init__(self):
        self.registers = [0] * NUM_REGISTERS  # 8 registers, initialized to 0
        self.memory = [0] * MEMORY_SIZE  # 100 memory addresses, initialized to 0
        self.pc = 0  # Program counter
        self.running = False  # Flag to check if the simulator is running
        self.instructions = []  # List of instructions
    
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
        else:
            messagebox.showerror("Error", f"Unknown instruction: {opcode}")
    
    def _add(self, parts):
        """ADD instruction (rd, rs1, rs2 or imm)"""
        rd = int(parts[1][1])
        rs1 = int(parts[2][1])
        rs2 = int(parts[3][1])
        self.registers[rd] = self.registers[rs1] + self.registers[rs2]
    
    def _sub(self, parts):
        """SUB instruction (rd, rs1, rs2)"""
        rd = int(parts[1][1])
        rs1 = int(parts[2][1])
        rs2 = int(parts[3][1])
        self.registers[rd] = self.registers[rs1] - self.registers[rs2]
    
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
        rs1 = int(parts[1][1])
        rs2 = int(parts[2][1])
        target = int(parts[3])
        if self.registers[rs1] == self.registers[rs2]:
            self.pc = target - 1
    
    def _branch_greater(self, parts):
        """BGT instruction (rs1, rs2, target)"""
        rs1 = int(parts[1][1])
        rs2 = int(parts[2][1])
        target = int(parts[3])
        if self.registers[rs1] > self.registers[rs2]:
            self.pc = target - 1
    
    def _branch_less(self, parts):
        """BLT instruction (rs1, rs2, target)"""
        rs1 = int(parts[1][1])
        rs2 = int(parts[2][1])
        target = int(parts[3])
        if self.registers[rs1] < self.registers[rs2]:
            self.pc = target - 1
    
    def _move(self, parts):
        """MOV instruction (rd, rs1)"""
        rd = int(parts[1][1])
        rs1 = int(parts[2][1])
        self.registers[rd] = self.registers[rs1]
    
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
        self.simulator = RiscVSimulator()
        self.root = root
        self.root.title("RISC-V Simulator")
        
        # Create the interface components
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
        
        # Buttons for controls
        self.load_button = tk.Button(self.root, text="Load Program", command=self.load_program)
        self.load_button.pack()

        self.run_button = tk.Button(self.root, text="Run Program", command=self.run_program)
        self.run_button.pack()

        self.step_button = tk.Button(self.root, text="Step", command=self.step_program)
        self.step_button.pack()

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_program)
        self.reset_button.pack()
    
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
    
    def step_program(self):
        """Execute one step of the program."""
        if self.simulator.execute():
            self.update_registers()
            self.update_memory()
    
    def reset_program(self):
        """Reset the simulator."""
        self.simulator.reset()
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

# Main application
def main():
    root = tk.Tk()
    gui = RiscVSimulatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
