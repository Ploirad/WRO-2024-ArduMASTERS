import smbus2

def read_color():
    # Dirección del sensor TCS34725
    TCS34725_ADDRESS = 0x29

    # Registro de control
    TCS34725_ENABLE = 0x00
    TCS34725_ATIME = 0x01
    TCS34725_CONTROL = 0x0F
    TCS34725_ID = 0x12
    TCS34725_CDATAL = 0x14
    TCS34725_RDATAL = 0x16
    TCS34725_GDATAL = 0x18
    TCS34725_BDATAL = 0x1A

    # Inicializar el bus I2C
    bus = smbus2.SMBus(1)

    # Configurar el sensor TCS34725
    bus.write_byte_data(TCS34725_ADDRESS, TCS34725_ENABLE, 0x01)
    bus.write_byte_data(TCS34725_ADDRESS, TCS34725_ATIME, 0xEB)
    bus.write_byte_data(TCS34725_ADDRESS, TCS34725_CONTROL, 0x03)

    # Leer el ID del sensor para verificar si está listo
    sensor_id = bus.read_byte_data(TCS34725_ADDRESS, TCS34725_ID)
    while sensor_id != 0x44:
        sensor_id = bus.read_byte_data(TCS34725_ADDRESS, TCS34725_ID)

    # Leer los valores de color
    red = bus.read_word_data(TCS34725_ADDRESS, TCS34725_RDATAL)
    green = bus.read_word_data(TCS34725_ADDRESS, TCS34725_GDATAL)
    blue = bus.read_word_data(TCS34725_ADDRESS, TCS34725_BDATAL)
    clear = bus.read_word_data(TCS34725_ADDRESS, TCS34725_CDATAL)

    # Limpiar y cerrar el bus I2C
    bus.close()

    # Devolver los valores de color
    return red, green, blue, clear

# Ejemplo de uso
if __name__ == "__main__":
    r, g, b, c = read_color()
    print(f"Rojo: {r}, Verde: {g}, Azul: {b}, Claro: {c}")
