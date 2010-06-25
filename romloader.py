import hardware

class romLoader:

    nesSystem = 0
    TRAINER_SIZE = 0x200 #512
    PRG_SIZE = 0x4000 #16k
    CHR_SIZE = 0x2000
    MIRRORING_MASK = 1
    SRAM_MASK = 2
    TRAINER_MASK = 4
    FOUR_SCREEN_MASK = 8
    
    def __init__(self, nes): 
        self.nesSystem = nes   
  
    def loadRom(self, romPath):
        try:
            romFile = open(romPath, 'rb')
        except ValueError:
            print "File I/O Error. Check the path of the rom file."
            
        romFile.seek(4) #skip first 4 bytes of crapola
        
        #set prgCount, chrCount and control bytes
        self.nesSystem.rom.prgCount =  romFile.read(1)
        self.nesSystem.rom.chrCount =  romFile.read(1)
        self.nesSystem.rom.controlByte1 =  romFile.read(1)
        self.nesSystem.rom.controlByte2 =  romFile.read(1)
        
        #Shift the lower bits to the rightmost nibble, OR the two BYTEs together to get our mapper number
        self.nesSystem.rom.mapperNumber = (ord(self.nesSystem.rom.controlByte2) & 0xf0) | ((ord(self.nesSystem.rom.controlByte1) & 0xf0) >> 4)
        
        romFile.seek(16)
        
        #get trainer
        if ord(self.nesSystem.rom.controlByte1) & self.TRAINER_MASK:
            self.nesSystem.rom.trainerData = romFile.read(self.TRAINER_SIZE)
            
        #prg rom
        self.nesSystem.rom.prgData = romFile.read(self.PRG_SIZE)
        
        #chr rom
        self.nesSystem.rom.chrData = romFile.read(self.CHR_SIZE)
       
        
nes = hardware.NES()        
r = romLoader(nes)

r.loadRom("Roms/mario.nes")
