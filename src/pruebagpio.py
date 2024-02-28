import RPi.GPIO as GPIO
import time

# Define el pin GPIO que utilizarás para controlar el servo
servo_pin = 18

# Configura el modo de los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Crea un objeto PWM (Modulación de Ancho de Pulso) en el pin seleccionado
pwm = GPIO.PWM(servo_pin, 50) # Frecuencia de PWM: 50Hz (estándar para servos)

# Inicializa el servo en su posición neutra (90 grados)
pwm.start(7.5) # Puede necesitar ajustar este valor según tu servo

# Espera un tiempo para que el servo se mueva a la posición inicial
time.sleep(1)

# Detén el servo (opcional)
pwm.stop()

# Limpia los pines GPIO
GPIO.cleanup()
