import smbus2
import time

def read_color():
    TCS34725_ADDRESS = 0x29
    TCS34725_CDATAL = 0x14
    TCS34725_RDATAL = 0x16
    TCS34725_GDATAL = 0x18
    TCS34725_BDATAL = 0x1A

    bus = smbus2.SMBus(1)
    clear = bus.read_word_data(TCS34725_ADDRESS, TCS34725_CDATAL)
    red = bus.read_word_data(TCS34725_ADDRESS, TCS34725_RDATAL)
    green = bus.read_word_data(TCS34725_ADDRESS, TCS34725_GDATAL)
    blue = bus.read_word_data(TCS34725_ADDRESS, TCS34725_BDATAL)

    return clear, red, green, blue

# Ejemplo de uso
if __name__ == "__main__":
    c, r, g, b = read_color()
    print(f"Rojo: {r}, Verde: {g}, Azul: {b}, Claro: {c}")
