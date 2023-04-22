import random
#import os
#import time

class Chip8:
    registers    = [0x0] * 16
    memory       = [0x0] * 4096
    index        = 0
    stack        = [0x0] * 16
    pc           = 0
    sp           = 0
    delayTimer   = 0
    soundTimer   = 0
    keypad       = [0x0] * 16
    video        = [0x0] * (64 * 32)
    opcode : int = 0

    START_ADDRESS         : int  = 0x200
    FONTSET_START_ADDRESS : int  = 0x50
    FONTSET_SIZE          : int  = 80
    DEBUG                 : bool = False

    font_set = [
        0xF0, 0x90, 0x90, 0x90, 0xF0, 
    	0x20, 0x60, 0x20, 0x20, 0x70, 
    	0xF0, 0x10, 0xF0, 0x80, 0xF0, 
    	0xF0, 0x10, 0xF0, 0x10, 0xF0, 
    	0x90, 0x90, 0xF0, 0x10, 0x10, 
    	0xF0, 0x80, 0xF0, 0x10, 0xF0, 
    	0xF0, 0x80, 0xF0, 0x90, 0xF0, 
    	0xF0, 0x10, 0x20, 0x40, 0x40, 
    	0xF0, 0x90, 0xF0, 0x90, 0xF0, 
    	0xF0, 0x90, 0xF0, 0x10, 0xF0, 
    	0xF0, 0x90, 0xF0, 0x90, 0x90, 
    	0xE0, 0x90, 0xE0, 0x90, 0xE0, 
    	0xF0, 0x80, 0x80, 0x80, 0xF0, 
    	0xE0, 0x90, 0x90, 0x90, 0xE0, 
    	0xF0, 0x80, 0xF0, 0x80, 0xF0, 
    	0xF0, 0x80, 0xF0, 0x80, 0x80  
    ]   

    def __init__(self):
        self.pc = self.START_ADDRESS

        for i in range(self.FONTSET_SIZE):
            self.memory[self.FONTSET_START_ADDRESS + i] = self.font_set[i]

    def op_NULL(self):
        print('unknown operator')

    def rand_byte(self):
        return random.randint(0,255)
        
    def load_rom(self, file):
        """
        Load the ROM file into memory.
        args: file
        """

        with open(file, 'br') as f:
            i : int = 0
            while i == f.tell():
                self.memory[self.START_ADDRESS + i] = int.from_bytes(f.read(1), 'big')
                #self.memory[self.START_ADDRESS + i] = f.read(1).hex()

                i += 1
            #print(self.memory[0x200:0x400])

    def op_00E0(self):
        """
            Clear the video buffer.
        """
        if self.DEBUG:
            print('00E0')

        self.video = [0] * len(self.video)

    def op_00EE(self):
        """
            Return from a subroutine.
        """
        if self.DEBUG:
            print('00EE')

        self.sp -= 1
        self.pc = self.stack[self.sp]

    def op_1nnn(self):
        """
            Jump to location nnn.
        """
        if self.DEBUG:
            print('1nnn')

        address = self.opcode & 0x0FFF
        self.pc = address
    
    def op_2nnn(self):
        """
            Call subroutine at nnn.
        """
        if self.DEBUG:
            print('2nnn')

        address = self.opcode & 0x0FFF

        self.stack[self.sp] = self.pc
        self.sp += 1
        self.pc = address

    def op_3xkk(self):
        """
            skip next instruction if Vx = kk.
        """
        if self.DEBUG:
            print('3xkk')

        Vx = (self.opcode & 0x0F00) >> 8
        byte = self.opcode & 0x00FF

        if self.registers[Vx] == byte:
            self.pc += 2

    def op_4xkk(self):
        """
            skip next instruction if Vx != kk.
        """
        if self.DEBUG:
            print('4xkk')

        Vx = (self.opcode & 0x0F00) >> 8
        byte = self.opcode & 0x00FF

        if self.registers[Vx] != byte:
            self.pc += 2

    def op_5xy0(self):
        """
            skip next instruction if Vx = Vy.
        """
        if self.DEBUG:
            print('5xy0')

        Vx = (self.opcode & 0x0F00) >> 8
        Vy = (self.opcode & 0X00F0) >> 4

        if self.registers[Vx] == self.registers[Vy]:
            self.pc += 2
    
    def op_6xkk(self):
        """
            Set Vx = kk.
        """
        if self.DEBUG:
            print('6xkk')

        Vx = (self.opcode & 0x0F00) >> 8
        byte = self.opcode & 0x00FF

        self.registers[Vx] = byte

    def op_7xkk(self):
        """
            Set Vx = Vx + kk.
        """
        if self.DEBUG:
            print('7xkk')

        Vx = (self.opcode & 0x0F00) >> 8
        byte = self.opcode & 0x00FF

        self.registers[Vx] += byte

    def op_8xy0(self):
        """
            Set Vx = Vy.
        """
        if self.DEBUG:
            print('8xy0')

        Vx = (self.opcode & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4

        self.registers[Vx] = self.registers[Vy]
    
    def op_8xy1(self):
        """
            Set Vx = Vx OR Vy.
        """
        if self.DEBUG:
            print('8xy1')

        Vx = (self.opcode & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4

        self.registers[Vx] |= self.registers[Vy]

    def op_8xy2(self):
        """
            Set Vx = Vx AND Vy.
        """
        if self.DEBUG:
            print('8xy2')

        Vx = (self.opcode & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4

        self.registers[Vx] &= self.registers[Vy]

    def op_8xy3(self):
        """
            Set Vx = Vx XOR Vy.
        """
        if self.DEBUG:
            print('8xy3')

        Vx = (self.opcode & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4

        self.registers[Vx] ^= self.registers[Vy]

    def op_8xy4(self):
        """
            Set Vx = Vx + Vy, set VF = carry.

            The values of Vx and Vy are added together. If the result is greater than 8 bits (i.e., > 255,)
            VF is set to 1, otherwise 0. Only the lowest 8 bits of the result are kept, and stored in Vx.
        """
        if self.DEBUG:
            print('8xy4')

        Vx = (self.opcode & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4

        _sum = self.registers[Vx] + self.registers[Vy]

        if _sum > 255:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0

        self.registers[Vx] = _sum & 0xFF

    def op_8xy5(self):
        """
            Set Vx = Vx - Vy, set VF = NOT borrow.

            If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted from Vx, and the results stored in Vx.
        """
        if self.DEBUG:
            print('8xy5')

        Vx = (self.opcode & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4
        
        if self.registers[Vx] > self.registers[Vy]:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0

        self.registers[Vx] -= self.registers[Vy]

    def op_8xy6(self):
        """
            Set Vx = Vx SHR 1.

            If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0. Then Vx is divided by 2.
        """
        if self.DEBUG:
            print('8xy6')

        Vx = (self.opcode & 0x0F00) >> 8

        self.registers[0xF] = (self.registers[Vx] & 0x1)
        self.registers[Vx] >>= 1

    def op_8xy7(self):
        """
            Set Vx = Vy - Vx, set VF = NOT borrow.

            If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted from Vy, and the results stored in Vx.
        """
        if self.DEBUG:
            print('8xy7')

        Vx = (self.opcode & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4
        
        if self.registers[Vy] > self.registers[Vx]:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0
        self.registers[Vx] = self.registers[Vy] - self.registers[Vx]
    
    def op_8xyE(self):
        """
            Set Vx = Vx SHL 1.

            If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0. Then Vx is multiplied by 2.
        """
        if self.DEBUG:
            print('8xyE')

        Vx = (self.opcode & 0x0F00) >> 8

        self.registers[0xF] = (self.registers[Vx] & 0x80) >> 7
        self.registers[Vx] <<= 1
    
    def op_9xy0(self):
        """
            Skip next instruction if Vx != Vy.
        """
        if self.DEBUG:
            print('9xy0')

        Vx = (self.opcode & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4

        if self.registers[Vx] != self.registers[Vy]:
            self.pc += 2

    def op_Annn(self):
        """
            Set I = nnn.
        """
        if self.DEBUG:
            print('Annn')

        address = self.opcode & 0x0FFF
        self.index = address

    def op_Bnnn(self):
        """
            Jump to location nnn + V0.
        """
        if self.DEBUG:
            print('Bnnn')

        address = self.opcode & 0x0FFF
        self.pc = self.registers[0] + address
    
    def op_Cxkk(self):
        """
            Set Vx = random byte AND kk.

        """
        if self.DEBUG:
            print('Cxkk')

        Vx = (self.opcode & 0x0F00) >> 8
        byte = self.opcode & 0x00FF

        self.registers[Vx] = self.rand_byte() & byte

    def op_Dxyn(self):
        """
            Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
        """
        if self.DEBUG:
            print('Dxyn')

        Vx = (self.opcode & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4
        height = self.opcode & 0x000F

        x_pos = self.registers[Vx] % 64
        y_pos = self.registers[Vy] % 32

        self.registers[0xF] = 0
        
        for row in range(height):
            sprite_byte = self.memory[self.index + row]
            for col in range(8):
                sprite_pixel = sprite_byte & (0x80 >> col)
                screen_pixel = self.video[(y_pos + row) * 64 + (x_pos + col)]

                if sprite_pixel:
                    if screen_pixel == 0xFFFFFFFF:
                        self.registers[0xF] = 1
                    self.video[(y_pos + row) * 64 + (x_pos + col)] ^= 0xFFFFFFFF

    def op_Ex9E(self):
        """
            Skip next instruction if key with the value of Vx is pressed.
        """
        if self.DEBUG:
            print('Ex9E')

        Vx = (self.opcode & 0x0F00) >> 8
        key = self.registers[Vx]

        if self.keypad[key]:
            self.pc += 2
    
    def op_ExA1(self):
        """
            Skip next instruction if key with the value of Vx is not pressed.
        """
        if self.DEBUG:
            print('ExA1')

        Vx = (self.opcode & 0x0F00) >> 8

        key = self.registers[Vx]

        if not self.keypad[key]:
            self.pc += 2

    def op_Fx07(self):
        """
            Set Vx = delay timer value.
        """
        if self.DEBUG:
            print('Fx07')

        Vx = (self.opcode & 0x0F00) >> 8
        
        self.registers[Vx] = self.delayTimer

    def op_Fx0A(self):
        """
            Wait for a key press, store the value of the key in Vx.
        """
        if self.DEBUG:
            print('Fx0A')

        Vx = (self.opcode & 0x0F00) >> 8

        if self.keypad[0]:
            self.registers[Vx] = 0
        elif self.keypad[1]:
            self.registers[Vx] = 1
        elif self.keypad[2]:
            self.registers[Vx] = 2
        elif self.keypad[3]:
            self.registers[Vx] = 3
        elif self.keypad[4]:
            self.registers[Vx] = 4
        elif self.keypad[5]:
            self.registers[Vx] = 5
        elif self.keypad[6]:
            self.registers[Vx] = 6
        elif self.keypad[7]:
            self.registers[Vx] = 7            
        elif self.keypad[8]:
            self.registers[Vx] = 8
        elif self.keypad[9]:
            self.registers[Vx] = 9
        elif self.keypad[10]:
            self.registers[Vx] = 10
        elif self.keypad[11]:
            self.registers[Vx] = 11
        elif self.keypad[12]:
            self.registers[Vx] = 12
        elif self.keypad[13]:             
            self.registers[Vx] = 13
        elif self.keypad[14]:
            self.registers[Vx] = 14
        elif self.keypad[15]:
            self.registers[Vx] = 15
        else:
            self.pc -= 2

    def op_Fx15(self):
        """
            Set delay timer = Vx.
        """
        if self.DEBUG:
            print('Fx15')

        Vx = (self.opcode & 0x0F00) >> 8

        self.delayTimer = self.registers[Vx]
    
    def op_Fx18(self):
        """
            Set sound timer = Vx.
        """
        if self.DEBUG:
            print('Fx18')

        Vx = (self.opcode & 0x0F00) >> 8

        self.soundTimer = self.registers[Vx]

    def op_Fx1E(self):
        """
            Set I = I + Vx.
        """
        if self.DEBUG:
            print('Fx1E')

        Vx = (self.opcode & 0x0F00) >> 8

        self.index += self.registers[Vx]
    
    def op_Fx29(self):
        """
            Set I = location of sprite for digit Vx.
        """
        if self.DEBUG:
            print('Fx29')

        Vx = (self.opcode & 0x0F00) >> 8
        digit = self.registers[Vx]

        self.index = self.FONTSET_START_ADDRESS + (5 * digit)

    def op_Fx33(self):
        """
            Store BCD representation of Vx in memory locations I, I+1, and I+2.

            The interpreter takes the decimal value of Vx, and places the hundreds digit in memory at location in I,
            the tens digit at location I+1, and the ones digit at location I+2.
        """
        if self.DEBUG:
            print('Fx33')

        Vx = (self.opcode & 0x0F00) >> 8
        value = self.registers[Vx]

        self.memory[self.index + 2] = value % 10
        value /= 10

        self.memory[self.index + 1] = int(value % 10) # doesnt need to be casted to int, 
                                                      # it's just my interpreter that kept bugging me about it.
        value /= 10

        self.memory[self.index] = int(value % 10)

    def op_Fx55(self):
        """
            Store registers V0 through Vx in memory starting at location I.
        """
        if self.DEBUG:
            print('Fx55')

        Vx = (self.opcode & 0x0F00) >> 8

        for i in range(Vx + 1):
            self.memory[self.index + i] = self.registers[i]

    def op_Fx65(self):
        """
            Read registers V0 through Vx from memory starting at location I.
        """
        if self.DEBUG:
            print('Fx65')

        Vx = (self.opcode & 0x0F00) >> 8

        for i in range(Vx + 1):
            self.registers[i] = self.memory[self.index + i]

    def decode_execute(self, op):
        #print(hex(op),hex(op & 0x0FFF),hex((op & 0xF000) >> 12))
        init = (op & 0xF000) >> 12
        rest = op & 0x0FFF
        end  = op & 0x000F
        last_two = op & 0x00FF

        if init == 0x0:
            if rest == 0xe0:
                self.op_00E0()
            elif rest == 0xee:
                self.op_00EE()
        elif init == 0x1:
            self.op_1nnn()
        elif init == 0x2:
            self.op_2nnn()
        elif init == 0x3:
            self.op_3xkk()
        elif init == 0x4:
            self.op_4xkk()
        elif init == 0x5:
            self.op_5xy0()
        elif init == 0x6:
            self.op_6xkk()
        elif init == 0x7:
            self.op_7xkk()
        elif init == 0x8:
            if end == 0x0:
                self.op_8xy0()
            elif end == 0x1:
                self.op_8xy1()
            elif end == 0x2:
                self.op_8xy2()
            elif end == 0x3:
                self.op_8xy3()
            elif end == 0x4:                
                 self.op_8xy4()
            elif end == 0x5:
                self.op_8xy5()
            elif end == 0x6:
                self.op_8xy6()
            elif end == 0x7:
                self.op_8xy7()
            else:
                self.op_8xyE()
        elif init == 0x9:
            self.op_9xy0()
        elif init == 0xA:
            self.op_Annn()
        elif init == 0xB:
            self.op_Bnnn()
        elif init == 0xC:
            self.op_Cxkk()
        elif init == 0xD:
            self.op_Dxyn()
        elif init == 0xE:
            if last_two == 0x9E:
                self.op_Ex9E()
            else:
                self.op_ExA1()
        elif init == 0xF:
            if last_two == 0x07:
                self.op_Fx07()
            elif last_two == 0x0A:
                self.op_Fx0A()
            elif last_two == 0x15:
                self.op_Fx15()
            elif last_two == 0x18:
                self.op_Fx18()
            elif last_two == 0x1E:
                self.op_Fx1E()
            elif last_two == 0x29:
                self.op_Fx29()
            elif last_two == 0x33:
                self.op_Fx33()
            elif last_two == 0x55:
                self.op_Fx55()
            elif last_two == 0x65:
                self.op_Fx65()
        else:
            self.op_NULL()

    def cycle(self):
        self.opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2
        
        #print(hex(self.opcode))
        self.decode_execute(self.opcode)
        print(self.keypad)

        if self.delayTimer > 0:
            self.delayTimer -= 1
        if self.soundTimer > 0:
            self.soundTimer -= 1


def draw(buffer):
    x = 0
    for i in buffer:
        if i == 0:
            print('\033[1;32m█', end = '\033[1;32m█')
        else:
            print('\033[1;31m█', end = '\033[1;31m█')
        x += 1
        if x == 64:
            x = 0
            print('')


#a = Chip8()
#a.load_rom('rom.ch8')
#while True:
#    os.system("clear")
#    a.cycle()
#    draw(a.video)
#    time.sleep(0.02)
