import RPi.GPIO as GPIO
import time

# Configuración de pines
IRsensor = 17
numberlinea = 0

# Inicialización de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IRsensor, GPIO.IN)

try:
    while True:
        linea = GPIO.input(IRsensor)
        
        # Toma de decisiones
        if linea == 1:
          numberlinea = numberlinea + 1
        print(nl)

except KeyboardInterrupt:
    GPIO.cleanup()
