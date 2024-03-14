import servo_lib.py as Servomotor
import ultrasound_lib as Us
import button as boton
import time

TRIG_pin_DELANTE = 23
ECHO_pin_DELANTE = 24
TRIG_pin_ATRAS = 17
ECHO_pin_ATRAS = 27
TRIG_pin_IZQUIERDA = 22
ECHO_pin_IZQUIERDA = 10
TRIG_pin_DERECHA = 5
ECHO_pin_DERECHA = 6
servo_pin_direccion = 2
servo_pin_traccion = 3
button_pin = 9

#VARIABLES
estado_boton = False
empezar = False

ultrasonidos = Us.Ultrasound(TRIG_pin_DELANTE, ECHO_pin_DELANTE, TRIG_pin_ATRAS, ECHO_pin_ATRAS, TRIG_pin_IZQUIERDA, ECHO_pin_IZQUIERDA, TRIG_pin_DERECHA, ECHO_pin_DERECHA)
servos = Servomotor.servos(servo_pin_traccion, servo_pin_direccion)
Boton = boton.Button(button_pin)
while True:
  estado_boton = Boton.button_lecture()
  if estado_boton:
    print("Botón presionado")
    empezar = True

  try:
    if empezar:
      distancia_delante = ultrasonidos.get_US_forward()
      distancia_atras = ultrasonidos.get_US_backward()
      distancia_izquierda = ultrasonidos.get_US_left()
      distancia_derecha = ultrasonidos.get_US_right()
      
      if distancia_delante < 15 and distancia_izquierda < 15 and distancia_derecha < 15:
        servos.backward()
        servos.turn_center()
      else:
        if distancia_delante < 15 and distancia_derecha > 14:
          #DERECHA
          servos.forward()
          servos.turn_right()
        elif distancia_delante < 15 and distancia_derecha < 15 and distancia_izquierda > 14:
          #IZQUIERDA
          servos.forward()
          servos.turn_left()
        elif distancia_delante < 15 and distancia_derecha < 15 and distancia_izquierda < 15:
          #ATRAS
          servos.backward()
          servos.turn_center()
        elif distancia_delante > 14:
          #AVANCE
          servos.forward()
          servos.turn_center()

        if distancia_izquierda < 7:
          #DERECHA
          servos.forward()
          servos.turn_right()

        if distancia_derecha < 7:
          #IZQUIERDA
          servos.forward()
          servos.turn_left()

        if distancia_atras < 14:
          servos.forward()
      print(f"Distancia hacia delante: {distancia_delante} cm")
      print(f"Distancia hacia atras: {distancia_atras} cm")
      print(f"Distancia hacia izquierda: {distancia_izquierda} cm")
      print(f"Distancia hacia derecha: {distancia_derecha} cm")
      print("")
      pwm_t.start(valor_t)
      pwm_d.start(valor_d)
      if valor_t > 8:
          print("avanti")
      elif valor_t < 6:
          print("back")
      else:
          print("stop")
      if valor_d > 11:
          print("izquierda")
      elif valor_d < 4:
          print("derecha")
      else:
          print("centro")
  except KeyboardInterrupt:
        GPIO.cleanup()
