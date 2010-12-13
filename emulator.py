import hardware, romloader, cpu, ppu

class emulator:
    def __init__(self): 
            self.nes = 0
            self.r = 0
            self.c = 0
            self.paused = False
            
            
    def setupEmulation(self, romPath):
        
        self.nes = hardware.NES()   
        self.r = romloader.romLoader(self.nes)
        self.r.loadRom(romPath)

        self.c = cpu.cpu(self.nes)
        self.c.memoryInit()
        self.c.cpuInit()
        
        
        
    def runEmulation(self):
        while True:
            while not self.paused:
                
                x.nes.currentTickCount += x.c.executeOpCode()
                #
                x.nes.totalCycles += x.nes.currentTickCount      
                if x.nes.currentTickCount >= x.nes.cycles_per_scanline:
                    if x.c.ppu.nextScanline(self.nes):
                        #print "Rendering frame", hex(x.c.programCounter)
                        #print hex(x.nes.cpu.programCounter)
                        x.c.pushByte16(x.nes.cpu.programCounter )
                        x.c.pushStatus()
                        x.nes.cpu.programCounter = ((x.c.readMemory(65530+1) << 8) + x.c.readMemory(65530))
                        #print hex(x.nes.cpu.programCounter)
                       
                        
                    x.nes.currentTickCount -= x.nes.cycles_per_scanline      
x = emulator()        
x.setupEmulation("Roms/mario.nes")
x.runEmulation()
