import pigpio
import time

def read_color():
    # Inicializar el objeto PiGPIO
    pi = pigpio.pi()

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

    # Configurar el sensor TCS34725
    pi.i2c_write_byte_data(TCS34725_ADDRESS, TCS34725_ENABLE, 0x01)
    pi.i2c_write_byte_data(TCS34725_ADDRESS, TCS34725_ATIME, 0xEB)
    pi.i2c_write_byte_data(TCS34725_ADDRESS, TCS34725_CONTROL, 0x03)

    # Esperar a que el sensor se estabilice
    time.sleep(0.5)

    # Leer los valores de color
    red = pi.i2c_read_word_data(TCS34725_ADDRESS, TCS34725_RDATAL)
    green = pi.i2c_read_word_data(TCS34725_ADDRESS, TCS34725_GDATAL)
    blue = pi.i2c_read_word_data(TCS34725_ADDRESS, TCS34725_BDATAL)
    clear = pi.i2c_read_word_data(TCS34725_ADDRESS, TCS34725_CDATAL)

    # Cerrar la conexión con PiGPIO
    pi.stop()

    # Devolver los valores de color
    return red, green, blue, clear

# Ejemplo de uso
if __name__ == "__main__":
    r, g, b, c = read_color()
    print(f"Rojo: {r}, Verde: {g}, Azul: {b}, Claro: {c}")
