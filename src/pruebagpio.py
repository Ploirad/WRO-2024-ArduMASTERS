import RPi.GPIO as GPIO
import time

# Limpia los pines GPIO
GPIO.cleanup()

# Define el pin GPIO que utilizarás para controlar el servo
servo_pin_direccion = 18
servo_pin_traccion = 17
boton_pin = 27

valor_d = 7.5 #2.5=izq; 7.5=centro; 12.5=der
valor_t = 0   #6=Atras;  8=Alante;  =stop

# Configura el modo de los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin_direccion, GPIO.OUT)
GPIO.setup(servo_pin_traccion, GPIO.OUT)
GPIO.setup(boton_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Crea un objeto PWM (Modulación de Ancho de Pulso) en el pin seleccionado
pwm_d = GPIO.PWM(servo_pin_direccion, 50) # Frecuencia de PWM: 50Hz (estándar para servos)
pwm_t = GPIO.PWM(servo_pin_traccion, 50) # Frecuencia de PWM: 50Hz (estándar para servos)

while True:
  arranco = GPIO.input(boton_pin)
  if arranco == GPIO.LOW:
    print("ON"))
    valor_d = 7.5
    valor_t = 8
    pwm_d.start(valor_d)
    pwm_t.start(valor_t)
    
    valor_d = 2.5
    valor_t = 6
    pwm_d.start(valor_d)
    pwm_t.start(valor_t)
    
    valor_d = 12.5
    valor_t = 8
    pwm_d.start(valor_d)
    pwm_t.start(valor_t)

# Detén el servo (opcional)
pwm.stop()
