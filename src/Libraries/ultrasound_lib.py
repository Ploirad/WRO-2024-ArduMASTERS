import RPi.GPIO as GPIO

class Ultrasound:
    def __init__(self, Tforw, Eforw, Tback, Eback, TI, EI, TD, ED):
      self.TRIG_PIN_DELANTE = Tforw
      self.ECHO_PIN_DELANTE = Eforw
      self.TRIG_PIN_ATRAS = Tback
      self.ECHO_PIN_ATRAS = Eback
      self.TRIG_PIN_IZQUIERDA = TI
      self.ECHO_PIN_IZQUIERDA = EI
      self.TRIG_PIN_DERECHA = TD
      self.ECHO_PIN_DERECHA = ED
      distancia_delante = 0
      distancia_atras = 0
      distancia_izquierda = 0
      distancia_derecha = 0
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(TRIG_PIN_DELANTE, GPIO.OUT)
      GPIO.setup(ECHO_PIN_DELANTE, GPIO.IN)
      GPIO.setup(TRIG_PIN_ATRAS, GPIO.OUT)
      GPIO.setup(ECHO_PIN_ATRAS, GPIO.IN)
      GPIO.setup(TRIG_PIN_IZQUIERDA, GPIO.OUT)
      GPIO.setup(ECHO_PIN_IZQUIERDA, GPIO.IN)
      GPIO.setup(TRIG_PIN_DERECHA, GPIO.OUT)
      GPIO.setup(ECHO_PIN_DERECHA, GPIO.IN)

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
        df = get_distance(TRIG_PIN_DELANTE, ECHO_PIN_DELANTE)
        return df
    def get_US_backward():
        db = get_distance(TRIG_PIN_ATRAS, ECHO_PIN_ATRAS)
        return db
    def get_US_left():
        dl = get_distance(TRIG_PIN_IZQUIERDA, ECHO_PIN_IZQUIERDA)
        return dl
    def get_US_right():
        dr = get_distance(TRIG_PIN_DERECHA, ECHO_PIN_DERECHA)
        return dr
