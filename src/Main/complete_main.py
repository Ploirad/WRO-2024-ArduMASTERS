import Libraries.Motor as M            #movement(vel, dir, stop)
import Libraries.Ultrasonidos as US    #measure_distance(position)  -> distance
import Libraries.color_detector as cam #obtener_centroides()       -> green_area, red_area, magent_area, cv, cr, cm
import Libraries.Boton as B            #button_state()             -> True/False
import threading

# Variables
start = False
run = True
Aparcar = False
vueltas = 0

# Distancias de los sensores ultrasónicos
frontal_distance = 0.0
right_distance = 0.0
left_distance = 0.0
back_distance = 0.0

# Áreas detectadas por la cámara
green_area = 0
red_area = 0
magenta_area = 0

# Posición en el eje X de los centroides de los colores detectados por la cámara
green_centroid = 0
red_centroid = 0
magenta_centroid = 0

def update_sensors():
    global frontal_distance, right_distance, left_distance, back_distance
    while run:
        frontal_distance = US.measure_distance(1)
        right_distance = US.measure_distance(2)
        left_distance = US.measure_distance(4)
        back_distance = US.measure_distance(3)

def update_camera():
    global green_area, red_area, magenta_area, green_centroid, red_centroid, magenta_centroid
    while run:
        green_area, red_area, magenta_area, green_centroid, red_centroid, magenta_centroid = cam.obtener_centroides()

sensor_thread = threading.Thread(target=update_sensors)
camera_thread = threading.Thread(target=update_camera)

sensor_thread.start()
camera_thread.start()

def aparcar():
    global frontal_distance, right_distance, left_distance, back_distance, magenta_area, magenta_centroid, run, start, Aparcar
    
    if magenta_centroid < 213:
        M.movement(1, -1, False)
        while magenta_area > 0:
            update_variables()
            M.movement(1, 0, False)
        while back_distance > 2:
            update_variables()
            M.movement(-1, 1, False)
    else:
        M.movement(1, 1, False)
        while magenta_area > 0:
            update_variables()
            M.movement(1, 0, False)
        while back_distance > 2:
            update_variables()
            M.movement(-1, -1, False)

    M.movement(0, 0, True)
    run = False
    start = False
    Aparcar = False
    print("CAR STOPPED")

while run:
    if not B.button_state():
        start = True
        print("BOTON PULSADO")
    
    if start:
        if frontal_distance > 30:
            if right_distance < 10:
                M.movement(1, 1, False)
                last_direction = 1
            elif left_distance < 10:
                M.movement(1, -1, False)
                last_direction = -1
            else:
                M.movement(1, 0, False)
        elif frontal_distance > 10:
            if right_distance < 10:
                while frontal_distance < 25:
                    update_variables()
                    M.movement(1, 1, False)
                    last_direction = 1
            elif left_distance < 10:
                while frontal_distance < 25:
                    update_variables()
                    M.movement(1, -1, False)
                    last_direction = -1
            else:
                while frontal_distance < 25:
                    update_variables()
                    M.movement(1, -1, False)
        else:
            while frontal_distance < 10:
                update_variables()
                if right_distance > left_distance:
                    while frontal_distance < 8:
                        update_variables()
                        M.movement(-1, -1, False)
                    M.movement(1, 1, False)
                else:
                    while frontal_distance < 8:
                        update_variables()
                        M.movement(-1, 1, False)
                    M.movement(1, -1, False)
            M.movement(1, 0, False)

        if right_distance < 6:
            M.movement(1, -1, False)
        if left_distance < 6:
            M.movement(1, 1, False)
        
        if green_area > red_area:
            if green_area > 4:
                M.movement(1, -1, False)
                print("V>R")
        else:
            if red_area > 1200:
                M.movement(1, 1, False)
                print("R>V")

        if vueltas == 3 and magenta_area > 10000:
            Aparcar = True
        
        while Aparcar:
            aparcar()

# Detener los threads al finalizar el programa
run = False
sensor_thread.join()
camera_thread.join()
