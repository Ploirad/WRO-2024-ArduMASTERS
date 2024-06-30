import RPi.GPIO as GPIO
import time

# Inicializa la librería GPIO
GPIO.setmode(GPIO.BCM)

# Define los pines del motor y del servo
ENA = 26
IN1 = 19
IN2 = 13
IN3 = 6
IN4 = 5
ENB = 11
SERVO_PIN = 18

# Configura los pines como salida
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Configura PWM en los pines ENA y ENB
pwmENA = GPIO.PWM(ENA, 1000)
pwmENB = GPIO.PWM(ENB, 1000)

# Inicializa PWM con un ciclo de trabajo de 0%
pwmENA.start(0)
pwmENB.start(0)

# Inicializa PWM para el servo
Direccion = GPIO.PWM(SERVO_PIN, 50)
Direccion.start(0)

d = 7.5

center = float(input("center: "))

# Define la función de movimiento
def move(percent_vel, percent_dir):
    global d, center
    #center = 8
    #d = (((7-center)/10000)*pow(percent_dir, 2))+((1/20)*percent_dir)+center
    if percent_dir > 0:
        d = 12
    elif percent_dir < 0:
        d = 2
    else:
        d = center
    Direccion.start(d)
    # 2-12, 9.5
    print(d)

    if percent_vel > 0:
        print("AVANCE")
        duty_cycle = percent_vel
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwmENA.ChangeDutyCycle(duty_cycle)
        pwmENB.ChangeDutyCycle(duty_cycle)
    elif percent_vel < 0:
        print("RETROCESO")
        duty_cycle = abs(percent_vel)
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        pwmENA.ChangeDutyCycle(duty_cycle)
        pwmENB.ChangeDutyCycle(duty_cycle)
    else:
        print("STOP")
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        pwmENA.ChangeDutyCycle(0)
        pwmENB.ChangeDutyCycle(0)