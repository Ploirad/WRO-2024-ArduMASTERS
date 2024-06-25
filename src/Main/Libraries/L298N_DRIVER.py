import RPi.GPIO as GPIO

# Initialize the motors
GPIO.setmode(GPIO.BCM)

# Define the motor pins
p1MA = 26
p2MA = 21
p1MB = 19
p2MB = 20
cicloTrabajo = 0
frecuencia = 1000

# Set up the motor pins as output
GPIO.setup(p1MA, GPIO.OUT)
GPIO.setup(p2MA, GPIO.OUT)
GPIO.setup(p1MB, GPIO.OUT)
GPIO.setup(p2MB, GPIO.OUT)

# Set up PWM on the motor pins
MA1 = GPIO.PWM(p1MA, frecuencia)
MA2 = GPIO.PWM(p2MA, frecuencia)
MB1 = GPIO.PWM(p1MB, frecuencia)
MB2 = GPIO.PWM(p2MB, frecuencia)

# Start PWM with 0% duty cycle
MA1.start(cicloTrabajo)
MA2.start(cicloTrabajo)
MB1.start(cicloTrabajo)
MB2.start(cicloTrabajo)

# Define the move function
def move(percent):
    if percent > 0:
        print("AVANCE")
        duty_cycle = percent
        MA1.ChangeDutyCycle(0)
        MA2.ChangeDutyCycle(duty_cycle)
        MB1.ChangeDutyCycle(0)
        MB2.ChangeDutyCycle(duty_cycle)
    elif percent < 0:
        print("RETROCESO")
        duty_cycle = abs(percent)
        MA1.ChangeDutyCycle(duty_cycle)
        MA2.ChangeDutyCycle(0)
        MB1.ChangeDutyCycle(duty_cycle)
        MB2.ChangeDutyCycle(0)
    else:
        print("STOP")
        MA1.ChangeDutyCycle(0)
        MA2.ChangeDutyCycle(0)
        MB1.ChangeDutyCycle(0)
        MB2.ChangeDutyCycle(0)

try:
    while True:
        perc = int(input("Percent (-100 to 100, 999 to exit): "))
        if perc == 999:
            break
        move(perc)
finally:
    MA1.stop()
    MA2.stop()
    MB1.stop()
    MB2.stop()
    GPIO.cleanup()
    print("GPIO cleanup and program end.")
