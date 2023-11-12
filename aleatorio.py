
 
#importacion de librerias
fin = False
#fin indica el final de la partida
intentos = 0
#intentos son la cantidad de intentos que llevan los jugadores
distancia = ""
#distancia es para que la pongas directamente cuando digas la proximidad de el número
numero = 0
#numero es lo que los jugadores han insertado
#funcion principal Mario

#funcion aleatoria Mario
def main():
    print("Bienvenido a Adivina el número!!!")
    print("Por favor, introduzca un número:")
    numero = input()
#Comprobacion de resultados Darío
if numero == aleatorio:
  fin = True
elif numero > aleatorio:
   intentos += 1
   distancia = "alto"
elif numero < aleatorio:
   intentos += 1
   distancia = "bajo"
#Fin del juego Adrián
main()