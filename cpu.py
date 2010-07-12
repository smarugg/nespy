import hardware
import romloader
import instructions
import ppu
import time

class cpu:

    def __init__(self, nes): 
        self.nesSystem = nes
        self.ppu = ppu.ppu(nes)
        self.operand = 0
        self.DEBUG = 0
        
        #dict containing the 6502's opcodes. Lowercase, because hex in python is lower
        self.opCodes = {
                    "0x2c" : instructions.BIT,
                    "0x78" : instructions.SEI,
                    "0xd8" : instructions.CLD,
                    "0xa9" : instructions.LDA_Immediate,
                    "0x9"  : instructions.ORA_Immediate,
                    "0x10" : instructions.BPL,
                    "0x8d" : instructions.STA_Absolute,
                    "0x20" : instructions.JSR,
                    "0x4c" : instructions.JMP,
                    "0x29" : instructions.AND_Immediate,
                    "0xa2" : instructions.LDX,
                    "0x8a" : instructions.TXA,
                    "0x9a" : instructions.TXS,
                    "0x99" : instructions.STA_AbsoluteY,
                    "0xad" : instructions.LDA_Absolute,
                    "0xa0" : instructions.LDY_Immediate,
                    "0xbd" : instructions.LDA_AbsoluteX,
                    "0xc9" : instructions.CMP,
                    "0xb0" : instructions.BCS,
                    "0xca" : instructions.DEX,
                    "0xd0" : instructions.BNE,
                    "0x85" : instructions.STA_ZeroPage,
                    "0x86" : instructions.STX_ZeroPage,
                    "0xe0" : instructions.CPX,
                    "0x91" : instructions.STA_IndirectY,
                    "0x88" : instructions.DEY,
                    "0xc0" : instructions.CPY,
                    "0xc8" : instructions.INY,
                    "0x60" : instructions.RTS,

                  }
        
    def trace(self, currentOpCode, tempCounter, instrName):
        print "PC:", hex(tempCounter), "   Accumulator:", (self.nesSystem.cpu.accumulator), "Status:", self.nesSystem.cpu.status, "\n"
    
    def getNextByte(self):
        return self.readMemory(self.nesSystem.cpu.programCounter + 1)
    
    def getNextWord(self):
        byte1 = self.nesSystem.cpu.cpuMemory[self.nesSystem.cpu.programCounter+1]
        byte2 = self.nesSystem.cpu.cpuMemory[self.nesSystem.cpu.programCounter+2]
        word = byte2
        word = word << 8
        word += byte1
        return word
        
    
    def readPRG(self, address):
        data = 0xFF
        data = self.nesSystem.cpu.cpuMemory[address]
        return data
        
    def writePRG(self, address, data):
        pass
    
    def readMemory(self, address):   
        data = 0x00
        
        if address < 0x2000:
            if address < 0x800:
                data = self.nesSystem.cpu.scratch1[address]
            elif address < 0x1000:
                pass
            elif address < 0x1800:
                pass
        
        elif address < 0x6000:
            registers = {
                    0x2002 : self.ppu.statusRegisterRead,
                  }
            data = registers[address](self.nesSystem)      
        
        elif address < 0x8000:
            pass
        else:
            data = self.readPRG(address)
        
        return data
        
        
    def writeMemory(self, address, data):
        if address < 0x800:
            self.nesSystem.cpu.scratch1[address] = data;
            
        elif address < 0x1000:
            pass
            
        elif address < 0x1800:
            pass
            
        elif address < 0x2000:
            pass
            
        elif address < 0x4000:
            registers = {
                    0x2000 : self.ppu.controlRegister1Write,
                    0x2001 : self.ppu.controlRegister2Write,
                    0x2005 : self.ppu.vRamRegister1Write,
                    0x2006 : self.ppu.vRamRegister2Write,
                    0x2007 : self.ppu.ppuDataRegisterWrite
                  }
            registers[address](self.nesSystem, data)
            
        elif address < 0x6000:
            pass
        
        elif address < 0x8000:
            pass
        
        else:
            self.writePRG(address, data)
    
    def memoryInit(self):
        for x in range(len(self.nesSystem.rom.prgData)):
            self.nesSystem.cpu.cpuMemory[x + 0x8000] = self.nesSystem.rom.prgData[x]
        
        
    def cpuInit(self):

        #PC = byte at 0xFFFD * 256 + byte at 0xFFFC 
        self.nesSystem.cpu.programCounter = (self.nesSystem.cpu.cpuMemory[0xFFFD] * 256) + self.nesSystem.cpu.cpuMemory[0xFFFC]
        self.nesSystem.cpu.stackP = 0
        self.nesSystem.cpu.accumulator = 0
        self.nesSystem.cpu.registerX = 0
        self.nesSystem.cpu.registerY = 0
        self.nesSystem.cpu.status = [0, 0, 0, 0, 0, 0, 0, 0]
     
    # def pushStack(self, byte):
        # self.nesSystem.cpu.stackP.append(byte)
    
    # def popStack(self):
        # return self.nesSystem.cpu.stackP.pop()
        
    # def topStack(self):
        # return self.nesSystem.cpu.stackP[-1]
     
    def pushByte8(self, byte):  
        self.writeMemory((0x100 + self.nesSystem.cpu.stackP), (byte & 255))
        self.nesSystem.cpu.stackP -= 1

    def pushByte16(self, byte):
        self.pushByte8(byte >> 8)
        self.pushByte8(byte & 255)
        
    def pullByte8(self):
        self.nesSystem.cpu.stackP += 1
        return self.readMemory(0x100 + self.nesSystem.cpu.stackP)
    
    def pullByte16(self):
        byte1 = self.pullByte8()
        byte2 = self.pullByte8()     
        word = byte2
        word = word << 8
        word += byte1
        return word

    # def pushByte(self, byte):
        #self.nesSystem.cpuMemory[(self.nesSystem.cpu.stackP)+0x100] = byte
        # print byte
        # self.nesSystem.cpu.stackP -= 1
        # self.writeMemory((self.nesSystem.cpu.stackP + 0x100), byte)
        # print self.readMemory(self.nesSystem.cpu.stackP + 0x100)
        
        
    # def popByte(self):
       # self.nesSystem.cpuMemory[(self.nesSystem.cpu.stackP)+0x100] = byte
        # self.nesSystem.cpu.stackP += 1
        # return self.readMemory(self.nesSystem.cpu.stackP + 0x101)

    def executeNMI(self):
        self.pushPC()
        self.pushStatus()
        self.nesSystem.cpu.programCounter = self.nesSystem.cpu.cpuMemory[0xFFFA]
        
    def executeOpCode(self):    
        print hex(self.nesSystem.cpu.programCounter)
        #print self.nesSystem.cpu.accumulator
        currentOpCode = hex(self.readMemory(self.nesSystem.cpu.programCounter))  
        tempCounter = self.nesSystem.cpu.programCounter
        #execute the instruction corresponding with the opcode signature          
        cyclesTaken = self.opCodes[currentOpCode](self.nesSystem, self)
        
        # if hex(self.nesSystem.cpu.programCounter) == "0x8e56":
            # x = raw_input()
 
        if self.DEBUG:
            self.trace(currentOpCode, tempCounter, self.opCodes[currentOpCode].__name__)
            
        return cyclesTaken
       