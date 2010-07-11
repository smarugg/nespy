import hardware, cpu

class ppu:

    def __init__(self, nes): 
        self.DEBUG = 1
        self.NMIOnVBlank = 0
        
     
        
    # def nextScanline(self, nesSystem):
        # if nesSystem.ppu.currentScanline == 240:
            # print "rendering frame"
        # nesSystem.ppu.currentScanline += 1  
        
        # if nesSystem.ppu.currentScanline == 262:
            # print "sdfsdfsdfs"
            # nesSystem.ppu.currentScanline = 0 
        
        # if (nesSystem.ppu.currentScanline == nesSystem.ppu.ScanlinesofVBlank) and (nesSystem.ppu.PPU2000Registers[0]):
            # return True
        # else:
            # return False
            
    def nextScanline(self, nesSystem):
        if nesSystem.ppu.currentScanline < 240:
            #print "Clean up line from before"
            pass
            
        if nesSystem.ppu.currentScanline == 240:
            #print "Rendering frame"
            pass
            
        nesSystem.ppu.currentScanline += 1
        
        if nesSystem.ppu.currentScanline == 262:
            nesSystem.ppu.currentScanline = 0

        if (nesSystem.ppu.currentScanline == nesSystem.ppu.ScanlinesofVBlank) and (nesSystem.ppu.PPU2000Registers[0] == 1):
            return True
        else:
            return False
            
    def controlWrite1(self, nesSystem, data): 
        if (data & 128) == 128:
            nesSystem.ppu.PPU2000Registers[self.NMIOnVBlank] = 1
        else:
            nesSystem.ppu.PPU2000Registers[self.NMIOnVBlank] = 0
      
    def controlWrite2(self, nesSystem, data):
        if (data & 128) == 128:
            nesSystem.ppu.PPU2000Registers[self.NMIOnVBlank] = 1
        else:
            nesSystem.ppu.PPU2000Registers[self.NMIOnVBlank] = 0
        
    def statusRead(self, nesSystem):
        data = 0
        
        
        if nesSystem.ppu.currentScanline == 240:
            #nesSystem.ppu.currentScanline = 0
            data = (data | 128)
        return data