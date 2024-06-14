import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

# Declare the PWM pins for the motors
Motor = GPIO.PWM(3, 50)
Direccion = GPIO.PWM(2, 50)

Motor.start(0)
Direccion.start(7.5)

current_vel = 0
current_dir = 7.5

def set_servo_angle(servo, angle):
    duty = angle / 18 + 2.5
    servo.ChangeDutyCycle(duty)

def smooth_transition(target_vel, target_dir, stop, steps=10, delay=0.1):
    global current_vel, current_dir
    if stop:
        target_vel = 0

    vel_step = (target_vel - current_vel) / steps
    dir_step = (target_dir - current_dir) / steps

    for i in range(steps):
        current_vel += vel_step
        current_dir += dir_step
        Motor.ChangeDutyCycle(current_vel)
        Direccion.ChangeDutyCycle(current_dir)
        time.sleep(delay)

def movement(vel, dir, stop):
    # Convert input into usable value
    if vel == 1:
        target_vel = 12.5
    elif vel == -1:
        target_vel = 2.5
    else:
        target_vel = 7.5

    if dir == 0:
        target_dir = 6.8
    elif dir <= -1:
        target_dir = 12.5
    else:
        target_dir = 2.5

    smooth_transition(target_vel, target_dir, stop)

def avance():
    Motor.ChangeDutyCycle(12.5)
