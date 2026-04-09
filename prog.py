import machine

addr=0b1101010
i2c=machine.I2C()

def read_reg(regaddr):
    i2c.writeto(addr, bytearray([0, regaddr]))
    return i2c.readfrom(addr, 2)[1]

def write_reg(regaddr, val):
    i2c.writeto(addr, bytearray([0, regaddr, val]))
