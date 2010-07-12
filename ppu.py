import hardware, cpu

class ppu:

    def __init__(self, nes): 
        self.DEBUG = 1
        self.firstWrite = 0
        #PPU 2000 register indexes
        self.NMIOnVBlank = 0
        self.ppuMasterSlave = 1
        self.spriteSize = 2
        self.backgroundPatternAddress = 3
        self.spritePatternAddress = 4
        self.ppuAddressIncrement = 5
        
        #PPU 2001 register indexes
        self.grayscale = 7
        self.backgroundClipping = 6
        self.spriteClipping = 5
        self.backgroundVisible = 4
        self.spritesVisible = 3
        
        #PPU 2006 register indexes
        self.prevVramAddress = 1
        self.vramAddress = 0
        self.scrollVert = 2
        self.scrollHori = 3
        
            
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
         
        #print nesSystem.ppu.currentScanline, nesSystem.ppu.PPU2000Registers[0]
        #print nesSystem.ppu.PPU2000Registers[0]
        return ((nesSystem.ppu.currentScanline == nesSystem.ppu.ScanlinesofVBlank) and (nesSystem.ppu.PPU2000Registers[0] == 1))
        #return True


        
    def controlRegister1Write(self, nesSystem, registerData): 
        if (registerData & 128) == 128:
            nesSystem.ppu.PPU2000Registers[self.NMIOnVBlank] = 1
        else:
            nesSystem.ppu.PPU2000Registers[self.NMIOnVBlank] = 0
            
        if nesSystem.ppu.PPU2000Registers[self.ppuMasterSlave] == 255:
            if (registerData & 64) == 64:
                nesSystem.ppu.PPU2000Registers[self.ppuMasterSlave] = 0
            else:
                nesSystem.ppu.PPU2000Registers[self.ppuMasterSlave] = 1

        if (registerData & 32) == 32:
            nesSystem.ppu.PPU2000Registers[self.spriteSize] = 16
        else:
            nesSystem.ppu.PPU2000Registers[self.spriteSize] = 8
            
        if (registerData & 16) == 16:
            nesSystem.ppu.PPU2000Registers[self.backgroundPatternAddress] = 4096 #0x1000
        else:
            nesSystem.ppu.PPU2000Registers[self.backgroundPatternAddress] = 0 #0x0000
            
        if (registerData & 8) == 8:
            nesSystem.ppu.PPU2000Registers[self.spritePatternAddress] = 4096 #0x1000
        else:
            nesSystem.ppu.PPU2000Registers[self.spritePatternAddress] = 0 #0x0000
            
        if (registerData & 4) == 4:
            nesSystem.ppu.PPU2000Registers[self.spritePatternAddress] = 32
        else:
            nesSystem.ppu.PPU2000Registers[self.spritePatternAddress] = 1 
            
            
            
            
    def controlRegister2Write(self, nesSystem, registerData):
        if (registerData & 1) == 1:
            nesSystem.ppu.PPU2001Registers[self.grayscale] = 1
        else:
            nesSystem.ppu.PPU2001Registers[self.grayscale] = 0
        
        if (registerData & 2) == 2:
             nesSystem.ppu.PPU2001Registers[self.backgroundClipping] = 1
        else:
             nesSystem.ppu.PPU2001Registers[self.backgroundClipping] = 0
             
        if (registerData & 4) == 4:
             nesSystem.ppu.PPU2001Registers[self.spriteClipping] = 1
        else:
             nesSystem.ppu.PPU2001Registers[self.spriteClipping] = 0
        
        if (registerData & 8) == 8:
             nesSystem.ppu.PPU2001Registers[self.backgroundVisible] = 1
        else:
             nesSystem.ppu.PPU2001Registers[self.backgroundVisible] = 0
             
        if (registerData & 16) == 16:
             nesSystem.ppu.PPU2001Registers[self.spritesVisible] = 1
        else:
             nesSystem.ppu.PPU2001Registers[self.spritesVisible] = 0
        
        ppuColor = (registerData >> 5) #toggling between RGB
          
    def vRamRegister2Write(self, nesSystem, registerData): 
        if self.firstWrite == 1:
            nesSystem.ppu.PPU2006Registers[self.prevVramAddress] = nesSystem.ppu.PPU2006Registers[self.vramAddress]
            nesSystem.ppu.PPU2006Registers[self.vramAddress] = (registerData << 8)
            self.firstWrite = 0
        
        else:
            nesSystem.ppu.PPU2006Registers[self.vramAddress] += registerData
            if (nesSystem.ppu.PPU2006Registers[self.prevVramAddress] == 0) and (nesSystem.ppu.currentScanline < 240):
                if ((nesSystem.ppu.PPU2006Registers[self.vramAddress] >= 8192) and (nesSystem.ppu.PPU2006Registers[self.vramAddress] <= 9216)):
                    nesSystem.ppu.PPU2006Registers[self.scrollHori] = (((nesSystem.ppu.PPU2006Registers[self.vramAddress] - 8192) / 32) * 8 - nesSystem.ppu.currentScanline)
                    
            self.firstWrite = 0
    
    def vRamRegister1Write(self, nesSystem, registerData): 
        if self.firstWrite == 1:
            nesSystem.ppu.PPU2006Registers[self.scrollVert] = registerData
            self.firstWrite = 0
        else:
            nesSystem.ppu.PPU2006Registers[self.scrollHori] = registerData
            if nesSystem.ppu.PPU2006Registers[self.scrollVert] > 239:
                nesSystem.ppu.PPU2006Registers[self.scrollVert] = 0
            
            self.firstWrite = 0

    def ppuDataRegisterWrite(self, nesSystem, registerData):
        #if nesSystem.ppu.PPU2006Registers[self.vramAddress] < 8192: #0x2000
        pass  
            
            
    def statusRegisterRead(self, nesSystem):
        data = 0
        if nesSystem.ppu.currentScanline == 240:
            #nesSystem.ppu.currentScanline = 0
            data |= 128
            
        self.firstWrite = 1
        return data