import RPi.GPIO as GPIO

servo_pin_direccion = 2
servo_pin_traccion = 3

def init_servos():
    GPIO.setup(servo_pin_direccion, GPIO.OUT)
    GPIO.setup(servo_pin_traccion, GPIO.OUT)

def giro(valor_t, valor_d):
    pwm_d = GPIO.PWM(servo_pin_direccion, 50)
    pwm_t = GPIO.PWM(servo_pin_traccion, 50)
    
    pwm_d.start(valor_d)
    pwm_t.start(valor_t)
    # Resto del código de giro

    time.sleep(2)
    pwm_d.start(6.0)
    pwm_t.start(valor_t)
    time.sleep(2)
    pwm_d.start(6.0)
    pwm_t.start(valor_t)
    if valor_d == 11.5:
        pwm_d.start(3.5)
    elif valor_d == 3.5:
        pwm_d.start(11.5)
    else:
        pwm_d.start(6.0)
    time.sleep(2)
    valor_t = 12.5
    valor_d = 6.0
