from time import sleep
from lcd_api import LcdApi

class I2cLcd(LcdApi):
    def __init__(self, i2c, addr, rows, cols):
        super().__init__(rows, cols)
        self.i2c = i2c
        self.addr = addr

        sleep(0.1)

        self.write_cmd(0x33)
        self.write_cmd(0x32)
        self.write_cmd(0x28)
        self.write_cmd(0x0C)
        self.write_cmd(0x06)
        self.clear()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytes([cmd | 0x08]))
        sleep(0.01)

    def clear(self):
        self.write_cmd(0x01)
        sleep(0.01)

    def move_to(self, col, row):
        addr = col + (0x40 * row)
        self.write_cmd(0x80 | addr)

    def putstr(self, string):
        for char in string:
            self.i2c.writeto(self.addr, bytes([ord(char)]))