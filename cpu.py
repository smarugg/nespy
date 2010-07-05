import hardware
import romloader
import instructions

class cpu:

    def __init__(self, nes): 
        self.nesSystem = nes
        self.operand = 0
        self.DEBUG = 1
        
    def trace(self, currentOpCode, tempCounter, instrName):
        print "PC:", hex(tempCounter), instrName, currentOpCode, "   Accumulator:", hex(ord(str(self.nesSystem.cpu.accumulator))), "Status:", self.nesSystem.cpu.status, "\n"
    
    def getNextByte(self):
        self.nesSystem.cpu.programCounter += 1
        return self.nesSystem.cpu.cpuMemory[self.nesSystem.cpu.programCounter]
        
    def getNextWord(self):
        self.nesSystem.cpu.programCounter += 2

        self.operand = ord(self.operand) | (ord(self.nesSystem.cpu.cpuMemory[self.nesSystem.cpu.programCounter]) << 8)
        return self.nesSystem.cpu.cpuMemory[self.nesSystem.cpu.programCounter]
        

    def memoryInit(self):
        for x in range(len(self.nesSystem.rom.prgData)):
            self.nesSystem.cpu.cpuMemory[x + 0x8000] = self.nesSystem.rom.prgData[x]
        
        # if ord(self.nesSystem.rom.controlByte1) & self.nesSystem.rom.SRAM_MASK:
            # print "SRAM"
        
        # if ord(self.nesSystem.rom.controlByte1) & self.nesSystem.rom.TRAINER_MASK:
            # print "SRAM"
        
    def cpuInit(self):

        #PC = byte at 0xFFFD * 256 + byte at 0xFFFC 
        self.nesSystem.cpu.programCounter = (ord(self.nesSystem.cpu.cpuMemory[0xFFFD]) * 256) + ord(self.nesSystem.cpu.cpuMemory[0xFFFC]) - 1
        self.nesSystem.cpu.stackP = 0xFF
        self.nesSystem.cpu.accumulator = 0
        self.nesSystem.cpu.registerX = 0
        self.nesSystem.cpu.registerY = 0
        self.nesSystem.cpu.status = [0, 0, 0, 0, 0, 0, 0, 0]
        

    def execute(self):
        
        
        currentOpCode = hex(ord(self.getNextByte()))

        
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
                    
                  }
        tempCounter = self.nesSystem.cpu.programCounter
        #print hex(self.nesSystem.cpu.programCounter)
        #execute the instruction corresponding with the opcode signature          
        opCodes[currentOpCode](self.nesSystem, self)
        
        if self.DEBUG:
            self.trace(currentOpCode, tempCounter, opCodes[currentOpCode].__name__)
       