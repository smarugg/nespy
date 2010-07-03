
class Rom:
    prgCount = 0
    chrCount = 0
    controlByte1 = 0
    controlByte2 = 0
    mapperNumber = 0
    trainerData = []
    prgData = []
    chrData = []
    
    TRAINER_SIZE = 0x200 #512
    PRG_SIZE = 0x4000 #16k
    CHR_SIZE = 0x2000
    MIRRORING_MASK = 1
    SRAM_MASK = 2
    TRAINER_MASK = 4
    FOUR_SCREEN_MASK = 8
    
    
    def __init__(self):
        pass
    
class CPU:
    programCounter = 0
    stackP = 0
    accumulator = 0
    registerX = 0
    registerY = 0
    status = 0
    cpuMemory = [0x10000]
    
    def __init__(self):   
        #fill the memory with nulls - limitation of python (can't assign to indexes that don't exist)
        for x in range(0x0, 0x10000):
            self.cpuMemory.append(0) 
    
class PPU:
    ppuMemory = [0x4000]
    
    def __init__(self):
        pass
    
class NES:
    rom = Rom()
    cpu = CPU()
    ppu = PPU()
    
    def __init__(self):
        pass

