# IDT5V49EE902 configuration and programming script for MicroPython on Raspberry Pi Pico.
import machine

addr=0b1101010
i2c=machine.I2C()

def read_reg(regaddr):
    i2c.writeto(addr, bytearray([0, regaddr]))
    return i2c.readfrom(addr, 2)[1]

def write_reg(regaddr, val):
    i2c.writeto(addr, bytearray([0, regaddr, val]))

def mod_reg(regaddr, mask, val):
    regval = read_reg(regaddr)
    regval = (regval & ~mask) | (val & mask)
    write_reg(regaddr, regval)

def set_reg_bit(regaddr, bit):
    mod_reg(regaddr, 1<<bit, 1<<bit)

def clear_reg_bit(regaddr, bit):
    mod_reg(regaddr, 1<<bit, 0)

def prog_save():
    i2c.writeto(addr, bytearray([1]))

# xtal trim 12 (3.5pF+31*0.125pF)
mod_reg(0x7, 0x1f, 0x1f)
# use sw ctrl cfg
set_reg_bit(0x0, 0)
# select config 0
mod_reg(0x1, 0x7, 0x0)

# Input clock configuration:
# Use XTAL (bit[0] = 0)
# switch mode manual (bit[2:1] = 0)
mod_reg(0xc0, 0x3, 0)

# Configure color clock output (17.734475 MHz) (output 5)
# set src mux (bit[4:2]) for output 5 to input/reference clock (value 2)
mod_reg(0xcc, 3 << 2, 2 << 2)
# bypass output divider for output 5
write_reg(0xa0, 0xff)


### pll config for 7.875MHz
# pll1
# disable PLL
write_reg(0x28, 0x0)
# set loop bandwidth parameter
# rz = 0xf, ip = 1, cz = 1 --> 0x9f
write_reg(0x24, 0x9f)
# fout = fin * M/D
# --> fin = 17.734475MHz. With M=1127 and D=47, fout = 17.734475 * 1127/47 = 425.25MHz.
# M = 1127. Split over two registers, M[7:0] in 0x30, M[10:8] in 0x34.
write_reg(0x30, 0x67)
write_reg(0x34, 0x4)
# D = 47
write_reg(0x28, 47)
# enable output divider for output 4. 
# Needed divider is 54. PLL frequency is 425.25007MHz --> 425.25MHz/54 = 7.875MHz
# Register value: divider = (q+2)*2 --> q = 25
# Additionally, MSB to set to 1 --> 25 + 128 = 153 = 0x99
write_reg(0x9c, 0x99)
# Configure dot clock output (7.875MHz) (output 4)
# select PLL1 as as source for output 4 (value 5). Split over two registers, two MSBs in 0xcc, LSB in 0xc4
set_reg_bit(0xc4, 7)
mod_reg(0xcc, 0x3, 0x2)

# output configuration:
# - Enable LVTTL (bit[1:0] = 0)
# - Lowest slew rate (bit[5:4] = 0)
mod_reg(0x79, 0x33, 0)
mod_reg(0x7a, 0x33, 0)
# enable output 4 and 5
set_reg_bit(0x3, 4)
set_reg_bit(0x3, 5)

# uncomment for programming to eeprom:
#prog_save()