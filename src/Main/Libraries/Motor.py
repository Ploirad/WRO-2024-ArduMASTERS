#This code is a library for the servos and motors to move the car

#Import the necessary libraries
import RPi.GPIO as GPIO

#Initialize the motors
GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

# Declare the PWM pins for the motors
Motor = GPIO.PWM(3, 50)
Direccion = GPIO.PWM(2, 50)

#This function is used to move the car depending 3 variables:
#   vel: Say if the car is going to go forward (1), backward (-1) or is going to be stopped (0)
#   dir: Say if the car is going to turn left (1), right (-1) or straight (0)
#   stop:Say if the car is going to move (True) or is going to stop (False)
#And depending the variables the car will move in all directions
def movement(vel, dir, stop):
    # Convert input into usable value with the mathematic function: 7.5x^2 + 5x
    v = (7.5 * pow(vel, 2)) + (5 * vel)
    if v == 0 or stop:
        Motor.stop()
        Direccion.start(6.8)
    
    else:
        Motor.start(v)

        # Convert input into usable value with the mathematic function: 0.7x^2 − 5x + 6.8 
        d = ((0.7 * pow(dir, 2)) - (5 * dir) + 6.8)
        Direccion.start(d)

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

move(int(input("Percent: ")))