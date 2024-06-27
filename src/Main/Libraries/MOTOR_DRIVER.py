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
GPIO.setup(18, GPIO.OUT)

# Set up PWM on the motor pins
MA1 = GPIO.PWM(p1MA, frecuencia)
MA2 = GPIO.PWM(p2MA, frecuencia)
MB1 = GPIO.PWM(p1MB, frecuencia)
MB2 = GPIO.PWM(p2MB, frecuencia)
Direccion = GPIO.PWM(18, 50)

# Start PWM with 0% duty cycle
MA1.start(cicloTrabajo)
MA2.start(cicloTrabajo)
MB1.start(cicloTrabajo)
MB2.start(cicloTrabajo)

# Define the move function
# Both values (percent_vel and percent_dir) go by -100% to 100%
def move(percent_vel, percent_dir):
    d = ((0.7 * pow((percent_dir/100), 2)) - (5 * (percent_dir/100)) + 6.8) #FORMULA QUE SE DEBE CAMBIAR SEGUN CUAL SEA EL CENTRO
    Direccion.start(d)

    if percent_vel > 0:
        print("AVANCE")
        duty_cycle = percent_vel
        MA1.ChangeDutyCycle(0)
        MA2.ChangeDutyCycle(duty_cycle)
        MB1.ChangeDutyCycle(0)
        MB2.ChangeDutyCycle(duty_cycle)
    elif percent_vel < 0:
        print("RETROCESO")
        duty_cycle = abs(percent_vel)
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