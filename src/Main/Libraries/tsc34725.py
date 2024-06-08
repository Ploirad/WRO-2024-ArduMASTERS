import time
from smbus import SMBus

def read_color():
    # Dirección del sensor TCS34725
    TCS34725_ADDRESS = 0x29

    # Registro de control
    TCS34725_COMMAND_BIT = 0x80
    TCS34725_ENABLE = 0x00
    TCS34725_ATIME = 0x01
    TCS34725_INTEGRATIONTIME_50MS = 0xEB  # 50ms de integración
    TCS34725_WAITTIME = 0x03
    TCS34725_ENABLE_AIEN = 0x10  # Interrupción de ADC activada
    TCS34725_ENABLE_WEN = 0x08  # Espera habilitada
    TCS34725_ENABLE_PON = 0x01  # Encendido normal
    TCS34725_ENABLE_AEN = 0x02  # Habilitar ADC y la interrupción de ADC

    # Inicializar el bus I2C
    bus = SMBus(1)

    # Configurar el sensor TCS34725
    bus.write_byte_data(TCS34725_ADDRESS, TCS34725_COMMAND_BIT | TCS34725_ATIME, TCS34725_INTEGRATIONTIME_50MS)
    bus.write_byte_data(TCS34725_ADDRESS, TCS34725_COMMAND_BIT | TCS34725_ENABLE, TCS34725_ENABLE_PON)
    bus.write_byte_data(TCS34725_ADDRESS, TCS34725_COMMAND_BIT | TCS34725_ENABLE, TCS34725_ENABLE_PON | TCS34725_ENABLE_AEN)

    # Leer los valores de color
    data = bus.read_i2c_block_data(TCS34725_ADDRESS, 0x16 | 0x80, 8)
    red = data[1] << 8 | data[0]
    green = data[3] << 8 | data[2]
    blue = data[5] << 8 | data[4]
    clear = data[7] << 8 | data[6]

    # Limpiar y cerrar el bus I2C
    bus.write_byte_data(TCS34725_ADDRESS, TCS34725_COMMAND_BIT | TCS34725_ENABLE, 0)
    bus.close()

    # Devolver los valores de color
    return red, green, blue, clear

while True:
    print(read_color())
