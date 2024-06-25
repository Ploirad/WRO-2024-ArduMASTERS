#L298N_PRUEBA_MOTOR.py
#Import the necessary libraries
import RPi.GPIO as GPIO

#Initialize the motors
GPIO.setmode(GPIO.BCM)

# -100% a 100%
def move(percent):
    if percent > 0:
        print("AVANCE")
        MA1.ChangeDutyCycle(0)
        MA2.ChangeDutyCycle(percent)
        MB1.ChangeDutyCycle(0)
        MB2.ChangeDutyCycle(percent)

    elif percent < 0:
        print("RETROCESO")
        MA1.ChangeDutyCycle(abs(percent))
        MA2.ChangeDutyCycle(0)
        MB1.ChangeDutyCycle(abs(percent))
        MB2.ChangeDutyCycle(0)

    else:
        print("STOP")
        MA1.ChangeDutyCycle(0)
        MA2.ChangeDutyCycle(0)
        MB1.ChangeDutyCycle(0)
        MB2.ChangeDutyCycle(0)

p1MA = 26
p2MA = 21
p1MB = 19
p2MB = 20
cicloTrabajo = 0
frecuencia = 1000

GPIO.setup(p1MA, GPIO.OUT)
GPIO.setup(p2MA, GPIO.OUT)
GPIO.setup(p1MB, GPIO.OUT)
GPIO.setup(p2MB, GPIO.OUT)

MA1 = GPIO.PWM(p1MA, frecuencia)
MA2 = GPIO.PWM(p2MA, frecuencia)
MB1 = GPIO.PWM(p1MB, frecuencia)
MB2 = GPIO.PWM(p2MB, frecuencia)

MA1.start(cicloTrabajo)
MA2.start(cicloTrabajo)
MB1.start(cicloTrabajo)
MB2.start(cicloTrabajo)

perc = int(input("Percent: "))
while True:
    move(perc)