
class Rom:
    prgCount = 0
    chrCount = 0
    controlByte1 = 0
    controlByte2 = 0
    mapperNumber = 0
    trainerData = []
    prgData = []
    chrData = []
    
    def __init__(self):
        pass
    
class CPU:
    programCounter = 0
    stackP = 0
    accumulator = 0
    xIndex = 0
    yIndex = 0
    status = 0
    cpuMemory = [0x10000]
    
    def __init__(self):
        pass
    
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

