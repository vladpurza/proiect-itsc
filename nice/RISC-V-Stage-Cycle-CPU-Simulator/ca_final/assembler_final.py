class Assembler:
    def __init__(self):
        self.register_dict = {
            "r0": "00000",
            "r1": "00001",
            "r2": "00010",
            "r3": "00011",
            "r4": "00100",
            "r5": "00101",
            "r6": "00110",
            "r7": "00111",
            "r8": "01000",
            "r9": "01001",
            "r10": "01010",
            "r11": "01011",
            "r12": "01100",
            "r13": "01101",
            "r14": "01110",
            "r15": "01111",
            "r16": "10000",
            "r17": "10001",
            "r18": "10010",
            "r19": "10011",
            "r20": "10100",
            "r21": "10101",
            "r22": "10110",
            "r23": "10111",
            "r24": "11000",
            "r25": "11001",
            "r26": "11010",
            "r27": "11011",
            "r28": "11100",
            "r29": "11101",
            "r30": "11110",
            "r31": "11111"
        }

        self.type_dict = {
            "SLLI": "0010011",
            "SRLI": "0010011",
            "SRAI": "0010011",
            "ADD": "0110011",
            "SUB": "0110011",
            "SLL": "0110011",
            "SLT": "0110011",
            "SLTU": "0110011",
            "XOR": "0110011",
            "SRL": "0110011",
            "SRA": "0110011",
            "OR": "0110011",
            "AND": "0110011",
            "JALR": "1100111",
            "LB": "0000011",
            "LH": "0000011",
            "LW": "0000011",
            "LBU": "0000011",
            "LHU": "0000011",
            "ADDI": "0010011",
            "SLTI": "0010011",
            "SLTIU": "0010011",
            "ORI": "0010011",
            "ANDI": "0010011",
            "BEQ": "1100011",
            "BNE": "1100011",
            "BLT": "1100011",
            "BGE": "1100011",
            "BLTU": "1100011",
            "BGEU": "1100011",
            "JAL": "1101111",
            "LUI": "0110111",
            "AUIPC": "0010111",
            "XORI": "0010011",
            
            
        }

        self.type_U = {

            "LUI": "0110111",
            "AUIPC": "0010111"
        }

        self.type_R = {
            "SLLI": "0010011",
            "SRLI": "0010011",
            "SRAI": "0010011",
            "ADD": "0110011",
            "SUB": "0110011",
            "SLL": "0110011",
            "SLT": "0110011",
            "SLTU": "0110011",
            "XOR": "0110011",
            "SRL": "0110011",
            "SRA": "0110011",
            "OR": "0110011",
            "AND": "0110011"
        }
        self.I_type = {
            "JALR": "1100111",

            "LB": "0000011",
            "LH": "0000011",
            "LW": "0000011",
            "LBU": "0000011",
            "LHU": "0000011",


            "ADDI": "0010011",
            "SLTI": "0010011",
            "SLTIU": "0010011",
            "XORI": "0010011",
            "ORI": "0010011",
            "ANDI": "0010011"


        }

        self.uj_type = {
            "JAL": "1101111"
        }

        self.sb_type = {
            "BEQ": "1100011",
            "BNE": "1100011",
            "BLT": "1100011",
            "BGE": "1100011",
            "BLTU": "1100011",
            "BGEU": "1100011"
        }
        

    def getval(self, d, i):
        return d[i]

    def imm_access(self, val, total):

        imm = bin(val)[2:].zfill(total)
        if(val < 0):
            abs_value = abs(val)
            imm = bin(abs_value)[2:].zfill(total)
            inverted_binary = ''.join(
                '1' if bit == '0' else '0' for bit in imm)

            carry = 1
            result = []
            for bit in reversed(inverted_binary):
                if bit == '0':
                    result.insert(0, str(carry))
                    carry = 0
                else:
                    result.insert(0, '1' if carry == 0 else '0')

            imm = ''.join(result)

        return imm

    def encode_instruction(self, instruction):
        l = instruction.split()
        l[0] = l[0].upper()
        # type R completed

        if l[0] == "SLLI":
            shamt_binary = format(int(l[3]), '05b')
            rs1_binary = self.getval(self.register_dict, l[2])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0010011"
            funct3 = "001"
            return "0000000"+" "+str(shamt_binary)+" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode
        elif l[0] == "SRLI":
            shamt_binary = format(int(l[3]), '05b')
            rs1_binary = self.getval(self.register_dict, l[2])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0010011"
            funct3 = "101"  # Funct3 for SRLI
            return "0000000"+" "+str(shamt_binary)+" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode
        elif l[0] == "SRAI":
            shamt_binary = format(int(l[3]), '05b')
            rs1_binary = self.getval(self.register_dict, l[2])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0010011"
            funct3 = "101"  # Funct3 for SRAI
            return "0100000"+" "+str(shamt_binary)+ " " + rs1_binary+ " " + funct3+ " " + rd_binary+ " " + opcode

        elif l[0] == "ADD":         # Done
            # ADD RD R2 R3
            rs1_binary = self.getval(self.register_dict, l[2])
            rs2_binary = self.getval(self.register_dict, l[3])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0110011"
            funct3 = "000"  # Funct3 for ADD
            return "0000000" + " " + rs2_binary + " " + rs1_binary + " " + funct3 + " " + rd_binary + " " + opcode

        elif l[0] == "SUB":            # Done

            rs1_binary = self.getval(self.register_dict, l[2])
            rs2_binary = self.getval(self.register_dict, l[3])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0110011"
            funct3 = "000"  # Funct3 for SUB
            return "0100000" + " " + rs2_binary + " " + rs1_binary + " " + funct3 + " " + rd_binary + " " + opcode

        elif l[0] == "SLL":  # Done

            rs1_binary = self.getval(self.register_dict, l[2])
            rs2_binary = self.getval(self.register_dict, l[3])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0110011"
            funct3 = "001"  # Funct3 for SLL
            return "0000000" + " " + rs2_binary + " " + rs1_binary + " " + funct3 + " " + rd_binary + " " + opcode

        elif l[0] == "SLT":  # Done
            rs1_binary = self.getval(self.register_dict, l[2])
            rs2_binary = self.getval(self.register_dict, l[3])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0110011"
            funct3 = "010"  # Funct3 for SLT
            return "0000000" + " " + rs2_binary + " " + rs1_binary + " " + funct3 + " " + rd_binary + " " + opcode

        elif l[0] == "SLTU":  # Done
            rs1_binary = self.getval(self.register_dict, l[2])
            rs2_binary = self.getval(self.register_dict, l[3])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0110011"
            funct3 = "011"  # Funct3 for SLTU
            return "0000000" + " " + rs2_binary + " " + rs1_binary + " " + funct3 + " " + rd_binary + " " + opcode

        elif l[0] == "XOR":  # Done
            rs1_binary = self.getval(self.register_dict, l[2])
            rs2_binary = self.getval(self.register_dict, l[3])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0110011"
            funct3 = "100"  # Funct3 for XOR
            return "0000000" + " " + rs2_binary + " " + rs1_binary + " " + funct3 + " " + rd_binary + " " + opcode

        elif l[0] == "SRL":    # Done

            rs1_binary = self.getval(self.register_dict, l[2])
            rs2_binary = self.getval(self.register_dict, l[3])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0110011"
            funct3 = "101"  # Funct3 for SRL
            return "0000000" + " " + rs2_binary + " " + rs1_binary + " " + funct3 + " " + rd_binary + " " + opcode

        elif l[0] == "SRA":     # Done

            rs1_binary = self.getval(self.register_dict, l[2])
            rs2_binary = self.getval(self.register_dict, l[3])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0110011"
            funct3 = "101"  # Funct3 for SRA
            return "0100000" + " " + rs2_binary + " " + rs1_binary + " " + funct3 + " " + rd_binary + " " + opcode

        elif l[0] == "OR":  # Done
            rs1_binary = self.getval(self.register_dict, l[2])
            rs2_binary = self.getval(self.register_dict, l[3])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0110011"
            funct3 = "110"  # Funct3 for OR
            return "0000000" + " " + rs2_binary + " " + rs1_binary + " " + funct3 + " " + rd_binary + " " + opcode

        elif l[0] == "AND":      # Done
            rs1_binary = self.getval(self.register_dict, l[2])
            rs2_binary = self.getval(self.register_dict, l[3])
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0110011"
            funct3 = "111"  # Funct3 for AND
            return "0000000" + " " + rs2_binary + " " + rs1_binary + " " + funct3 + " " + rd_binary + " " + opcode

        elif l[0] == "SB":  # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
           
            # Get the binary representation of rs2
            rs2_binary = self.getval(self.register_dict, l[2])
            # Get the binary representation of rs1
            rs1_binary = self.getval(self.register_dict, l[1])
            opcode = "0100011"  # Opcode for SH
            funct3 = "000"  # Funct3 for SH
            return imm_binary[0:7]+" " + rs2_binary+" " + rs1_binary+" " + funct3+" " + imm_binary[7:12]+" " + opcode

        elif l[0] == "SH":    # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
            imm_binary = imm_binary[::-1]
            # Get the binary representation of rs2
            rs2_binary = self.getval(self.register_dict, l[2])
            # Get the binary representation of rs1
            rs1_binary = self.getval(self.register_dict, l[1])
            opcode = "0100011"  # Opcode for SH
            funct3 = "001"  # Funct3 for SH
            return imm_binary[0:7]+" " + rs2_binary +" "+ rs1_binary+" " + funct3+" " + imm_binary[7:12]+" " + opcode

        elif l[0] == "SW":    # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
           
            # Get the binary representation of rs2
            rs2_binary = self.getval(self.register_dict, l[2])
            # Get the binary representation of rs1
            rs1_binary = self.getval(self.register_dict, l[1])
            opcode = "0100011"  # Opcode for SW
            funct3 = "010"  # Funct3 for SW
            return imm_binary[0:7]+" " + rs2_binary+" " + rs1_binary+" " + funct3+" " + imm_binary[7:12]+" " + opcode

        elif l[0] == "LB":    # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
           
            rd_binary = self.getval(self.register_dict, l[1])
            rs1_binary = self.getval(self.register_dict, l[2])
            opcode = "0000011"  # Opcode for LB
            funct3 = "000"  # Funct3 for LB

            return imm_binary +" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode

        elif l[0] == "LH":     # done

            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
            
            rd_binary = self.getval(self.register_dict, l[1])
            rs1_binary = self.getval(self.register_dict, l[2])
            opcode = "0000011"  # Opcode for LH
            funct3 = "001"  # Funct3 for LH
            return imm_binary +" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode

        elif l[0] == "LW":      # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
           
            rd_binary = self.getval(self.register_dict, l[1])
            rs1_binary = self.getval(self.register_dict, l[2])
            opcode = "0000011"  # Opcode for LW
            funct3 = "010"  # Funct3 for LW
            return imm_binary +" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode

        elif l[0] == "LBU":     # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
            
            rd_binary = self.getval(self.register_dict, l[1])
            rs1_binary = self.getval(self.register_dict, l[2])
            opcode = "0000011"  # Opcode for LBU
            funct3 = "100"  # Funct3 for LBU
            return imm_binary +" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode
        elif l[0] == "LHU":     # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
            
            rd_binary = self.getval(self.register_dict, l[1])
            rs1_binary = self.getval(self.register_dict, l[2])
            opcode = "0000011"  # Opcode for LHU
            funct3 = "101"  # Funct3 for LHU
            return imm_binary +" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode

        elif l[0] == "ADDI":   # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')

            rd_binary = self.getval(self.register_dict, l[1])
            rs1_binary = self.getval(self.register_dict, l[2])
            opcode = "0010011"
            funct3 = "000"  # Funct3 for ADDI
            return imm_binary +" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode

        elif l[0] == "SLTI":  # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
            
            rd_binary = self.getval(self.register_dict, l[1])
            rs1_binary = self.getval(self.register_dict, l[2])
            opcode = "0010011"
            funct3 = "010"  # Funct3 for SLTI
            return imm_binary +" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode

        elif l[0] == "SLTIU":  # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
            
            rd_binary = self.getval(self.register_dict, l[1])
            rs1_binary = self.getval(self.register_dict, l[2])
            opcode = "0010011"
            funct3 = "011"  # Funct3 for SLTIU
            return imm_binary +" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode

        elif l[0] == "XORI":   # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
            
            rd_binary = self.getval(self.register_dict, l[1])
            rs1_binary = self.getval(self.register_dict, l[2])
            opcode = "0010011"
            funct3 = "100"  # Funct3 for XORI
            return imm_binary +" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode

        elif l[0] == "ORI":   # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
            
            rd_binary = self.getval(self.register_dict, l[1])
            rs1_binary = self.getval(self.register_dict, l[2])
            opcode = "0010011"
            funct3 = "110"  # Funct3 for ORI
            return imm_binary +" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode
        elif l[0] == "ANDI":    # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
            
            rd_binary = self.getval(self.register_dict, l[1])
            rs1_binary = self.getval(self.register_dict, l[2])
            opcode = "0010011"
            funct3 = "111"  # Funct3 for ANDI
            return imm_binary +" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode

        
        elif l[0] == "BEQ":    # done

            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
            imm_binary = imm_binary[::-1]
            # Get the binary representation of rs2
            rs2_binary = self.getval(self.register_dict, l[2])
            # Get the binary representation of rs1
            rs1_binary = self.getval(self.register_dict, l[1])

            opcode = "1100011"  # Opcode for BEQ
            funct3 = "000"  # Funct3 for BEQ

            # Combine the fields to form the instruction
            return imm_binary[11]+imm_binary[9:3:-1]+ " " + rs2_binary+ " " + rs1_binary+ " " + funct3+ " " + imm_binary[3::-1]+ " "+imm_binary[10]+ " " + opcode

        elif l[0] == "BNE":     # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 12-bit binary
                imm_binary = format(int(l[3]), '012b')
            imm_binary = imm_binary[::-1]
            # Get the binary representation of rs2
            rs2_binary = self.getval(self.register_dict, l[2])
            # Get the binary representation of rs1
            rs1_binary = self.getval(self.register_dict, l[1])

            opcode = "1100011" # Opcode for BNE
            funct3 = "001"  # Funct3 for BNE
            return imm_binary[11] + imm_binary[9:3:-1]+ " " + rs2_binary+ " " + rs1_binary+ " " + funct3+ " " + imm_binary[3::-1]+ " "+imm_binary[10]+ " " + opcode

        elif l[0] == "BLT":    # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                imm_binary = format(int(l[3]), '012b')
            imm_binary = imm_binary[::-1]
            rs2_binary = self.getval(self.register_dict, l[2])
            rs1_binary = self.getval(self.register_dict, l[1])

            opcode = "1100011"
            funct3 = "100"
            return imm_binary[11] + imm_binary[9:3:-1]+ " " + rs2_binary+ " " + rs1_binary+ " " + funct3+ " " + imm_binary[3::-1]+ " "+imm_binary[10]+ " " + opcode

        elif l[0] == "BGE":   # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                imm_binary = format(int(l[3]), '012b')
            imm_binary = imm_binary[::-1]
            rs2_binary = self.getval(self.register_dict, l[2])
            rs1_binary = self.getval(self.register_dict, l[1])
            opcode = "1100011" # Opcode for BGE
            funct3 = "101"  # Funct3 for BGE
            return imm_binary[11] + imm_binary[9:3:-1]+ " " + rs2_binary+ " " + rs1_binary+ " " + funct3+ " " + imm_binary[3::-1]+ " "+imm_binary[10]+ " " + opcode

        elif l[0] == "BLTU":    # done

            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                imm_binary = format(int(l[3]), '012b')
            imm_binary = imm_binary[::-1]
            rs2_binary = self.getval(self.register_dict, l[2])
            rs1_binary = self.getval(self.register_dict, l[1])
            opcode = "1100011" # Opcode for BLTU
            funct3 = "110"  # Funct3 for BLTU
            return imm_binary[11] + imm_binary[9:3:-1]+ " "+ rs2_binary+ " " + rs1_binary + " "+ funct3 + " "+ imm_binary[3::-1]+ " "+imm_binary[10]+ " " + opcode

        elif l[0] == "BGEU":     # done
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                imm_binary = format(int(l[3]), '012b')
            imm_binary = imm_binary[::-1]
            rs2_binary = self.getval(self.register_dict, l[2])
            rs1_binary = self.getval(self.register_dict, l[1])
            opcode = "1100011" # Opcode for BGEU
            funct3 = "111"  # Funct3 for BGEU
            return imm_binary[11]+ imm_binary[9:3:-1]+ " " + rs2_binary+ " " + rs1_binary+ " " + funct3+ " " + imm_binary[3::-1]+ " "+imm_binary[10]+ " " + opcode

        elif l[0] == "LUI":
            if (int(l[2]) < 0):
                imm_binary = self.imm_access(int(l[2]), 20)

            else:
                # Convert immediate to 32-bit binary
                imm_binary = format(int(l[2]), '020b')
            # imm_binary = imm_binary[::-1]
            # Get the binary representation of rd
            rd_binary = self.getval(self.register_dict, l[1])

            opcode = "0110111"  # Opcode for LUI

            # Combine the fields to form the instruction
            return imm_binary+" " + rd_binary + " " + opcode

        elif l[0] == "AUIPC":
            if (int(l[2]) < 0):
                imm_binary = self.imm_access(int(l[2]), 20)
            else:
                # Convert immediate to 32-bit binary
                imm_binary = format(int(l[2]), '020b')
            # imm_binary = imm_binary[::-1]
            # Get the binary representation of rd
            rd_binary = self.getval(self.register_dict, l[1])
            opcode = "0010111"  # Opcode for AUIPC
            return imm_binary +" " + rd_binary + " " + opcode

        elif l[0] == "LOADNOC":
            if (int(l[3]) < 0):
                imm_binary = self.imm_access(int(l[3]), 12)
            else:
                # Convert immediate to 32-bit binary
                imm_binary = format(int(l[3]), '012b')
            opcode="1111111"
            funct3="010"
            rs2_binary = self.getval(self.register_dict, l[1])
            rs1_binary = self.getval(self.register_dict, l[2])

            return imm_binary +" " + rs1_binary+" " + funct3+" " + rs2_binary+" " + opcode
        elif l[0]=="STORENOC":
            
            
            opcode="1111111"
            rd_binary = "00001"
            rs1_binary="00001"
            funct3="011"
            imm_binary="000000001111"
            return imm_binary +" " + rs1_binary+" " + funct3+" " + rd_binary+" " + opcode