import hardware

#getting individual bits shortcuts
I_F = (1 << 2)
N_F = (1 << 7)
Z_F = (1 << 1)


def setN(nesSystem, result):
    if result < 0:
        nesSystem.cpu.status |= N_F
    else:
        nesSystem.cpu.status &= ~N_F
        
def setZ(nesSystem, result):
    if result == 0:
        nesSystem.cpu.status |= Z_F
    else:
        nesSystem.cpu.status &= ~Z_F
        
                
        
        

#0x78. Set interrupt disable status
def SEI(nesSystem, cpu):
    print "SEI" 
    nesSystem.cpu.status |= I_F
   
#0xD8. Clear decimal mode
def CLD(nesSystem, cpu):
    print "CLD"
    
#0xA9. Load accumulator with memory
def LDA(nesSystem, cpu):
    print "LDA"
    cpu.operand = cpu.getNextByte()
    nesSystem.cpu.accumulator = cpu.operand
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    
#0x10. Branch on result plus. 0x10 
def BPL(nesSystem, cpu):
    print "BPL"
    cpu.operand = cpu.getNextByte()
    
    if not (nesSystem.cpu.status & N_F):
        nesSystem.cpu.programCounter += ord(cpu.operand)
        
       
def STA_bbbb(nesSystem, cpu):
    cpu.operand = cpu.getNextWord()
    nesSystem.cpu.cpuMemory[ord(cpu.operand)] = nesSystem.cpu.accumulator
       
