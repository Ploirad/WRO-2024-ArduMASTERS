
 
#importacion de librerias
import random 
fin = False
#fin indica el final de la partida
intentos = 0
#intentos son la cantidad de intentos que llevan los jugadores
distancia = ""
#distancia es para que la pongas directamente cuando digas la proximidad de el número
numero = 0
#numero es lo que los jugadores han insertado
repeticion = False
again = True
#devuelve numero 
def aleatorio ():
    return random.randint(1, 100)

#funcion aleatoria Mario
def main():
   print("Bienvenido a Adivina el número!!!")
   print("Por favor, introduzca un número:")
   numero = input()
#Comprobacion de resultados Darío
   if numero == aleatorio:
      fin = True
   elif numero > aleatorio:
      distancia = "ALTO"
   elif numero < aleatorio:
      distancia = "BAJO"
#Fin del juego Adrián
   texto = input()
   if fin == True:
      print("HAS GANADO, ¿QUIERES SEGUIR? (SI/NO)")
      while repeticion == False:
         if texto == "SI":
            repeticion = True
         elif texto == "NO":
            repeticion = True
            again = False
      #cancelar repetición
         else:
            print("ESCRIBE -SI- O -NO-")
   else:#aprox="GRANDE" // aprox="PEQUEÑO"
      print(f"NO, ES MÁS {distancia}")
    #Continuar
      intentos += 1
while again == True:
   main()