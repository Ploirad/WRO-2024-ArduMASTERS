import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

Motor = GPIO.PWM(3, 50)
Direccion = GPIO.PWM(2, 50)

def movimiento(vel, dir, stop):
    if vel > 0:
        sen = 12.5
    elif vel < 0: 
        sen = 2.5
    else:
        stop = 1

    if not stop:
        Motor.start(sen)
        Direccion.start(4.5+(dir/30))
    else:
        Motor.stop()
        Direccion.start(7.5)

v = input("vel: ")
v = int(v)
d = input("dir: ")
d = int(d)
print(v)
print(d)
while True:
    movimiento(v, d, False)
