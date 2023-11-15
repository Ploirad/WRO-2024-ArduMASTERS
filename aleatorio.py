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
         while repeticion == False:
            texto = input()
            acertado = True
            if texto == "SI":
               acertado = 
            elif texto == "NO":
               acertado = False
            else:
               print("ESCRIBE -SI- O -NO-")
      elif int(numero) < num_aleatorio:
         print("NO, ES MÁS ALTO")
      elif int(numero) > num_aleatorio:
         print("NO, ES MÁS BAJO")

while hola == True:
   main()
