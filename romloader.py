import hardware

class romLoader:

    nesSystem = 0
    
    
    def __init__(self, nes): 
        self.nesSystem = nes   
  
    def loadRom(self, romPath):
        try:
            romFile = open(romPath, 'rb')
        except ValueError:
            print "File I/O Error. Check the path of the rom file."
            
        romFile.seek(4) #skip first 4 bytes of crapola (the NES> bit)
        
        #set prgCount, chrCount and control bytes
        self.nesSystem.rom.prgCount =  ord(romFile.read(1)) #number of 16kb rom banks
        self.nesSystem.rom.chrCount =  ord(romFile.read(1)) #number of 8kb vrom banks
        self.nesSystem.rom.controlByte1 = romFile.read(1)
        self.nesSystem.rom.controlByte2 = romFile.read(1)
        
        #Shift the lower bits to the rightmost nibble, OR the two BYTEs together to get our mapper number
        #print self.nesSystem.rom.controlByte1
        self.nesSystem.rom.mapperNumber = (ord(self.nesSystem.rom.controlByte2) & 0xf0) | ((ord(self.nesSystem.rom.controlByte1) & 0xf0) >> 4)
        
        romFile.seek(16)
        
        #get trainer
        if ord(self.nesSystem.rom.controlByte1) & self.nesSystem.rom.TRAINER_MASK:
            self.nesSystem.rom.trainerData = romFile.read(self.nesSystem.rom.TRAINER_SIZE)
            
        #prg rom
        #read prg count * prg size (different roms have different sized banks)
        self.nesSystem.rom.prgData = romFile.read(self.nesSystem.rom.PRG_SIZE * self.nesSystem.rom.prgCount)
        
        #chr rom
        self.nesSystem.rom.chrData = romFile.read(self.nesSystem.rom.CHR_SIZE * self.nesSystem.rom.chrCount)
        
        print romPath, " ......LOADED"
        print "Mapper Number: ", self.nesSystem.rom.mapperNumber
        print "PRG Count: ", self.nesSystem.rom.prgCount
        print "CHR Count: ", self.nesSystem.rom.chrCount
        print "ControlByte 1: ", ord(self.nesSystem.rom.controlByte1)
        print "ControlByte 2: ", ord(self.nesSystem.rom.controlByte2)
        print "Size of PRG Data: ", len(self.nesSystem.rom.prgData)
        print "Size of CHR Data: ", len(self.nesSystem.rom.chrData)

    def printPrg(self, count):
        for x in range(count):
           print hex(ord(self.nesSystem.rom.prgData[x]))
           
    def printChr(self, count):
        for x in range(count):
           print hex(ord(self.nesSystem.rom.chrData[x]))