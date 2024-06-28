import RPi.GPIO as GPIO
import threading as thr

GPIO.setmode(GPIO.BCM)

# Declare servo pin
GPIO.setup(14, GPIO.OUT)

# Declare L298N pins
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT) 
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(0, GPIO.OUT)

# Declare the PWM pins
ENA = GPIO.PWM(26,50)
ENB = GPIO.PWM(0,50)
Direction = GPIO.PWM(14,50)

# Start PWM pins

GPIO.output(26,True)
GPIO.output(0,True)
GPIO.output(14,True)
ENA.start(0)
ENB.start(0)
Direction.start(0)

# Create funcion for stopping servo in auxiliary thread
Servo_stop = thr.Timer(0.1,lambda:[Direction.ChangeDutyCycle(0), GPIO.output(14,False)])

# Inputs of the function are VELocity and DIRection
def movement(vel,dir):
    # Set direction as desired
    GPIO.output(14,True)
    Direction.ChangeDutyCycle(dir/18+2)
    Servo_stop.start()
    
    if vel > 0: # Go foreward
        GPIO.output(19,True)
        GPIO.output(13,False)
        GPIO.output(6,True)
        GPIO.output(5,False)
        ENA.ChangeDutyCycle(vel)
        ENB.ChangeDutyCycle(vel)
    if vel < 0: # Go backwards
        GPIO.output(19,False)
        GPIO.output(13,True)
        GPIO.output(6,False)
        GPIO.output(5,True)
        ENA.ChangeDutyCycle(vel)
        ENB.ChangeDutyCycle(vel)
    else: # Stop everything
        GPIO.output(19,False)
        GPIO.output(13,False)
        GPIO.output(6,False)
        GPIO.output(5,False)
        GPIO.output(26,False)
        GPIO.output(0,False)