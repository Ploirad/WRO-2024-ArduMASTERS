import RPi.GPIO as GPIO
import time
from servo_control import *

button_pin = 9

def setup_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def main():
    setup_GPIO()  # Configurar pines GPIO
    
    # Inicializar servos
    init_servos()
    
    v = 0
    while True:
        button_state = GPIO.input(button_pin)
        if button_state == GPIO.HIGH:
            print("Botón presionado")
            if v == 0:
                v = 1
        
        try:
            if v == 1:
                # Lógica principal del robot
                
                # Ejemplo de uso de los servos
                print("Moviendo los servos...")
                giro(12.5, 6.0)  # Ejemplo: mover hacia adelante y centrar dirección
                time.sleep(2)    # Espera 2 segundos
                giro(2.5, 11.5)  # Ejemplo: mover hacia atrás y girar a la derecha
                time.sleep(2)    # Espera 2 segundos
                giro(12.5, 3.5)  # Ejemplo: mover hacia adelante y girar a la izquierda
                time.sleep(2)    # Espera 2 segundos
            
        except KeyboardInterrupt:
            GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
