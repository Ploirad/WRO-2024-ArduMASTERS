import RPi.GPIO as GPIO

class Button:
  def __init__(self, button_pin):
    self.button_pin = pin_boton
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  def button_lecture():
    State = False
    button_state = GPIO.input(button_pin)
    if button_state == GPIO.HIGH:
      State = True
    else:
      State = False
    return State
