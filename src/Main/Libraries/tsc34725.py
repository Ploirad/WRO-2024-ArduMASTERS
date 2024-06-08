from smbus import SMBus
from gpiozero import Button
import time

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

# Registro de datos de color
TCS34725_CDATAL = 0x14  # Datos de color bajos (16 bits)
TCS34725_CDATAH = 0x15  # Datos de color altos (16 bits)

# Inicializar el bus I2C
bus = SMBus(1)

# Configurar el sensor TCS34725
bus.write_byte_data(TCS34725_ADDRESS, TCS34725_COMMAND_BIT | TCS34725_ATIME, TCS34725_INTEGRATIONTIME_50MS)
bus.write_byte_data(TCS34725_ADDRESS, TCS34725_COMMAND_BIT | TCS34725_ENABLE, TCS34725_ENABLE_PON)
time.sleep(0.5)
TCS34725_ENABLE_AEN = 0x02  # Habilitar ADC y la interrupción de ADC
bus.write_byte_data(TCS34725_ADDRESS, TCS34725_COMMAND_BIT | TCS34725_ENABLE, TCS34725_ENABLE_PON | TCS34725_ENABLE_AEN)

# Leer los valores de color continuamente
try:
    while True:
        # Leer los datos de color
        data = bus.read_i2c_block_data(TCS34725_ADDRESS, TCS34725_CDATAL | 0x80, 8)
        red = data[1] << 8 | data[0]
        green = data[3] << 8 | data[2]
        blue = data[5] << 8 | data[4]
        clear = data[7] << 8 | data[6]

        # Imprimir los valores de color
        print(f"Rojo: {red}, Verde: {green}, Azul: {blue}, Claro: {clear}")

        # Esperar un momento antes de leer nuevamente
        time.sleep(0.5)

except KeyboardInterrupt:
    # Limpiar y cerrar el bus I2C al salir
    bus.write_byte_data(TCS34725_ADDRESS, TCS34725_COMMAND_BIT | TCS34725_ENABLE, 0)
    bus.close()
