import hardware, romloader, cpu

def setupEmulation(romPath):
    
    nes = hardware.NES()   
    r = romloader.romLoader(nes)
    r.loadRom(romPath)

    c = cpu.cpu(nes)
    c.memoryInit()
    c.cpuInit()
    return c
def runEmulation(nesSystem):
    nesSystem.execute()
