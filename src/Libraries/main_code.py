import button
import time

#TRIG_pin_DELANTE = 23
#ECHO_pin_DELANTE = 24
#TRIG_pin_ATRAS = 17
#ECHO_pin_ATRAS = 27
#TRIG_pin_IZQUIERDA = 22
#ECHO_pin_IZQUIERDA = 10
#TRIG_pin_DERECHA = 5
#ECHO_pin_DERECHA = 6
#servo_pin_direccion = 2
#servo_pin_traccion = 3
button_pin = 9

#VARIABLES
estado_boton = False
empezar = False

#ultrasonidos = Us.Ultrasound(TRIG_pin_DELANTE, ECHO_pin_DELANTE, TRIG_pin_ATRAS, ECHO_pin_ATRAS, TRIG_pin_IZQUIERDA, ECHO_pin_IZQUIERDA, TRIG_pin_DERECHA, ECHO_pin_DERECHA)
#servos = Servomotor.servos(servo_pin_traccion, servo_pin_direccion)
boton = button.Button(button_pin)
while True:
  estado_boton = boton.button_lecture()
  if estado_boton:
    print("Botón presionado")
    empezar = True

  try:
    if empezar:
      print("empezado")
  except KeyboardInterrupt:
        GPIO.cleanup()
