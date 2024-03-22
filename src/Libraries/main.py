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
    setup_GPIO()  # Configurar pines GPIO
    init_servos()
    init_ultrasonido()
    init_siguelineas()
    
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
                # Ejemplo de uso de los ultrasonidos
                distancia_delante = get_distance(Tforw, Eforw)
                distancia_atras = get_distance(Tback, Eback)
                distancia_izquierda = get_distance(TI, EI)
                distancia_derecha = get_distance(TD, ED)

                if linea_detectada():
                    print("Línea detectada")
                else:
                    print("No se detecta línea")
                print("Distancia delante:", distancia_delante, "cm")
                print("Distancia atrás:", distancia_atras, "cm")
                print("Distancia izquierda:", distancia_izquierda, "cm")
                print("Distancia derecha:", distancia_derecha, "cm")
                print("")
            
        except KeyboardInterrupt:
            GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
