import machine

addr=0b1101010
i2c=machine.I2C()

def read_reg(regaddr):
    i2c.writeto(addr, bytearray([0, regaddr]))
    return i2c.readfrom(addr, 2)[1]

def write_reg(regaddr, val):
    i2c.writeto(addr, bytearray([0, regaddr, val]))

def prog_save():
    i2c.writeto(addr, bytearray([1]))

# xtal trim 12 (3.5pF+12*0.125pF)
write_reg(7, 12)
#use sw ctrl cfg
write_reg(0x0, 1)
# select config 0
write_reg(0x1, 0x0)
#enable output 6 and 3
write_reg(0x3, (1<<6) | (1<<3))
# manual switch
write_reg(0xc0, 84)

# select input clk as output 3
write_reg(0xc4, 2<<4)
# output divider = 1 for out 3
write_reg(0x94, 0xff)


### pll config for 7.875
# pll1
# disable PLL
write_reg(0x28, 0)
# set loop bandwidth parameter
# rz = 0xf, ip = 1, cz = 1 --> 0x9f
write_reg(0x24, 0x9f)
# fout = fin * M/D
# M = 1127
write_reg(0x30, 103)
write_reg(0x34, 4)
# D = 47
write_reg(0x28, 47)
# enable output divider 6 o = 25 + msb
write_reg(0xa8, 0x99)
# select PLL1 as output 6
write_reg(0xcc, 5<<5)
