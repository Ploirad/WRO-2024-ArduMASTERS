import board
import busio
import adafruit_tcs34725

# Configurar el bus I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Inicializar el sensor
sensor = adafruit_tcs34725.TCS34725(i2c)

def read_color():
    # Leer los valores de color RGB del sensor
    r, g, b, _ = sensor.color_rgb_bytes
    
    # Determinar el color basado en los valores RGB
    if r > 200 and g > 200 and b > 200:
        color = "Blanco"
    elif r > g and r > b:
        color = "Rojo"
    elif g > r and g > b:
        color = "Verde"
    elif b > r and b > g:
        color = "Azul"
    else:
        color = "Otros"
    
    return color

try:
    while True:
        color = read_color()
        print("Color detectado:", color)
        time.sleep(1)

except KeyboardInterrupt:
    pass
