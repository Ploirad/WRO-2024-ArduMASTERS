import RPi.GPIO as GPIO
import time

# Define el pin GPIO que utilizarás para controlar el servo
servo_pin_direccion = 18
servo_pin_traccion = 17

valor_d = 7.5 #2.5=izq; 7.5=centro; 12.5=der
valor_t = 7   #6=Atras;  8=Alante;  7=stop

# Configura el modo de los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin_direccion, GPIO.OUT)
GPIO.setup(servo_pin_traccion, GPIO.OUT)

# Crea un objeto PWM (Modulación de Ancho de Pulso) en el pin seleccionado
pwm_d = GPIO.PWM(servo_pin_direccion, 50) # Frecuencia de PWM: 50Hz (estándar para servos)
pwm_t = GPIO.PWM(servo_pin_traccion, 50) # Frecuencia de PWM: 50Hz (estándar para servos)

valor_d = 7.5
valor_t = 12.5
pwm_d.start(valor_d)
pwm_t.start(valor_t)

time.sleep(4)

valor_d = 2.5
valor_t = 2.5
pwm_d.start(valor_d)
pwm_t.start(valor_t)

time.sleep(4)

valor_d = 12.5
valor_t = 12.5
pwm_d.start(valor_d)
pwm_t.start(valor_t)

time.sleep(4)

#Reinicio
pwm_d.start(6)
pwm_t.start(7)
time.sleep(4)

# Detén el servo (opcional)
pwm_d.stop()
pwm_t.stop()

# Limpia los pines GPIO
GPIO.cleanup()
