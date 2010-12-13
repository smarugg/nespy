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
                    "0xa"  : instructions.ASL,
                    "0x2c" : instructions.BIT,
                    "0x78" : instructions.SEI,
                    "0xd8" : instructions.CLD,
                    "0xa9" : instructions.LDA_Immediate,
                    "0xa5" : instructions.LDA_ZeroPage,
                    "0x5"  : instructions.ORA_ZeroPage,
                    "0x9"  : instructions.ORA_Immediate,
                    "0x10" : instructions.BPL,
                    "0x18" : instructions.CLC,
                    "0x8d" : instructions.STA_Absolute,
                    "0x20" : instructions.JSR,
                    "0x2a" : instructions.ROL_Accumulator,
                    "0x38" : instructions.SEC,
                    "0x3d" : instructions.AND_Absolute,
                    "0x40" : instructions.RTI,
                    "0x45" : instructions.EOR_ZeroPage,
                    "0x48" : instructions.PHA,
                    "0x4a" : instructions.LSR_Accumulator,
                    "0x4c" : instructions.JMP,
                    "0x29" : instructions.AND_Immediate,
                    "0xa8" : instructions.TAY,
                    "0xaa" : instructions.TAX,
                    "0xac" : instructions.LDY_Absolute,
                    "0xa2" : instructions.LDX_Immediate,
                    "0xae" : instructions.LDX_Absolute,
                    "0x8a" : instructions.TXA,
                    "0x9a" : instructions.TXS,
                    "0x99" : instructions.STA_AbsoluteY,
                    "0xad" : instructions.LDA_Absolute,
                    "0xa0" : instructions.LDY_Immediate,
                    "0xb1" : instructions.LDA_IndirectY,
                    "0xbd" : instructions.LDA_AbsoluteX,
                    "0xbe" : instructions.LDX_AbsoluteY,
                    "0xb9" : instructions.LDA_AbsoluteY,
                    "0xc9" : instructions.CMP,
                    "0xc6" : instructions.DEC_ZeroPage,
                    "0xb0" : instructions.BCS,
                    "0xca" : instructions.DEX,
                    "0xce" : instructions.DEC_Absolute,
                    "0xd0" : instructions.BNE,
                    "0x6c" : instructions.JMP_Indirect,
                    "0x6d" : instructions.ADC_Absolute,
                    "0x69" : instructions.ADC_Immediate,
                    "0x7e" : instructions.ROR_AbsoluteX,
                    "0x85" : instructions.STA_ZeroPage,
                    "0x86" : instructions.STX_ZeroPage,
                    "0x8c" : instructions.STY_Absolute,
                    "0xe0" : instructions.CPX,
                    "0xe8" : instructions.INX,
                    "0x90" : instructions.BCC,
                    "0x91" : instructions.STA_IndirectY,
                    "0x98" : instructions.TYA,
                    "0x9d" : instructions.STA_AbsoluteX,
                    "0x88" : instructions.DEY,
                    "0xc0" : instructions.CPY,
                    "0xc8" : instructions.INY,
                    "0xee" : instructions.INC,
                    "0xe6" : instructions.INC_ZeroPage,
                    "0x60" : instructions.RTS,
                    "0x65" : instructions.ADC_ZeroPage,
                    "0x68" : instructions.PLA,
                    "0xf0" : instructions.BEQ,
                    "0xf8" : instructions.SED,
                    "0xf9" : instructions.SBC_AbsoluteY,

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
                    0x4016 : self.ppu.donothing,
                    0x4017 : self.ppu.donothing,
                  }
            data = registers[address](self.nesSystem)      
        
        elif address < 0x8000:
            pass
        else:
            data = self.readPRG(address)
        
        return data
    
    def readMemory16(self, address):   
        data1 = 0x00
        data2 = 0x00
        
        if address < 0x2000:
            if address < 0x800:
                data1 = self.nesSystem.cpu.scratch1[address]
                data2 = self.nesSystem.cpu.scratch1[address + 1]
            elif address < 0x1000:
                data1 = self.nesSystem.cpu.scratch1[address - 0x800]
                data2 = self.nesSystem.cpu.scratch1[address - 0x800 + 1]
            elif address < 0x1800:
                data1 = self.nesSystem.cpu.scratch1[address - 0x1000]
                data2 = self.nesSystem.cpu.scratch1[address - 0x1000 + 1]
            else:
                data1 = self.nesSystem.cpu.scratch1[address - 0x1800]
                data2 = self.nesSystem.cpu.scratch1[address - 0x1800 + 1]
        
        elif address < 0x8000:
            pass 

        else:
            data1 = self.readPRG(address)
            data2 = self.readPRG(address + 1)
        data = (data2 << 8) + data1
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
                    0x2003 : self.ppu.spriteAddressRegisterWrite,
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
        for index, x in enumerate(self.nesSystem.rom.prgData):
            self.nesSystem.cpu.cpuMemory[index + 0x8000] = self.nesSystem.rom.prgData[index]
            
        for index, x in enumerate(self.nesSystem.rom.chrData):
            self.nesSystem.ppu.ppuMemory[index] = self.nesSystem.rom.chrData[index]
            
        
        
    def cpuInit(self):

        #PC = byte at 0xFFFD * 256 + byte at 0xFFFC 
        self.nesSystem.cpu.programCounter = (self.nesSystem.cpu.cpuMemory[0xFFFD] * 256) + self.nesSystem.cpu.cpuMemory[0xFFFC]
        self.nesSystem.cpu.stackP = 0
        self.nesSystem.cpu.accumulator = 0
        self.nesSystem.cpu.registerX = 0
        self.nesSystem.cpu.registerY = 0
        self.nesSystem.cpu.status = [0, 0, 0, 0, 0, 0, 0, 0]

     
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
        
    def pullStatus(self):
        statusData = self.pullByte8()
        
        if (statusData & 128) == 128:
            self.nesSystem.cpu.status[instructions.N_F] = 1
        else:
            self.nesSystem.cpu.status[instructions.N_F] = 0
            
        if (statusData & 64) == 64:
            self.nesSystem.cpu.status[instructions.V_F] = 1
        else:
            self.nesSystem.cpu.status[instructions.V_F] = 0
           
        if (statusData & 16) == 16:
            self.nesSystem.cpu.status[instructions.B_F] = 1
        else:
            self.nesSystem.cpu.status[instructions.B_F] = 0

        if (statusData & 8) == 8:
            self.nesSystem.cpu.status[instructions.D_F] = 1
        else:
            self.nesSystem.cpu.status[instructions.D_F] = 0
        
        if (statusData & 4) == 4:
            self.nesSystem.cpu.status[instructions.I_F] = 1
        else:
            self.nesSystem.cpu.status[instructions.I_F] = 0

        if (statusData & 2) == 2:
            self.nesSystem.cpu.status[instructions.Z_F] = 1
        else:
            self.nesSystem.cpu.status[instructions.Z_F] = 0   

        if (statusData & 1) == 1:
            self.nesSystem.cpu.status[instructions.C_F] = 1
        else:
            self.nesSystem.cpu.status[instructions.C_F] = 0

    def pushStatus(self):  
        status = 0
        
        if self.nesSystem.cpu.status[instructions.N_F] == 1:
            status += 128
            
        if self.nesSystem.cpu.status[instructions.V_F] == 1:
            status += 64
            
        if self.nesSystem.cpu.status[instructions.B_F] == 1:
            status += 16
        
        if self.nesSystem.cpu.status[instructions.D_F] == 1:
            status += 8
            
        if self.nesSystem.cpu.status[instructions.I_F] == 1:
            status += 4

        if self.nesSystem.cpu.status[instructions.Z_F] == 1:
            status += 2
            
        self.pushByte8(status)
        

    def executeNMI(self):
        self.pushPC()
        self.pushStatus()
        self.nesSystem.cpu.programCounter = self.nesSystem.cpu.cpuMemory[0xFFFA]
        
    def executeOpCode(self):    
        #print hex(self.nesSystem.cpu.programCounter)#, "RegX", hex(self.nesSystem.cpu.registerX), "RegY", hex(self.nesSystem.cpu.registerY), "StackP", hex(self.nesSystem.cpu.stackP)
        #print self.nesSystem.cpu.accumulator
        currentOpCode = hex(self.readMemory(self.nesSystem.cpu.programCounter))  
        
        tempCounter = self.nesSystem.cpu.programCounter
        #execute the instruction corresponding with the opcode signature          
        cyclesTaken = self.opCodes[currentOpCode](self.nesSystem, self)
        
        # if self.nesSystem.cpu.programCounter == 36395:
           # x = raw_input()
 
        if self.DEBUG:
            self.trace(currentOpCode, tempCounter, self.opCodes[currentOpCode].__name__)
            
        return cyclesTaken
       