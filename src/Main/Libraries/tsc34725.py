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

def detect_color(clear, red, green, blue):
    saturation = min(red, green, blue) / clear
    value = clear / 65535

    if saturation > 0.3:
        if red > green and red > blue:
            return "Rojo"
        elif green > red and green > blue:
            return "Verde"
        elif blue > red and blue > green:
            return "Azul"
    elif value < 0.2:
        return "Negro"
    else:
        return "Blanco"

# Loop infinito para detectar colores continuamente
while True:
    clear, red, green, blue = read_color()
    color = detect_color(clear, red, green, blue)

    print("Color detectado:", color)
    time.sleep(1)  # Esperar 1 segundo antes de la próxima detección
