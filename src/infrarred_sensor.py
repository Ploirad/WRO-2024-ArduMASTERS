import RPi.GPIO as GPIO
import time

# Configuración de pines
IRsensor = 8
numberlinea = 0

# Inicialización de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IRsensor, GPIO.IN)

try:
    while True:
        linea = GPIO.input(IRsensor)
        
        # Toma de decisiones
        if linea == 0:
          numberlinea = numberlinea + 1
        print(f"NumberLinea{numberlinea}")
        print(f"Linea:{linea}")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
