import smbus2
import time

# Dirección del sensor TCS34725
TCS34725_ADDR = 0x29

# Registro de control
TCS34725_ENABLE = 0x00
TCS34725_ATIME = 0x01
TCS34725_GAIN = 0x0F
TCS34725_ID = 0x12
TCS34725_CDATAL = 0x14
TCS34725_CDATAH = 0x15
TCS34725_RDATAL = 0x16
TCS34725_RDATAH = 0x17
TCS34725_GDATAL = 0x18
TCS34725_GDATAH = 0x19
TCS34725_BDATAL = 0x1A
TCS34725_BDATAH = 0x1B

# Configuración del bus I2C
bus = smbus2.SMBus(1)

def tcs34725_init():
    # Encender el sensor
    bus.write_byte_data(TCS34725_ADDR, TCS34725_ENABLE, 0x01)
    
    # Configurar el tiempo de integración (ATIME)
    bus.write_byte_data(TCS34725_ADDR, TCS34725_ATIME, 0xEB) # 600ms
    
    # Configurar el rango de ganancia (GAIN)
    bus.write_byte_data(TCS34725_ADDR, TCS34725_GAIN, 0x01) # 1x
    
    time.sleep(0.5) # Esperar para que se estabilice el sensor

def read_color():
    # Leer datos de color
    data = bus.read_i2c_block_data(TCS34725_ADDR, TCS34725_CDATAL | 0x80, 8)
    
    # Convertir datos a valores RGB
    red = data[1] << 8 | data[0]
    green = data[3] << 8 | data[2]
    blue = data[5] << 8 | data[4]

    return red, green, blue

try:
    tcs34725_init() # Inicializar el sensor
    
    while True:
        color = read_color()
        print("Color detectado:", color)
        time.sleep(1)

except KeyboardInterrupt:
    pass
