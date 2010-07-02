import hardware

I_F = (1 << 2)


def SEI(nes):
    print "SEI" 
    nes.cpu.status |= I_F
    
def CLD(nes):
    print "CLD"