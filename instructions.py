import hardware, time

#getting registers (the list indexes)     
C_F = 0 
Z_F = 1
I_F = 2
D_F = 3
B_F = 4
V_F = 6
N_F = 7

#convert to signed 8-bit - this is magic
def castSigned8Bit(i):
    return(i + 2**7) % 2**8 - 2**7     

#Sign flag: this is set if the result of an operation is
#negative, cleared if positive.
def setN(nesSystem, result):
    if (result & 128) == 128:
        nesSystem.cpu.status[N_F] = 1
    else:
        nesSystem.cpu.status[N_F] = 0

#Zero flag: this is set to 1 when any arithmetic or logical
#operation produces a zero result, and is set to 0 if the result is
#non-zero.        
def setZ(nesSystem, result):
    if result == 0:
        nesSystem.cpu.status[Z_F] = 1
    else:
        nesSystem.cpu.status[Z_F] = 0

#Carry flag:
def setC(nesSystem, item1, item2):
    if item1 >= item2:
        nesSystem.cpu.status[C_F] = 1
    else:
        nesSystem.cpu.status[C_F] = 0

#Overflow flag
def setV(nesSystem, result):
    if (result & 64) == 64:
        nesSystem.cpu.status[V_F] = 1
    else:
        nesSystem.cpu.status[V_F] = 0
        
def AND_Immediate(nesSystem, cpu):
    address = cpu.getNextByte()
    nesSystem.cpu.accumulator = (nesSystem.cpu.accumulator & address)
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 2
    return 2

def AND_Absolute(nesSystem, cpu):
    address = cpu.getNextWord()  
    nesSystem.cpu.accumulator = (nesSystem.cpu.accumulator & cpu.readMemory(address))
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 3
    return 4
    
def ADC_ZeroPage(nesSystem, cpu):
    address = cpu.getNextByte()
    result = nesSystem.cpu.accumulator + cpu.readMemory(address) + nesSystem.cpu.status[C_F]
    #can't use usual methods here, so do it manually
    if result > 255:
        nesSystem.cpu.status[C_F] = 1
        nesSystem.cpu.status[V_F] = 1
    else:
        nesSystem.cpu.status[C_F] = 0
        nesSystem.cpu.status[V_F] = 0
    setN(nesSystem, result)
    setZ(nesSystem, result)
    nesSystem.cpu.accumulator = (result & 255)
    nesSystem.cpu.programCounter += 2
    return 3

def ADC_Absolute(nesSystem, cpu):
    address = cpu.getNextWord()
    result = nesSystem.cpu.accumulator + cpu.readMemory(address) + nesSystem.cpu.status[C_F]
    #can't use usual methods here, so do it manually
    if result > 255:
        nesSystem.cpu.status[C_F] = 1
        nesSystem.cpu.status[V_F] = 1
    else:
        nesSystem.cpu.status[C_F] = 0
        nesSystem.cpu.status[V_F] = 0
    setN(nesSystem, result)
    setZ(nesSystem, result)
    nesSystem.cpu.accumulator = (result & 255)
    nesSystem.cpu.programCounter += 3
    return 4  

def ADC_Immediate(nesSystem, cpu):
    address = cpu.getNextByte()
    result = nesSystem.cpu.accumulator + address + nesSystem.cpu.status[C_F]
    #can't use usual methods here, so do it manually
    if result > 255:
        nesSystem.cpu.status[C_F] = 1
        nesSystem.cpu.status[V_F] = 1
    else:
        nesSystem.cpu.status[C_F] = 0
        nesSystem.cpu.status[V_F] = 0
    setN(nesSystem, result)
    setZ(nesSystem, result)
    nesSystem.cpu.accumulator = (result & 255)
    nesSystem.cpu.programCounter += 2
    return 2     

def ASL(nesSystem, cpu):
    address =  cpu.getNextByte()
    setC(nesSystem, nesSystem.cpu.accumulator, address)
    nesSystem.cpu.accumulator = (nesSystem.cpu.accumulator << 1)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    setN(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 1
    return 2
    
def BCS(nesSystem, cpu):
    address = cpu.getNextByte()
    s8Address = castSigned8Bit(address)
    tickcount = 0
    if nesSystem.cpu.status[C_F] == 1:
        nesSystem.cpu.programCounter += 2
        if ((nesSystem.cpu.programCounter & 0xFF00) != ((nesSystem.cpu.programCounter + s8Address + 2) & 0xFF00)):
            tickcount +=1
        nesSystem.cpu.programCounter = nesSystem.cpu.programCounter + s8Address
        tickcount +=1
    
    else:
        nesSystem.cpu.programCounter += 2
    tickcount +=2 
    return tickcount
    
def BCC(nesSystem, cpu):
    address = cpu.getNextByte()
    s8Address = castSigned8Bit(address)
    tickcount = 0
    if nesSystem.cpu.status[C_F] == 0:
        nesSystem.cpu.programCounter += 2
        if ((nesSystem.cpu.programCounter & 0xFF00) != ((nesSystem.cpu.programCounter + s8Address + 2) & 0xFF00)):
            tickcount +=1
        nesSystem.cpu.programCounter = nesSystem.cpu.programCounter + s8Address
        tickcount +=1
    
    else:
        nesSystem.cpu.programCounter += 2
    tickcount +=2 
    return tickcount    

#0xf0. Branch if equal (zero flag set)
def BEQ(nesSystem, cpu):
    address = cpu.getNextByte()
    s8Address = castSigned8Bit(address)
    tickcount = 0
    if nesSystem.cpu.status[Z_F] == 1:
        nesSystem.cpu.programCounter += 2
        if ((nesSystem.cpu.programCounter & 0xFF00) != ((nesSystem.cpu.programCounter + s8Address +2) & 0xFF00)):
            tickcount +=1
        
        nesSystem.cpu.programCounter = nesSystem.cpu.programCounter + s8Address
        tickcount +=1
    
    else:
        nesSystem.cpu.programCounter += 2
    tickcount +=2 
    return tickcount    

def BIT(nesSystem, cpu):
    address = cpu.getNextWord()
    result = cpu.readMemory(address)
    setZ(nesSystem, (nesSystem.cpu.accumulator & result))
    setN(nesSystem, result)
    setV(nesSystem, result)
    nesSystem.cpu.programCounter += 3
    return 4      
    
def BNE(nesSystem, cpu):
    address = cpu.getNextByte()
    s8Address = castSigned8Bit(address)
    
    tickcount = 0
    if nesSystem.cpu.status[Z_F] == 0:
        nesSystem.cpu.programCounter += 2
        if ((nesSystem.cpu.programCounter & 0xFF00) != ((nesSystem.cpu.programCounter + s8Address + 2) & 0xFF00)):
            tickcount +=1
        nesSystem.cpu.programCounter = nesSystem.cpu.programCounter + s8Address
        tickcount +=1
    else:
        nesSystem.cpu.programCounter += 2
    tickcount +=2 
    return tickcount  

#0x10. Branch on result plus. Jump back the RELATIVE number of bytes. 
#If the operand was FB, then we jump back FB - FF+1 number of bytes (-5) 
def BPL(nesSystem, cpu):
    address = cpu.getNextByte()
    s8Address = castSigned8Bit(address)
    tickcount = 0
    if nesSystem.cpu.status[N_F] == 0:
        nesSystem.cpu.programCounter += 2
        #if (nesSystem.cpu.programCounter & 0xFF00) != (nesSystem.cpu.programCounter + (address - (0xFF + 1))):
        if ((nesSystem.cpu.programCounter & 0xFF00) != ((nesSystem.cpu.programCounter + s8Address +2) & 0xFF00)):
            tickcount +=1
        
        nesSystem.cpu.programCounter = nesSystem.cpu.programCounter + s8Address
        tickcount +=1
    
    else:
        nesSystem.cpu.programCounter += 2
    tickcount +=2 
    return tickcount       
 
#0xD8. Clear decimal mode
def CLD(nesSystem, cpu):
    nesSystem.cpu.programCounter += 1
    return 2
    
def CLC(nesSystem, cpu):
    nesSystem.cpu.status[C_F] = 0
    nesSystem.cpu.programCounter += 1
    return 2

def CMP(nesSystem, cpu):
    address = cpu.getNextByte()
    setC(nesSystem, nesSystem.cpu.accumulator, address)
    setZ(nesSystem, nesSystem.cpu.accumulator - address)
    setN(nesSystem, nesSystem.cpu.accumulator - address)
    nesSystem.cpu.programCounter += 2
    return 2
    
def CPX(nesSystem, cpu):
    address = cpu.getNextByte()
    setC(nesSystem, nesSystem.cpu.registerX, address)
    setZ(nesSystem, nesSystem.cpu.registerX)
    setN(nesSystem, nesSystem.cpu.registerX)
    nesSystem.cpu.programCounter += 2
    return 2

def CPY(nesSystem, cpu):
    address = cpu.getNextByte()
    setC(nesSystem, nesSystem.cpu.registerY, address)
    setZ(nesSystem, nesSystem.cpu.registerY)
    setN(nesSystem, nesSystem.cpu.registerY)
    nesSystem.cpu.programCounter += 2
    return 2    
  
def DEC_Absolute(nesSystem, cpu):
    address = cpu.getNextWord()
    result = cpu.readMemory(address)
    cpu.writeMemory(address, result -1)    
    setN(nesSystem, result -1)
    setZ(nesSystem, result -1)
    nesSystem.cpu.programCounter += 3
    return 6
      
def DEC_ZeroPage(nesSystem, cpu):
    address = cpu.getNextByte()
    result = cpu.readMemory(address)
    cpu.writeMemory(address, result -1)  
    cpu.writeMemory(address, result -1)    
    setN(nesSystem, result -1)
    setZ(nesSystem, result -1)
    nesSystem.cpu.programCounter += 2
    return 5  
  
def DEX(nesSystem, cpu):
    nesSystem.cpu.registerX -= 1
    if nesSystem.cpu.registerX < 0:
        nesSystem.cpu.registerX = 255
        
    setN(nesSystem, nesSystem.cpu.registerX)
    setZ(nesSystem, nesSystem.cpu.registerX)
    nesSystem.cpu.programCounter += 1
    return 2
    
def DEY(nesSystem, cpu):
    if nesSystem.cpu.registerY > 0:
        nesSystem.cpu.registerY -= 1
    else:
        nesSystem.cpu.registerY = 255
        
    setN(nesSystem, nesSystem.cpu.registerY)
    setZ(nesSystem, nesSystem.cpu.registerY)
    nesSystem.cpu.programCounter += 1
    return 2    

def EOR_ZeroPage(nesSystem, cpu):
    address = cpu.readMemory(cpu.getNextByte())
    nesSystem.cpu.accumulator = (nesSystem.cpu.accumulator ^ address)
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 2
    return 3    
    
def INY(nesSystem, cpu):
    if nesSystem.cpu.registerY < 255:
        nesSystem.cpu.registerY += 1
    else:
        nesSystem.cpu.registerY = 0
        
    setN(nesSystem, nesSystem.cpu.registerY)
    setZ(nesSystem, nesSystem.cpu.registerY)
    nesSystem.cpu.programCounter += 1
    return 2 

def INX(nesSystem, cpu):
    if nesSystem.cpu.registerX < 255:
        nesSystem.cpu.registerX += 1
    else:
        nesSystem.cpu.registerX = 0
        
    setN(nesSystem, nesSystem.cpu.registerX)
    setZ(nesSystem, nesSystem.cpu.registerX)
    nesSystem.cpu.programCounter += 1
    return 2 

def INC(nesSystem, cpu):
    address = cpu.getNextWord()
    memory = cpu.readMemory(address)
    memory += 1
    setN(nesSystem, memory)
    setZ(nesSystem, memory)
    cpu.writeMemory(address, memory)
    nesSystem.cpu.programCounter += 3
    
    return 6      
    
def INC_ZeroPage(nesSystem, cpu):
    address = cpu.getNextByte()
    result = cpu.readMemory(address)
    cpu.writeMemory(address, result + 1)    
    setN(nesSystem, result + 1)
    setZ(nesSystem, result + 1)
    nesSystem.cpu.programCounter += 2
    return 5 
  
def JMP(nesSystem, cpu):
    address = cpu.getNextWord()
    nesSystem.cpu.programCounter = address
    return 3
    
def JMP_Indirect(nesSystem, cpu):
    address = cpu.getNextWord()
    nesSystem.cpu.programCounter = cpu.readMemory16(address)
    return 5
  
def JSR(nesSystem, cpu):
    address = cpu.getNextWord()
    cpu.pushByte16(nesSystem.cpu.programCounter + 2)
    nesSystem.cpu.programCounter = address
    return 6

#0xAD.Loads a byte of memory into the accumulator setting the zero and negative flags as appropriate.
def LDA_Absolute(nesSystem, cpu):
    address = cpu.getNextWord()
    nesSystem.cpu.accumulator = cpu.readMemory(address)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    setN(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 3
    return 4
    
def LDA_AbsoluteX(nesSystem, cpu):
    address = cpu.getNextWord()
    nesSystem.cpu.accumulator = cpu.readMemory(address + nesSystem.cpu.registerX)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    setN(nesSystem, nesSystem.cpu.accumulator) 
    nesSystem.cpu.programCounter += 3
    return 4
    
def LDA_AbsoluteY(nesSystem, cpu):
    address = cpu.getNextWord()
    nesSystem.cpu.accumulator = cpu.readMemory(address + nesSystem.cpu.registerY)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    setN(nesSystem, nesSystem.cpu.accumulator) 
    nesSystem.cpu.programCounter += 3
    return 4  

#0xA9. Load accumulator with memory IMMEDIATE
def LDA_Immediate(nesSystem, cpu):
    cpu.operand = cpu.getNextByte()
    nesSystem.cpu.accumulator = cpu.operand
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 2
    return 2

def LDA_IndirectY(nesSystem, cpu):
    address = cpu.getNextByte()
   # print address, cpu.readMemory16(address)
    nesSystem.cpu.accumulator = cpu.readMemory(cpu.readMemory16(address) + nesSystem.cpu.registerY)
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 2
    return 5    
  
def LDA_ZeroPage(nesSystem, cpu):
    address = cpu.getNextByte()
    nesSystem.cpu.accumulator = cpu.readMemory(address)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    setN(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 2
    return 3
  
#0xA2. load register X with next byte
def LDX_Immediate(nesSystem, cpu):
    address = cpu.getNextByte()
    nesSystem.cpu.registerX =  address
    setN(nesSystem, nesSystem.cpu.registerX)
    setZ(nesSystem, nesSystem.cpu.registerX)
    nesSystem.cpu.programCounter += 2
    return 2

def LDX_Absolute(nesSystem, cpu):
    address = cpu.getNextWord()
    nesSystem.cpu.registerX = cpu.readMemory(address)
    setZ(nesSystem, nesSystem.cpu.registerX)
    setN(nesSystem, nesSystem.cpu.registerX)
    nesSystem.cpu.programCounter += 3
    return 4
    
def LDX_AbsoluteY(nesSystem, cpu):
    address = cpu.getNextWord()
    nesSystem.cpu.registerX = cpu.readMemory(address) + nesSystem.cpu.registerY
    setZ(nesSystem, nesSystem.cpu.registerX)
    setN(nesSystem, nesSystem.cpu.registerX)
    nesSystem.cpu.programCounter += 3
    return 4
    
def LDY_Absolute(nesSystem, cpu):
    address = cpu.getNextWord()
    nesSystem.cpu.registerY = cpu.readMemory(address)
    setZ(nesSystem, nesSystem.cpu.registerY)
    setN(nesSystem, nesSystem.cpu.registerY)
    nesSystem.cpu.programCounter += 3
    return 4
 
def LDY_Immediate(nesSystem, cpu):
    address = cpu.getNextByte()
    nesSystem.cpu.registerY = address
    setZ(nesSystem, nesSystem.cpu.registerY)
    setN(nesSystem, nesSystem.cpu.registerY)
    nesSystem.cpu.programCounter += 2
    return 2

def LSR_Accumulator(nesSystem, cpu):
    address =  cpu.getNextByte()
    setC(nesSystem, nesSystem.cpu.accumulator, address)
    nesSystem.cpu.accumulator = (nesSystem.cpu.accumulator >> 1)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    setN(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 1
    return 2
    
def ORA_Immediate(nesSystem, cpu):
    address = cpu.getNextByte()
    nesSystem.cpu.accumulator = (nesSystem.cpu.accumulator | address)
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 2
    return 2

def ORA_ZeroPage(nesSystem, cpu):
    address = cpu.readMemory(cpu.getNextByte())
    nesSystem.cpu.accumulator = (nesSystem.cpu.accumulator | address)
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 2
    return 3

def PHA(nesSystem, cpu):
    cpu.pushByte8(nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 1
    return 2

def PLA(nesSystem, cpu):
    nesSystem.cpu.accumulator = cpu.pullByte8()
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 1
    return 4

def ROL_Accumulator(nesSystem, cpu):
    if (nesSystem.cpu.accumulator & 128) == 128:
        newCarry = 1
    else:
        newCarry = 0 
        
    nesSystem.cpu.accumulator = (nesSystem.cpu.accumulator << 1)
    nesSystem.cpu.accumulator = (nesSystem.cpu.accumulator | nesSystem.cpu.status[C_F])
    
    nesSystem.cpu.status[C_F] = newCarry
    
    setZ(nesSystem, nesSystem.cpu.accumulator)
    setN(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 1
    return 2
  
def ROR_AbsoluteX(nesSystem, cpu):
    address = cpu.getNextWord()
    data = cpu.readMemory(address) + nesSystem.cpu.registerX
    
    if (data & 1) == 1:
        newCarry = 1
    else:
        newCarry = 0 
        
        
    data = (data >> 1)
    
    if (nesSystem.cpu.status[C_F] == 1):
        data = (data | 128)
  
    nesSystem.cpu.status[C_F] = newCarry
    
    setZ(nesSystem, data)
    setN(nesSystem, data)
    cpu.writeMemory(address + nesSystem.cpu.registerX, data)
    
    nesSystem.cpu.programCounter += 3
    return 7

def RTI(nesSystem, cpu):
    cpu.pullStatus()
    nesSystem.cpu.programCounter = cpu.pullByte16()
    return 6  
  
def RTS(nesSystem, cpu):
    address = cpu.pullByte16()
    nesSystem.cpu.programCounter = address + 1
    return 6

def SBC_AbsoluteY(nesSystem, cpu):
    address = cpu.getNextWord()
    #cpu.readMemory16(address + nesSystem.cpu.registerY, nesSystem.cpu.accumulator)
    result = nesSystem.cpu.accumulator - cpu.readMemory(address + nesSystem.cpu.registerY)
    if nesSystem.cpu.status[C_F] == 0:
        result -= 1
    if result > 255:
        nesSystem.cpu.status[C_F] = 0
        nesSystem.cpu.status[V_F] = 1
    else:
        nesSystem.cpu.status[C_F] = 1
        nesSystem.cpu.status[V_F] = 0
    
    setZ(nesSystem, nesSystem.cpu.accumulator)
    setN(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.accumulator = (result & 255)
    nesSystem.cpu.programCounter += 3
    return 4

def SEC(nesSystem, cpu):
    nesSystem.cpu.status[C_F] = 1
    nesSystem.cpu.programCounter += 1
    return 2

def SED(nesSystem, cpu):
    nesSystem.cpu.status[D_F] = 1
    nesSystem.cpu.programCounter += 1
    return 2    

#0x78. Set interrupt disable status
def SEI(nesSystem, cpu):
    nesSystem.cpu.status[I_F] = 1
    nesSystem.cpu.programCounter += 1
    return 2
    
#0x8D. Store the byte in the accumulator into memory     
def STA_Absolute(nesSystem, cpu):
    address = cpu.getNextWord()
    cpu.writeMemory(address, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 3
    return 4

def STA_AbsoluteX(nesSystem, cpu):
    address = cpu.getNextWord()
    cpu.writeMemory(address + nesSystem.cpu.registerX, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 3
    return 5

def STA_AbsoluteY(nesSystem, cpu):
    address = cpu.getNextWord()
    cpu.writeMemory(address + nesSystem.cpu.registerY, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 3
    return 5
 
def STA_IndirectY(nesSystem, cpu):
    address = cpu.getNextByte()
    cpu.writeMemory(cpu.readMemory(address) + nesSystem.cpu.registerY, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 2
    return 6
    
def STA_ZeroPage(nesSystem, cpu):
    address = cpu.getNextByte()
    cpu.writeMemory(address, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 2
    return 3

def STX_ZeroPage(nesSystem, cpu):
    address = cpu.getNextByte()
    cpu.writeMemory(address, nesSystem.cpu.registerX)
    nesSystem.cpu.programCounter += 2
    return 3
    
def STY_Absolute(nesSystem, cpu):
    address = cpu.getNextWord()
    cpu.writeMemory(address, nesSystem.cpu.registerY)
    nesSystem.cpu.programCounter += 3
    return 4

def TAX(nesSystem, cpu):
    nesSystem.cpu.registerX = nesSystem.cpu.accumulator
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 1
    return 2
    
def TAY(nesSystem, cpu):
    nesSystem.cpu.registerY = nesSystem.cpu.accumulator
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 1
    return 2
    
def TXA(nesSystem, cpu):
    nesSystem.cpu.accumulator = nesSystem.cpu.registerX
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 1
    return 2
    
def TXS(nesSystem, cpu):
    nesSystem.cpu.stackP = nesSystem.cpu.registerX
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 1
    return 2

def TYA(nesSystem, cpu):
    nesSystem.cpu.accumulator = nesSystem.cpu.registerY
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    nesSystem.cpu.programCounter += 1
    return 2    
    
def toggleVblank(nesSystem, cpu):
    nesSystem.cpu.cpuMemory[0x2002] = 128
    