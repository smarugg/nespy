import hardware
import romloader
import instructions
import ppu

class cpu:

    def __init__(self, nes): 
        self.nesSystem = nes
        self.ppu = ppu.ppu(nes)
        self.operand = 0
        self.DEBUG = 0
        
    def trace(self, currentOpCode, tempCounter, instrName):
        print "PC:", hex(tempCounter), "   Accumulator:", (self.nesSystem.cpu.accumulator), "Status:", self.nesSystem.cpu.status, "\n"
    
    def getNextByte(self):
        #self.nesSystem.cpu.programCounter += 1
        #return self.nesSystem.cpu.cpuMemory[self.nesSystem.cpu.programCounter]
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
                pass 
            elif address < 0x1000:
                pass
            elif address < 0x1800:
                pass
        
        elif address < 0x6000:
            registers = {
                    0x2002 : self.ppu.statusRead,
                  }
            data = registers[address](self.nesSystem)      
        
        elif address < 0x8000:
            pass
        else:
            data = self.readPRG(address)
        
        return data
        
        
    def writeMemory(self, address, data):
        
        if address < 0x800:
            pass
            
        elif address < 0x1000:
            pass
            
        elif address < 0x1800:
            pass
            
        elif address < 0x2000:
            pass
            
        elif address < 0x4000:
            registers = {
                    0x2000 : self.ppu.controlWrite1,
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
        self.nesSystem.cpu.stackP = []
        self.nesSystem.cpu.accumulator = 0
        self.nesSystem.cpu.registerX = 0
        self.nesSystem.cpu.registerY = 0
        self.nesSystem.cpu.status = [0, 0, 0, 0, 0, 0, 0, 0]
     
    #def pushByte(self, byte):
        #writeMemory(address, data)
     
    def pushPC(self):
        instructions.pushStack(self.nesSystem, self.nesSystem.cpu.programCounter)
        
    def pushStatus(self):
        instructions.pushStack(self.nesSystem, self.nesSystem.cpu.status)

    def executeNMI(self):
        self.pushPC()
        self.pushStatus()
        self.nesSystem.cpu.programCounter = self.nesSystem.cpu.cpuMemory[0xFFFA]
        
    def executeOpCode(self):
        #currentOpCode = hex(ord(self.getNextByte()))
        
        print hex(self.nesSystem.cpu.programCounter)
        currentOpCode = hex(self.readMemory(self.nesSystem.cpu.programCounter))
        
        #dict containing the 6502's opcodes. Lowercase, because hex in python is lower
        opCodes = {
                    "0x78" : instructions.SEI,
                    "0xd8" : instructions.CLD,
                    "0xa9" : instructions.LDA_Immediate,
                    "0x10" : instructions.BPL,
                    "0x8d" : instructions.STA_Absolute,
                    "0x20" : instructions.JSR,
                    "0xa2" : instructions.LDX,
                    "0x9a" : instructions.TXS,
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
                    
                    
                  }
        tempCounter = self.nesSystem.cpu.programCounter
        #execute the instruction corresponding with the opcode signature          
        cyclesTaken = opCodes[currentOpCode](self.nesSystem, self)
        
        if self.DEBUG:
            self.trace(currentOpCode, tempCounter, opCodes[currentOpCode].__name__)
            
        return cyclesTaken
       