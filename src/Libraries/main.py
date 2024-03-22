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
                
                # Aquí puedes agregar tu lógica para controlar el robot
                # Por ejemplo, mover los servos en respuesta a ciertas condiciones,
                # leer sensores, etc.
                
                # Por ahora, simplemente imprime un mensaje
                print("Ejecutando lógica principal del robot...")
                time.sleep(1)  # Espera 1 segundo antes de continuar
            
        except KeyboardInterrupt:
            GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
