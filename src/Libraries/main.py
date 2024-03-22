#LIBRERIAS
import RPi.GPIO as GPIO
import time
from servo_control import *
from ultrasound import *
from siguelineas import *

#PINES
button_pin = 9

#CONSTANTES (NO CAMBIAN)
DA = (14, 15)
TAvance = 12.5
TAtras = 2.5
GDer = 3.5
GIzq = 11.5
GCent = 6.0

#VARIABLES
NoLinea = 0
NoTotalVueltas = 0
NoMaxVueltas = 0

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
                Dforw = get_distance(Tforw, Eforw)
                Dback = get_distance(Tback, Eback)
                DD = get_distance(TI, EI)
                DI = get_distance(TD, ED)

                if Dforw < DA[1] and DD < DA[1] and DI < DA[1]:
                    giro(TAtras, GCent)
                else:
                    if Dforw < DA[1] and DD > DA[0] and DD > DI:
                        giro(TAvance, GDer)
                    elif Dforw < DA[1] and DI > DA[0] and DI > DD:
                        giro(TAvance, GIzq)
                    elif Dforw > DA[0]:
                        giro(TAvance, GCent)
                if DI < 7 and DD > DI:
                    giro(TAvance, GDer)
                if DD < 7 and DI > DD:
                    giro(TAvance, GIzq)
                
                if leer_linea():
                    print("HAY LINEA")
                    NoLinea += 1
                    NoTotalVueltas += 1
                    if DD > DI:
                        giro(TAvance, GDer)
                    elif DI > DD:
                        giro(TAvance, GIzq)
                else:
                    print("NO HAY LINEA")

                if NoTotalVueltas == NoMaxVueltas:
                    v = 0
                print("Distancia delante:", distancia_delante, "cm")
                print("Distancia atrás:", distancia_atras, "cm")
                print("Distancia izquierda:", distancia_izquierda, "cm")
                print("Distancia derecha:", distancia_derecha, "cm")
                print("")
            else:
                print("PULSE EL BOTON")
        
        except KeyboardInterrupt:
            GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
