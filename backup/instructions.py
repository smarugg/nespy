import hardware

#getting individual bits shortcuts
I_F = (1 << 2)
N_F = (1 << 7)
Z_F = (1 << 1)


def setN(nesSystem, result):
    if ord(result) < 0:
        nesSystem.cpu.status |= N_F
    else:
        nesSystem.cpu.status &= (~N_F)
        
def setZ(nesSystem, result):
    if ord(result) == 0:
        nesSystem.cpu.status |= Z_F
    else:
        nesSystem.cpu.status &= (~Z_F)


def pushStack(nesSystem, byte):
    nesSystem.cpu.cpuMemory[nesSystem.cpu.stackP - 1 + 0x100] = byte
    
def popStack(nesSystem):
    return nesSystem.cpu.cpuMemory[nesSystem.cpu.stackP + 1 + 0x101]        
        
#0x78. Set interrupt disable status
def SEI(nesSystem, cpu):
    nesSystem.cpu.status |= I_F
   
#0xD8. Clear decimal mode
def CLD(nesSystem, cpu):
    pass
    
#0xA9. Load accumulator with memory IMMEDIATE
def LDA_Immediate(nesSystem, cpu):
    cpu.operand = cpu.getNextByte()
    nesSystem.cpu.accumulator = cpu.operand
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    
#0x10. Branch on result plus. 0x10 
def BPL(nesSystem, cpu):
    cpu.operand = cpu.getNextByte()
    if not nesSystem.cpu.status & N_F :
        print hex(nesSystem.cpu.programCounter + ord(cpu.operand))
        print "hello"
        
#0x8D. Store the byte in the accumulator into memory     
def STA_Absolute(nesSystem, cpu):
    cpu.operand = cpu.getNextWord()
    nesSystem.cpu.cpuMemory[ord(cpu.operand)] = nesSystem.cpu.accumulator
       
def JSR(nesSystem, cpu):
    pass
 
#0xA2. load register X with next byte
def LDX(nesSystem, cpu):
    cpu.operand = cpu.getNextByte()
    nesSystem.cpu.registerX =  cpu.operand
    setN(nesSystem, nesSystem.cpu.registerX)
    setZ(nesSystem, nesSystem.cpu.registerX)
    
#0x9A. Transfers the byte in X Register into the Stack Pointer. Not many roms use this
def TXS(nesSystem, cpu):
    #nesSystem.cpu.stackP = nesSystem.cpu.registerX
    pushStack(nesSystem, nesSystem.cpu.registerX)
    
    
    
#0xAD. Transfers the byte in X Register into the Stack Pointer. Not many roms use this
def LDA_Absolute(nesSystem, cpu):
    cpu.operand = cpu.getNextWord()
    nesSystem.cpu.accumulator = nesSystem.cpu.cpuMemory[ord(cpu.operand)]
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    
    
    #nesSystem.cpu.stackP = nesSystem.cpu.registerX
    