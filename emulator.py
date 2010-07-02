import hardware, romloader, cpu

nes = hardware.NES()   
  
r = romloader.romLoader(nes)
r.loadRom("Roms/Mario.nes")
#r.printPrg(20)

c = cpu.cpu(nes)
c.memoryInit()

c.cpuInit()
c.execute()