import random
def aleatorio ():
   return random.randint(1, 100)
    
def main():
   numero = 0
   acertado = False
   num_aleatorio = aleatorio()
   intentos = 0
   print("Bienvenido a Adivina el número!!!")
   while acertado == False:
      print("Por favor, introduzca un número:")
      numero = input()
      intentos += 1
      if int(numero) == num_aleatorio:
         print("Lo has adivinado en " + intentos)
         print("HAS GANADO, ¿QUIERES SEGUIR? (SI/NO)")
         if input("¿Quieres volver a jugar (y/n)?") == "y":
            print("Genial!")
            main()
      elif int(numero) < num_aleatorio:
         print("NO, ES MÁS ALTO")
      elif int(numero) > num_aleatorio:
         print("NO, ES MÁS BAJO")

if input("¿Quieres jugar? (y/n)") == "y":
   main()
