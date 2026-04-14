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

# Use XTAL as input
# Change value to 0 to use clk_in as input
write_reg(0x5, 4)
# xtal trim 12 (3.5pF+12*0.125pF)
write_reg(0x7, 12)
# use sw ctrl cfg
write_reg(0x0, 1)
# select config 0
write_reg(0x1, 0x0)
# enable output 4 and 5
write_reg(0x3, (1<<4) | (1<<5))
# manual switch
write_reg(0xc0, 84)

# select input clk as output 5
write_reg(0xcc, 2<<2)
# bypass output divider for output 5
write_reg(0xa0, 0xff)


### pll config for 7.875MHz
# pll1
# disable PLL
write_reg(0x28, 0)
# set loop bandwidth parameter
# rz = 0xf, ip = 1, cz = 1 --> 0x9f
write_reg(0x24, 0x9f)
# fout = fin * M/D
# --> fin = 17.734475MHz. With M=1127 and D=47, fout = 17.734475 * 1127/47 = 425.25MHz.
# M = 1127
write_reg(0x30, 103)
write_reg(0x34, 4)
# D = 47
write_reg(0x28, 47)
# enable output divider for output 4. 
# Needed divider is 54. PLL frequency is 425.25007MHz --> 425.25MHz/54 = 7.875MHz
# Register value: divider = (q+2)*2 --> q = 25
# Additionally, MSB to set to 1 --> 25 + 128 = 153 = 0x99
write_reg(0x9c, 0x99)
# select PLL1 as output 4 (value 5). Split over two registers, two MSBs in 0xcc, LSB in 0xc4
write_reg(0xc4, 1<<7)
write_reg(0xcc, 2)

# uncomment for programming to eeprom:
#prog_save()