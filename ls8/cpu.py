"""CPU functionality."""

import sys

hard_code_program = [
    # From print8.ls8
    0b10000010, # LDI R0,8
    0b00000000,
    0b00001000,
    0b01000111, # PRN R0
    0b00000000,
    0b00000001, # HLT
]

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.PC = 0
        self.running = True
        self.register = [0] * 8 
        self.FL = 0b00000000
    
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self, file = hard_code_program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        hard_code_program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in file:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # Power Up
        # PC = 0
        SP = 7 # Stack Pointer
        self.register[SP] = 0xf4
        self.running = True

        def LDI(operand_a, operand_b):
            # print('LDI ran...')
            self.register[operand_a] = operand_b
            self.PC += 3

        def PRN(operand_a, operand_b):
            # print('PRN ran...')
            print(self.register[operand_a])
            self.PC += 2

        def MUL(operand_a, operand_b):
            self.register[operand_a] = self.register[operand_a] * self.register[operand_b]
            self.PC += 3

        def HLT(operand_a, operand_b):
            self.running = False
        
        def PUSH(operand_a, operand_b):
            self.register[SP] -= 1
            self.ram[self.register[SP]] = self.register[operand_a]
            self.PC += 2
        
        def POP(operand_a, operand_b):
            self.register[operand_a] = self.ram[self.register[SP]]
            self.register[SP] += 1
            self.PC += 2

        def CALL(operand_a, operand_b):
            # print('Call ran...')
            return_address = self.PC + 2
            # print('return address: ', return_address)

            self.register[SP] -= 1
            self.ram[self.register[SP]] = return_address


            reg_num = self.ram[self.PC+1]
            subroutine_address = self.register[reg_num]

            self.PC = subroutine_address

        def RET(operand_a, operand_b):
            # print('RET ran...')
            # print('before set PC: ', self.PC)
            self.PC = self.ram[self.register[SP]]
            # print('after set PC: ', self.PC)
            self.register[SP] += 1


        def ADD(operand_a, operand_b):
            self.register[operand_a] = self.register[operand_a] + self.register[operand_b]
            self.PC += 3

        def CMP(operand_a, operand_b):
            if (self.register[operand_a] == self.register[operand_b]):
                # print('set flag to equal')
                self.FL = 0b00000001
            elif (self.register[operand_a] < self.register[operand_b]):
                # print('set flag to less than')
                self.FL = 0b00000100
            elif (self.register[operand_a] > self.register[operand_b]):
                # print('set flag to greater than')
                self.FL = 0b00000010
            self.PC += 3

        def JMP(operand_a, operand_b):
            self.PC = self.register[operand_a]

        def JEQ(operand_a, operand_b):
            # print('FL: ', self.FL)
            if(self.FL == 0b00000001):
                # print('JEQ: its equal! jump!')
                self.PC = self.register[operand_a]
            else:
                # print('JEQ: its not equal! DONT jump!')
                self.PC += 2
        def JNE(operand_a, operand_b):
            # print('FL: ', self.FL)
            total = self.FL & 0b00000001
            if (total == 0):
                # print('JNE: its not equal! JUMP!')
                # print('jumping to: ', self.register[operand_a])
                self.PC = self.register[operand_a]
            else:
                # print('JNE: its not equal! DONT jump!')
                self.PC += 2


        branch_table = {
            0b10000010 : LDI,
            0b01000111 : PRN,
            0b00000001 : HLT,
            0b10100010 : MUL,
            0b01000101 : PUSH,
            0b01000110 : POP,
            0b01010000 : CALL,
            0b00010001 : RET,
            0b10100000 : ADD,
            0b10100111 : CMP,
            0b01010100 : JMP,
            0b01010101 : JEQ,
            0b01010110 : JNE

        }


        while self.running:
            try:
                IR = self.ram[self.PC]
                # print('in try: ', bin(IR))
                operand_a = self.ram[self.PC + 1]
                operand_b = self.ram[self.PC + 2]

                branch_table[IR](operand_a, operand_b)
            except:
                # print('broke here PC: ', self.PC)
                # print('broke here IR: ', IR)
                break
 