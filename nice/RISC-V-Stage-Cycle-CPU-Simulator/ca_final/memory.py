import random

class DataMemory:
    def __init__(self):
        self.memory = {}
        self.max_size = 1024
        self.read_count = 0
        self.write_count = 0

        self.memory_mapped_registers = {
            "1000": 0,
            "1001": 0,
            "1002": 0,
            "1003": 0,
            "1004": 0,
        }

    def read_mmr(self, address):
        if address in self.memory_mapped_registers:
            self.read_count += 1
            return self.memory_mapped_registers[address]
        else:
            return None
        
    def write_mmr(self, address, data):
        if address in self.memory_mapped_registers:
            self.write_count += 1
            self.memory_mapped_registers[address] = data
        else:
            raise ValueError("Address out of range")
        
    def print_mmr_values(self):
        print("Register Values:")
        for i in range(1000, 1005):
            print("MMR" + str(i) + ": " + str(self.memory_mapped_registers[str(i)]))

    def read(self, address):
        if address in self.memory:
            self.read_count += 1
            return self.memory[address]
        else:
            return None
        
    

    def write(self, address, data):
        if address < self.max_size:
            self.write_count += 1
            self.memory[address] = data
        else:
            raise ValueError("Address out of range")
    
    def assign_random_values(self):
        for i in range(1024):
            self.memory[i] = random.randint(0, 100)
