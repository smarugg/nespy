import hardware, romloader, cpu

nes = hardware.NES()   
  
r = romloader.romLoader(nes)
r.loadRom("Roms/Mario.nes")
#r.loadRom("Roms/Duck Hunt.nes")

c = cpu.cpu(nes)

c.memoryInit()
c.cpuInit()
while True:
    c.execute()
