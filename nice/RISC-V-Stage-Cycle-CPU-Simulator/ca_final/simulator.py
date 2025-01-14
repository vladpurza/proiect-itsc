from memory import DataMemory
import matplotlib.pyplot as plt

class Simulator:
    def __init__(self):
        self.program_counter = 0

        self.mar = 0 # memory address register to store the temporary address of the program counter

        self.inst_memory = []

        self.branch_flag = False

        self.dm = DataMemory()

        self.dm.assign_random_values()

        self.latches = {
            "IF/ID": None,
            "ID/EX": None,
            "EX/MEM": None,
            "MEM/WB": None,
        }

        self.reg_in_use = {
            "R0": False,
            "R1": False,
            "R2": False,
            "R3": False,
            "R4": False,
            "R5": False,
            "R6": False,
            "R7": False,
            "R8": False,
            "R9": False,
            "R10": False,
            "R11": False,
            "R12": False,
            "R13": False,
            "R14": False,
            "R15": False,
            "R16": False,
            "R17": False,
            "R18": False,
            "R19": False,
            "R20": False,
            "R21": False,
            "R22": False,
            "R23": False,
            "R24": False,
            "R25": False,
            "R26": False,
            "R27": False,
            "R28": False,
            "R29": False,
            "R30": False,
            "R31": False,
        }

        self.reg_val = {
            "R0": 0,
            "R1": 0,
            "R2": 0,
            "R3": 0,
            "R4": 0,
            "R5": 0,
            "R6": 0,
            "R7": 0,
            "R8": 0,
            "R9": 0,
            "R10": 0,
            "R11": 0,
            "R12": 0,
            "R13": 0,
            "R14": 0,
            "R15": 0,
            "R16": 0,
            "R17": 0,
            "R18": 0,
            "R19": 0,
            "R20": 0,
            "R21": 0,
            "R22": 0,
            "R23": 0,
            "R24": 0,
            "R25": 0,
            "R26": 0,
            "R27": 0,
            "R28": 0,
            "R29": 0,
            "R30": 0,
            "R31": 1001,
        }
        self.register_dict = {
            "00000": "R0",
            "00001": "R1",
            "00010": "R2",
            "00011": "R3",
            "00100": "R4",
            "00101": "R5",
            "00110": "R6",
            "00111": "R7",
            "01000": "R8",
            "01001": "R9",
            "01010": "R10",
            "01011": "R11",
            "01100": "R12",
            "01101": "R13",
            "01110": "R14",
            "01111": "R15",
            "10000": "R16",
            "10001": "R17",
            "10010": "R18",
            "10011": "R19",
            "10100": "R20",
            "10101": "R21",
            "10110": "R22",
            "10111": "R23",
            "11000": "R24",
            "11001": "R25",
            "11010": "R26",
            "11011": "R27",
            "11100": "R28",
            "11101": "R29",
            "11110": "R30",
            "11111": "R31",
        }

        self.pipeline = {
            "W": False,
            "M": False,
            "X": False,
            "D": False,
            "F": False,
        }
        
        self.curr_fetch = None
        self.curr_decode = None
        self.curr_execute = None
        self.curr_memory = None
        self.curr_writeback = None
        
        self.cycle = 1

        self.writeback_stalled = False
        self.memory_stalled = False
        self.execute_stalled = False
        self.decode_stalled = False
        self.fetch_stalled = False

        self.executed_instructions = 0

        self.graph_data = {
            "instruction_types": {
                "R": 0,
                "I": 0,
                "S": 0,
                "SB": 0,
                "U": 0,
                "UJ": 0,
                "NOC": 0,
            },

            "stalls_vs_cycles": [],

            "memory_accesses": {
                "reads": 0,
                "writes": 0,
            },
        }

    def make_stalls_vs_cycles_graph(self):
        # line graph of stalls vs cycles, plot a point for each value in the list
        plt.plot(range(1, len(self.graph_data["stalls_vs_cycles"]) + 1), self.graph_data["stalls_vs_cycles"])
        plt.xlabel("Cycle")
        plt.ylabel("Stalls")
        plt.title("Stalls vs Cycles")
        plt.show()

    def make_memory_accesses_graph(self):
        self.graph_data["memory_accesses"]["reads"] = self.dm.read_count
        self.graph_data["memory_accesses"]["writes"] = self.dm.write_count
        # bar graph of reads and writes
        plt.bar(self.graph_data["memory_accesses"].keys(), self.graph_data["memory_accesses"].values())
        plt.xlabel("Memory Accesses")
        plt.ylabel("Frequency")
        plt.title("Memory Accesses")
        plt.show()

    def make_instruction_types_graph(self):
        plt.bar(self.graph_data["instruction_types"].keys(), self.graph_data["instruction_types"].values())
        plt.xlabel("Instruction Types")
        plt.ylabel("Frequency")
        plt.title("Instruction Types")
        plt.show()

    def make_graph(self):
        self.make_instruction_types_graph()
        self.make_stalls_vs_cycles_graph()
        self.make_memory_accesses_graph()

    def print_reg_val(self):
        # print register values in a table
        # print("PC: ", self.program_counter)
        print("Register Values:")
        for i in range(0, 32, 4):
            print(
                f"{self.register_dict[str(bin(i))[2:].zfill(5)]}: {self.reg_val[self.register_dict[str(bin(i))[2:].zfill(5)]]}\t\t\t{self.register_dict[str(bin(i + 1))[2:].zfill(5)]}: {self.reg_val[self.register_dict[str(bin(i + 1))[2:].zfill(5)]]}\t\t\t{self.register_dict[str(bin(i + 2))[2:].zfill(5)]}: {self.reg_val[self.register_dict[str(bin(i + 2))[2:].zfill(5)]]}\t\t\t{self.register_dict[str(bin(i + 3))[2:].zfill(5)]}: {self.reg_val[self.register_dict[str(bin(i + 3))[2:].zfill(5)]]}"
            )

    def print_pipeline(self):
        # print pipeline in a table
        print(self.cycle)
        for key in self.pipeline:
            if self.pipeline[key]:
                print(f"{key}")
        print()

    def load_instructions_into_memory(self, instructions):
        for instruction in instructions:
            self.inst_memory.append(instruction)

    def run_simulator(self, instructions):
        self.load_instructions_into_memory(instructions)
        total_instructions = len(self.inst_memory)
        while self.executed_instructions < total_instructions:
            # curr_instruction = instructions[self.program_counter]

            # writeback
            if self.curr_memory is not None:
                self.curr_writeback = self.writeback(self.curr_memory[0], self.curr_memory[1], self.curr_memory[2])
                self.pipeline["W"] = True
            else:
                self.curr_memory = None
                self.pipeline["W"] = False

            # memory
            if self.curr_execute is not None:
                self.curr_memory = []
                self.curr_memory.append(self.curr_execute[0][0])
                self.curr_memory.append(self.curr_execute[0][1])
                self.curr_memory.append(self.curr_execute[1])
                self.memory_stage(self.curr_execute[0][0], self.curr_execute[0][1], self.curr_execute[1])
                self.pipeline["M"] = True
            else:
                self.curr_memory = None
                self.pipeline["M"] = False

            # execute
            if self.curr_decode is not None:
                temp_exec = self.execute(self.curr_decode[0], self.curr_decode[1])

                if len(temp_exec[0]) == 3 and temp_exec[0][2] == False:
                    print("Execute stalled")
                    self.pipeline["X"] = False
                    self.curr_execute = None
                    self.execute_stalled = True
                    self.graph_data["stalls_vs_cycles"].append(1)
                else:
                    self.curr_execute = temp_exec
                    self.pipeline["X"] = True
                    self.graph_data["stalls_vs_cycles"].append(0)
                
            else:
                # print("Execute stalled")
                self.graph_data["stalls_vs_cycles"].append(0)
                self.curr_execute = None
                self.pipeline["X"] = False

            
            # decode
            if self.curr_fetch is not None:
                if self.execute_stalled == False:
                    self.curr_decode = self.decode(self.curr_fetch)
                    self.pipeline["D"] = True
                else:
                    print("Decode stalled")
                    self.pipeline["D"] = True
            elif self.branch_flag:
                self.pipeline["D"] = True

            else:
                if self.execute_stalled == False:
                    self.curr_decode = None
                    self.pipeline["D"] = False
                else:
                    print("Decode stalled")
                    self.pipeline["D"] = True


            # fetch
            # if not self.pipeline["F"]:
            #     self.curr_fetch = self.fetch(curr_instruction)
            #     self.pipeline["F"] = True
            # else:
            #     # print("Fetch stalled"))
            if self.program_counter < total_instructions:
                if self.branch_flag:
                    self.branch_flag = False
                elif not self.decode_stalled:
                    self.curr_fetch = self.fetch(self.inst_memory[self.program_counter])
                    self.mar = self.program_counter
                    self.program_counter += 1
                self.pipeline["F"] = True
                
            else:
                self.curr_fetch = None
                self.pipeline["F"] = False

            if self.pipeline["W"]:
                self.executed_instructions += 1

            self.print_pipeline()
            if self.execute_stalled:
                self.execute_stalled = False
            if self.decode_stalled:
                self.decode_stalled = False
            self.cycle += 1
    
    def fetch(self, instruction):
        instruction = instruction.replace(" ", "")
        return instruction
    
    def decode(self, instruction):
        opcode = instruction[25:32]
        return [opcode, instruction]
    
    def execute(self, opcode, instruction):
        instruction = instruction.replace(" ", "")
        if opcode == "0110011":
            # R type: add, sub, sll, slt, sltu, xor, srl, sra, or, and
            return [self.r_type(instruction), "R"]
        elif opcode == "0010011" or opcode == "0000011" or opcode == "1100111" or opcode == "1110011":
            # I type: addi, slti, sltiu, xori, ori, andi, slli, srli, srai
            return [self.i_type(instruction), "I"]
        elif opcode == "0100011":
            # S type: sb, sh, sw, sd
            return [self.s_type(instruction), "S"]
        elif opcode == "1100011":
            # SB type: beq, bne, blt, bge, bltu, bgeu
            return [self.sb_type(instruction), "SB"]
        elif opcode == "0110111" or opcode == "0010111":
            # U type: lui, auipc
            return [self.u_type(instruction), "U"]
        elif opcode == "1101111":
            # UJ type: jal
            return [self.uj_type(instruction), "UJ"]
        elif opcode == "1111111":
            # halt
            return [self.custom_type(instruction), "NOC"]
        else:
            print("Invalid instruction")

    def writeback(self, register, x, instr_type: str):
        if instr_type == "R" or instr_type == "I":
            self.reg_val[register] = x
        
        elif instr_type == "U" or instr_type == "UJ":
            self.reg_val[register] = x

        elif instr_type == "NOC" and register != 1004:
            self.dm.write_mmr(register, x)
            self.dm.print_mmr_values()
        
        self.reg_in_use[register] = False
        self.print_reg_val()

    def memory_stage(self, register, x, instr_type: str):
        if instr_type == "S":
            self.dm.write(x, self.reg_val[register])   
        elif instr_type == "NOC" and register == 1004:
            self.dm.write_mmr("1004", x) 
            self.dm.print_mmr_values()        

    def r_type(self, instruction):
        funct7 = instruction[0:7]
        rs2 = self.register_dict[instruction[7:12]]
        rs1 = self.register_dict[instruction[12:17]]
        funct3 = instruction[17:20]
        rd = self.register_dict[instruction[20:25]]
        instr_name = ""

        self.reg_in_use[rd] = True

        if self.reg_in_use[rs1] or self.reg_in_use[rs2]:
            print("Data hazard")
            return [rd, None, False]

        self.graph_data["instruction_types"]["R"] += 1
        if funct7 == "0000000":
            if funct3 == "000":
                # add
                instr_name = "add"
                x = self.reg_val[rs1] + self.reg_val[rs2]
                
            
            elif funct3 == "001":
                # sll
                instr_name = "sll"
                x = self.reg_val[rs1] << self.reg_val[rs2]
                
            
            elif funct3 == "010":
                # slt
                instr_name = "slt"
                x = 1 if self.reg_val[rs1] < self.reg_val[rs2] else 0
                
            
            elif funct3 == "011":
                # sltu
                instr_name = "sltu"
                x = 1 if self.reg_val[rs1] < self.reg_val[rs2] else 0
                
            
            elif funct3 == "100":
                # xor
                instr_name = "xor"
                x = self.reg_val[rs1] ^ self.reg_val[rs2]
                

            elif funct3 == "101":
                # srl
                instr_name = "srl"
                x = self.reg_val[rs1] >> self.reg_val[rs2]
                
            elif funct3 == "110":
                # or
                instr_name = "or"
                x = self.reg_val[rs1] | self.reg_val[rs2]
                
            elif funct3 == "111":
                # and
                instr_name = "and"
                x = self.reg_val[rs1] & self.reg_val[rs2]
                
        elif funct7 == "0100000":
            if funct3 == "000":
                # sub
                instr_name = "sub"
                x = self.reg_val[rs1] - self.reg_val[rs2]
                
            elif funct3 == "101":
                # sra
                instr_name = "sra"
                x = self.reg_val[rs1] >> self.reg_val[rs2]
                
        print(f"{instr_name} {rd}, {rs1}, {rs2}")
        # self.print_reg_val()
        return [rd, x]

    def i_type(self, instruction):
        opcode = instruction[25:32]
        rs1 = self.register_dict[instruction[12:17]]
        rd = self.register_dict[instruction[20:25]]
        funct3 = instruction[17:20]
        imm = int(instruction[0:12], 2)
        instr_name = ""

        self.reg_in_use[rd] = True

        if self.reg_in_use[rs1]:
            print("Data hazard")
            return [rd, None, False]
        
        self.graph_data["instruction_types"]["I"] += 1

        if opcode == "0010011":
            if funct3 == "000":
                # addi
                instr_name = "addi"
                x = self.reg_val[rs1] + imm
            elif funct3 == "001":
                # slli
                instr_name = "slli"
                x = self.reg_val[rs1] << imm
            elif funct3 == "010":
                # slti
                instr_name = "slti"
                x = 1 if self.reg_val[rs1] < imm else 0
            elif funct3 == "011":
                # sltiu
                instr_name = "sltiu"
                x = 1 if self.reg_val[rs1] < imm else 0
            elif funct3 == "100":
                # xori
                instr_name = "xori"
                x = self.reg_val[rs1] ^ imm
            elif funct3 == "101":
                # srli
                instr_name = "srli"
                x = self.reg_val[rs1] >> imm
            elif funct3 == "110":
                # ori
                instr_name = "ori"
                x = self.reg_val[rs1] | imm
            elif funct3 == "111":
                # andi
                instr_name = "andi"
                x = self.reg_val[rs1] & imm
        elif opcode == "0000011":
            if funct3 == "000":
                # lb
                instr_name = "lb"
                x = self.dm.read(self.reg_val[rs1] + imm)

            elif funct3 == "001":
                # lh
                instr_name = "lh"
                x = self.dm.read(self.reg_val[rs1] + imm)
            elif funct3 == "010":
                # lw
                instr_name = "lw"
                x = self.dm.read(self.reg_val[rs1] + imm)
            elif funct3 == "011":
                # ld
                instr_name = "ld"
                x = self.dm.read(self.reg_val[rs1] + imm)
            elif funct3 == "100":
                # lbu
                instr_name = "lbu"
                x = self.dm.read(self.reg_val[rs1] + imm)
            elif funct3 == "101":
                # lhu
                instr_name = "lhu"
                x = self.dm.read(self.reg_val[rs1] + imm)
            elif funct3 == "110":
                # lwu
                instr_name = "lwu"
                x = self.dm.read(self.reg_val[rs1] + imm)
        elif opcode == "1100111":
            # jalr
            instr_name = "jalr"
            x = self.reg_val[rs1] + imm
        elif opcode == "1110011":
            # scall, sbreak
            if funct3 == "000":
                if imm == 0:
                    # scall
                    instr_name = "scall"
                elif imm == 1:
                    # sbreak
                    instr_name = "sbreak"

        print(f"{instr_name} {rd}, {rs1}, {imm}")
        # self.print_reg_val()
        return [rd, x]
    
    def s_type(self, instruction):
        opcode = instruction[25:32]
        rs1 = self.register_dict[instruction[12:17]]
        rs2 = self.register_dict[instruction[7:12]]
        funct3 = instruction[17:20]
        imm = int(instruction[0:7] + instruction[20:25], 2)
        instr_name = ""

        if self.reg_in_use[rs1] or self.reg_in_use[rs2]:
            print("Data hazard")
            return [rs1, None, False]
        
        self.graph_data["instruction_types"]["S"] += 1

        if opcode == "0100011":
            if funct3 == "000":
                # sb
                instr_name = "sb"
                x = imm + self.reg_val[rs2]
            elif funct3 == "001":
                # sh
                instr_name = "sh"
                x = imm + self.reg_val[rs2]
            elif funct3 == "010":
                # sw
                instr_name = "sw"
                x = imm + self.reg_val[rs2]
            # elif funct3 == "011":
            #     # sd
            #     instr_name = "sd"
            #     self.reg_val[rs1] = imm + self.reg_val[rs2]

        print(f"{instr_name} {rs1}, {imm}({rs2})")
        # self.print_reg_val()
        return [rs1, x]

    def sb_type(self, instruction):
        opcode = instruction[25:32]
        rs1 = self.register_dict[instruction[12:17]]
        rs2 = self.register_dict[instruction[7:12]]
        funct3 = instruction[17:20]
        imm = int("0" + instruction[0] + instruction[24] +
                  instruction[1:7] + instruction[20:24], 2)
        instr_name = ""

        if self.reg_in_use[rs1] or self.reg_in_use[rs2]:
            print("Data hazard")
            return [rs1, None, False]
        
        self.graph_data["instruction_types"]["SB"] += 1

        if opcode == "1100011":
            if funct3 == "000":
                # beq
                instr_name = "beq"
                if self.reg_val[rs1] == self.reg_val[rs2]:
                    imm = imm
                else:
                    imm = 0
            elif funct3 == "001":
                # bne
                instr_name = "bne"
                if self.reg_val[rs1] != self.reg_val[rs2]:
                    imm = imm
                else:
                    imm = 0
            elif funct3 == "100":
                # blt
                instr_name = "blt"
                if self.reg_val[rs1] < self.reg_val[rs2]:
                    imm = imm
                else:
                    imm = 0
            elif funct3 == "101":
                # bge
                instr_name = "bge"
                if self.reg_val[rs1] >= self.reg_val[rs2]:
                    imm = imm
                else:
                    imm = 0
            elif funct3 == "110":
                # bltu
                instr_name = "bltu"
                if self.reg_val[rs1] < self.reg_val[rs2]:
                    imm = imm
                else:
                    imm = 0
            elif funct3 == "111":
                # bgeu
                instr_name = "bgeu"
                if self.reg_val[rs1] >= self.reg_val[rs2]:
                    imm = imm
                else:
                    imm = 0
            

        print(f"{instr_name} {rs1}, {rs2}, {imm}")
        # self.print_reg_val()
        if imm != 0:
            self.program_counter = self.mar + imm - 1
            self.curr_decode = None
            self.curr_fetch = None
            self.branch_flag = True
            self.executed_instructions += imm
        return ["PC", imm]

    def u_type(self, instruction):
        opcode = instruction[25:32]
        rd = self.register_dict[instruction[20:25]]
        
        imm = int("000000000000" + instruction[0:20], 2)
        instr_name = ""

        self.reg_in_use[rd] = True

        self.graph_data["instruction_types"]["U"] += 1

        if opcode == "0110111":
            # lui
            instr_name = "lui"
            x = imm
        elif opcode == "0010111":
            # auipc
            instr_name = "auipc"
            if self.curr_fetch is None:
                x = imm + self.mar
            else:
                x = imm + self.mar - 1

        print(f"{instr_name} {rd}, {imm}")
        # self.print_reg_val()
        return [rd, x]

    def uj_type(self, instruction):
        opcode = instruction[25:32]
        rd = self.register_dict[instruction[20:25]]
        imm = int("0" + instruction[0] + instruction[12:20] +
                  instruction[11] + instruction[1:11], 2)
        instr_name = ""

        self.reg_in_use[rd] = True

        self.graph_data["instruction_types"]["UJ"] += 1

        if opcode == "1101111":
            # jal
            instr_name = "jal"
            x = imm

        print(f"{instr_name} {rd}, {imm}")
        # self.print_reg_val()
        return [rd, x]
    
    def custom_type(self, instruction):
        imm = int(instruction[0:12], 2)
        rs1 = self.register_dict[instruction[12:17]]
        rs2 = self.register_dict[instruction[20:25]]
        funct3 = instruction[17:20]

        self.graph_data["instruction_types"]["NOC"] += 1

        if funct3 == "010":
            if (self.reg_val[rs1] + imm) >= 1000 and (self.reg_val[rs1] + imm) <= 1003:
                x = str(self.reg_val[rs1] + imm)
                return [x, self.reg_val[rs2]]
                
        elif funct3 == "011":
            return [1004, 1]

# sim = Simulator()
# # # execute a r type instruction
# sim.run_simulator([
#     "0000000 00010 00011 000 00001 0110011", 
#     "0000000 00001 00010 000 00000 1100011", 
#     "0000000 00010 00011 000 00001 0110011", 
#     "0000000 00010 00011 000 00001 0110011", 
#     "0000000 00010 00011 000 00001 0110011", 
#     "00000000000000000000 00001 0110111", 
#     "0000000 00010 00011 000 00001 0110011"
#     ])

# # execute a i type instruction - addi
# sim.execute("000000000000 00001 00010 000 0010011")
# # sim.execute("000000000000 00001 00010 000 00001 0010011")

# # execute a s type instruction
# sim.execute("0000000 00010 00001 000 00000 0100011")

# # execute a sb type instruction
# sim.execute("0000000 00001 00010 000 00000 1100011")

# # execute a u type instruction
# sim.execute("00000000000000000000 00001 0110111")

# # execute a uj type instruction
# sim.execute("00000000000000000000 00001 1101111")
