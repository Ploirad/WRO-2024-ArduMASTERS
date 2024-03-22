import RPi.GPIO as GPIO
import time
from servo_control import *
from ultrasound import *
from siguelineas import *

button_pin = 9

def setup_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def main():
    init_servos()
    init_ultrasonido()
    init_siguelineas()
    
    v = 0
    while True:
        button_state = GPIO.input(button_pin)
        if button_state == GPIO.HIGH:
            print("Botón presionado")
            if v == 0:
                setup_GPIO()
                v = 1
        
        try:
            if v == 1:
                distancia_delante = get_distance(TRIG_PIN_DELANTE, ECHO_PIN_DELANTE)
                # Lógica principal del robot
                pass
            
        except KeyboardInterrupt:
            GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
