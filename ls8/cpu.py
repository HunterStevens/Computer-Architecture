"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MULT = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 0xF4

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print("You must enter the ls8.py and then the name of the ls8 file.")
            sys.exit()
        address = 0

        program = open(sys.argv[1], 'r')

        try:
            for instruction in program:
                comment = False
                insert = ""
                for char in instruction:
                    if char == "#":
                        comment = True
                    if comment == True:
                        break
                    elif char == "\n":
                        pass
                    else:
                        insert += str(char)
                if insert == "":
                    pass
                else:
                    self.ram[address] = int(insert,2)
                    address += 1
        except FileNotFoundError:
            print ("file not found")
            sys.exit()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.ram[reg_a] += self.ram[reg_b]
        elif op == "MULT":
            self.ram[reg_a] *= self.ram[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
        return

    def stack(self, op, value = None):
        if op == "PUSH":
            self.sp -= 1
            self.ram_write(self.sp, value)
            return
        elif op == "POP":
            if self.sp < 0xF4:
                pop_value = self.ram_read(self.sp)
                # print(pop_value, " <-- Pop_value")
                self.sp += 1
                return pop_value
            else:
                print("ERROR: Stack is empty")
                return


    def run(self):
        """Run the CPU."""
        while True:
            ir = self.ram_read(self.pc)
            byt_a = self.ram_read(self.pc + 1)
            byt_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                break
            elif ir == LDI:
                self.ram[byt_a] = byt_b
                self.pc += 3
            elif ir == PRN:
                print(self.ram[byt_a], "\n")
                self.pc += 2
            elif ir == MULT:
                self.alu("MULT", byt_a, byt_b)
                self.pc += 3
            elif ir == ADD:
                self.alu("ADD", byt_a, byt_b)
                self.pc += 3
            elif ir == PUSH:
                self.stack("PUSH", self.ram[byt_a])
                # print(self.reg[byt_a], " <-- self.reg[byt_a]")
                self.pc += 2
            elif ir == POP:
                value = self.stack("POP")
                self.ram[byt_a] = value
                self.pc += 2
            else:
                print(f"Unknown Instruction {ir}")
                if self.pc < len(self.ram)-1:
                    self.pc += 1
                else:
                    ir = HLT
        pass
