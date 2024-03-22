import RPi.GPIO as GPIO
import time

servo_pin_direccion = 2
servo_pin_traccion = 3

def init_servos():
    GPIO.setup(servo_pin_direccion, GPIO.OUT)
    GPIO.setup(servo_pin_traccion, GPIO.OUT)

def giro(valor_t, valor_d):
    pwm_d = GPIO.PWM(servo_pin_direccion, 50)
    pwm_t = GPIO.PWM(servo_pin_traccion, 50)
    
    pwm_d.start(valor_d)
    pwm_t.start(valor_t)
    
    time.sleep(2)
    pwm_d.ChangeDutyCycle(6.0)  # Modificar el ciclo de trabajo en lugar de reiniciar
    pwm_t.ChangeDutyCycle(valor_t)  # Modificar el ciclo de trabajo en lugar de reiniciar
    time.sleep(2)
    pwm_d.ChangeDutyCycle(6.0)  # Modificar el ciclo de trabajo en lugar de reiniciar
    pwm_t.ChangeDutyCycle(valor_t)  # Modificar el ciclo de trabajo en lugar de reiniciar
    if valor_d == 11.5:
        pwm_d.ChangeDutyCycle(3.5)  # Modificar el ciclo de trabajo en lugar de reiniciar
    elif valor_d == 3.5:
        pwm_d.ChangeDutyCycle(11.5)  # Modificar el ciclo de trabajo en lugar de reiniciar
    else:
        pwm_d.ChangeDutyCycle(6.0)  # Modificar el ciclo de trabajo en lugar de reiniciar
    time.sleep(2)
    valor_t = 12.5
    valor_d = 6.0
