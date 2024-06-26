#LIBRERIAS
import Ultrasonidos as HC  #Contiene la funcion:  HC.measure_distance(pos)  Para obtener la distancia que hay en el HC ubicado en la posicion pos
import Motor as M          #Contiene la funcion:  M.movement(AvanceRetroceso, DerechaCentroIzquierda)     Para mover los servos segun lo dicho en las variables
import time
import RPi.GPIO as GPIO

#CREAR EL BOTON
GPIO.setmode(GPIO.BCM)
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#VARIABLES
arrancado = False #variable que comprueba si el coche esta o no arrancado
TF = False

#BUCLE PRINCIPAL
while True:
  #si se ha arrancado
  if arrancado:
    print("vuelta")
    #OBTENER DISTANCIAS
    DDelantera = HC.measure_distance(1)
    DDerecha = HC.measure_distance(2)
    DTrasera = HC.measure_distance(3)
    DIzquierda = HC.measure_distance(4)
    #IMPRIMIRLAS
    print(DDelantera)
    print(DDerecha)
    print(DIzquierda)
    print(DTrasera)
    
    #SI SE PUEDE AVANZAR
    if DDelantera > 30:
      #SI ALGUNA DISTANCIA LATERAL ES MUY PEQUEÑA GIRAR AL OPUESTO
      if DDerecha < 6 and DIzquierda > 6:
        M.movement(1, -1, TF)
      elif DIzquierda < 6 and DDerecha > 6:
        M.movement(1, 1, TF)
      else:
        M.movement(1, 0, TF)
    
    #SI HAY POCA DISTANCIA PARA AVANZAR
    elif DDelantera > 5:
      #IR AL LADO MAS GRANDE
      if DDerecha > DIzquierda:
        M.movement(1, 1, TF)
      else:
        M.movement(1, -1, TF)
    
    #SI ESTA DEMASIADO CERCA DE LA PARED VE PARA ATRAS Y GIRA AL LADO MAS PEQUEÑO
    else:
      #RETROCEDER HASTA QUE LA DISTAANCIA DE ATRAS SEA 5CM
      while DDelantera < 30:    
        DDelantera = HC.measure_distance(1)
        DDerecha = HC.measure_distance(2)
        DTrasera = HC.measure_distance(3)
        DIzquierda = HC.measure_distance(4)
        print(DDelantera)
        print(DDerecha)
        print(DIzquierda)
        print(DTrasera)
        if DDerecha > DIzquierda:
          M.movement(-1, -1, TF)
        else:
          M.movement(-1, 1, TF)
      time.sleep(2)
      if DDerecha > DIzquierda:
        M.movement(1, -1, TF)
      else:
        M.movement(1, 1, TF)
        
  #SINO SE HA ARRANCADO
  else:
    print("esperando al boton")
    if GPIO.input(9) == GPIO.HIGH: #OBTENER VALOR DEL BOTON
      arrancado = True #ARRANCAR EL COCHE
