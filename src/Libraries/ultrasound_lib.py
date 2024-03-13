import RPi.GPIO as GPIO

class Servos:
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

