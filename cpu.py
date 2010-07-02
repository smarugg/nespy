import hardware
import romloader
import instructions

class cpu:

    def __init__(self, nes): 
        self.nesSystem = nes
    
    def getNextByte(self):
        return self.nesSystem.cpu.cpuMemory[self.nesSystem.cpu.programCounter + 1]
        
    def getNextWord(self):
        return self.nesSystem.cpu.cpuMemory[self.nesSystem.cpu.programCounter + 1]

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
        self.nesSystem.cpu.xIndex = 0
        self.nesSystem.cpu.yIndex = 0
        self.nesSystem.cpu.status = 0
        
    def execute(self):
        
        currentOpCode = hex(ord(self.getNextByte()))
        
        #dict of the 6502's opcodes
        opCodes = {
                    "0x78" : instructions.SEI,
                    "0xD8" : instructions.CLD,
                  }
        #execute the instruction corresponding with the opcode signature          
        opCodes[currentOpCode](self.nesSystem)
        