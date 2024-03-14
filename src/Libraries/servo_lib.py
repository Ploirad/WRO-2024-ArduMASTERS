import RPi.GPIO as GPIO

class servos:
  def __init__(self, traccion_pin, direccion_pin):
    self.servo_pin_direccion = direccion_pin
    self.servo_pin_traccion = traccion_pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.servo_pin_direccion, GPIO.OUT)
    GPIO.setup(self.servo_pin_traccion, GPIO.OUT)
    self.pwm_d = GPIO.PWM(self.servo_pin_direccion, 50) # Frecuencia de PWM: 50Hz (estándar para servos)
    self.pwm_t = GPIO.PWM(self.servo_pin_traccion, 50) # Frecuencia de PWM: 50Hz (estándar para servos)
  
  def forward():
    pwm_t.start(12.5)
  
  def backward():
    pwm_t.start(2.5)
  
  def turn_left():
    pwm_d.start(11.5)
  
  def turn_right():
    pwm_d.start(3.5)
  
  def turn_center():
    pwm_d.start(6.0)
