from assembler_final import Assembler
from simulator import Simulator


class CPU:
    def __init__(self):
        self.assembler = Assembler()
        self.simulator = Simulator()

    def read_file(self, filename):
        with open(filename, 'r') as f:
            instructions = f.readlines()
        return instructions

    def encode(self, instructions):
        encoded_instructions = []
        for instruction in instructions:
            encoded_instruction = self.assembler.encode_instruction(
                instruction)
            print(instruction + ' -> ' + encoded_instruction)
            encoded_instructions.append(encoded_instruction)
        return encoded_instructions

    def execute(self, encoded_instructions):
        self.simulator.run_simulator(encoded_instructions)
        self.simulator.make_graph()

    def createLogFile(self, encoded_instructions):
        with open('log.txt', 'w') as f:
            for instruction in encoded_instructions:
                f.write(instruction + '\n')


if __name__ == '__main__':
    cpu = CPU()
    instructions = cpu.read_file('test_file.txt')
    encoded_instructions = cpu.encode(instructions)
    cpu.createLogFile(encoded_instructions)
    instructions = cpu.read_file('log.txt')
    cpu.execute(instructions)
