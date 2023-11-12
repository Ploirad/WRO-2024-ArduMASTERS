
 
#importacion de librerias

#funcion principal Mario

#funcion aleatoria Mario

#Comprobacion de resultados Darío

#Fin del juego Adrián
texto = input()
intentos = 0
aprox = ""
win = texto == numero
if win == True:
    print("HAS GANADO, ¿QUIERES SEGUIR? (SI/NO)")
    if texto == "SI":
        #volver a hacer bucle
    elif texto == "NO":
        #cancelar repetición
    else:
        print("ESCRIBE -SI- O -NO-")
else:#aprox="GRANDE" // aprox="PEQUEÑO"
    print(f"NO, ES MÁS {aprox}")
    #Continuar
    intentos += 1