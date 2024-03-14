import RPi.GPIO as GPIO
import time

class Ultrasound:
    def __init__(self, Tforw, Eforw, Tback, Eback, TI, EI, TD, ED):
        self.Tforw = Tforw
        self.Eforw = Eforw
        self.Tback = Tback
        self.Eback = Eback
        self.TI = TI
        self.EI = EI
        self.TD = TD
        self.ED = ED
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Tforw, GPIO.OUT)
        GPIO.setup(Eforw, GPIO.IN)
        GPIO.setup(Tback, GPIO.OUT)
        GPIO.setup(Eback, GPIO.IN)
        GPIO.setup(TI, GPIO.OUT)
        GPIO.setup(EI, GPIO.IN)
        GPIO.setup(TD, GPIO.OUT)
        GPIO.setup(ED, GPIO.IN)
        

    def get_distance(trig_pin, echo_pin):
        # Envía un pulso al pin Trig
        GPIO.output(trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(trig_pin, False)
        pulse_end = 0
        pulse_start = 0
        while GPIO.input(echo_pin) == 0:
            pulse_start = time.time()
        while GPIO.input(echo_pin) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 3)
        return distance

    def get_US_forward():
        df = get_distance(Tforw, Eforw)
        return df
    def get_US_backward():
        db = get_distance(Tback, Eback)
        return db
    def get_US_left():
        dl = get_distance(TI, EI)
        return dl
    def get_US_right():
        dr = get_distance(TD, ED)
        return dr
