import Ultrasonidos as HC
import Motor as M
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
TF = False
arrancado = False
DDelanteraAnteriorTruncada = 0.0
DDelantera = 0.0

while True:
  if arrancado:
    print("vuelta")
    DDelanteraAnteriorTruncada = (int((10*DDelantera)))/10
    DDelantera = HC.measure_distance(1)
    DDerecha = HC.measure_distance(2)
    DIzquierda = HC.measure_distance(4)
    print(DDelantera)
    print(DDerecha)
    print(DIzquierda)

    if ((int((10*DDelantera)))/10) == DDelanteraAnteriorTruncada:
      print(f"retroceso, {((int((10*DDelantera)))/10)} = {DDelanteraAnteriorTruncada}")
      M.movimiento(-1, 0, TF)
    else:
      if DDelantera > 30:
        if DDerecha < 6 and DIzquierda > 6:
          M.movimiento(1, -1, TF)
        elif DIzquierda < 6 and DDerecha > 6:
          M.movimiento(1, 1, TF)
        else:
          M.movimiento(1, 0, TF)
      elif DDelantera > 5:
        M.movimiento(1, (1 if DDerecha > DIzquierda else (-1 if DIzquierda > DDerecha else DDerecha)), TF)
      else:
        M.movimiento(-1, (1 if DDerecha > DIzquierda else (-1 if DIzquierda > DDerecha else DDerecha)), TF)
        DTrasera = HC.measure_distance(3)
        if DTrasera < 5:
          M.movimiento(1, 0, TF)
  else:
    print("esperando al boton")
    if GPIO.input(9) == GPIO.HIGH:
      arrancado = True
