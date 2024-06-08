import smbus
import time

def read_color():
    TCS34725_ADDRESS = 0x29
    TCS34725_ENABLE = 0x00
    TCS34725_ATIME = 0x01
    TCS34725_CONTROL = 0x0F

    bus = smbus.SMBus(1)
    bus.write_byte_data(TCS34725_ADDRESS, TCS34725_ENABLE, 0x01)
    time.sleep(0.1)
    bus.write_byte_data(TCS34725_ADDRESS, TCS34725_ATIME, 0xEB)
    bus.write_byte_data(TCS34725_ADDRESS, TCS34725_CONTROL, 0x03)

    TCS34725_ADDRESS = 0x29
    TCS34725_CDATAL = 0x14
    TCS34725_RDATAL = 0x16
    TCS34725_GDATAL = 0x18
    TCS34725_BDATAL = 0x1A

    bus = smbus.SMBus(1)
    clear = bus.read_word_data(TCS34725_ADDRESS, TCS34725_CDATAL)
    red = bus.read_word_data(TCS34725_ADDRESS, TCS34725_RDATAL)
    green = bus.read_word_data(TCS34725_ADDRESS, TCS34725_GDATAL)
    blue = bus.read_word_data(TCS34725_ADDRESS, TCS34725_BDATAL)

    return red, green, blue, clear

while True:
    r, g, b, c = read_color()
    print(f"R: {r}, G: {g}, B: {b}, C: {c}")
    time.sleep(1)
