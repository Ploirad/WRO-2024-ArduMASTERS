#Special Libraries                             #Functions
import Libraries.Motor as M            #movement(vel, dir, stop)
import Libraries.Ultrasonidos as US    #measure_distance(position)  -> distance
import Libraries.color_detector as cam #obtener_centroides()           -> green_area, red_area, magent_area, cv, cr, cm
import Libraries.Boton as B            #button_state()              -> True/False

#Variables
start = False
run = True
Aparcar = False
vueltas = 0

#This distances are the distances of the ultrasounds sensors
frontal_distance = 0.0
right_distance = 0.0
left_distance = 0.0
back_distance = 0.0

#The areas detected by the camera
green_area = 0
red_area = 0
magenta_area = 0

#The position in the X edge of the centroids of the colors detected by the camera
green_centroid = 0
red_centroid = 0
magenta_centroid = 0

def update_variables():
  global frontal_distance, right_distance, left_distance, back_distance, green_area, red_area, magenta_area, green_centroid, red_centroid, magenta_centroid
  frontal_distance = US.measure_distance(1)
  print(f"frontal_distance = {frontal_distance}")
  right_distance = US.measure_distance(2)
  print(f"right_distance = {right_distance}")
  left_distance = US.measure_distance(4)
  print(f"left_distance = {left_distance}")
  back_distance = US.measure_distance(3)
  print(f"back_distance = {back_distance}")
  green_area, red_area, magenta_area, green_centroid, red_centroid, magenta_centroid = cam.obtener_centroides()
  print(f"green_area = {green_area}, red_area = {red_area}, magenta_area = {magenta_area}")
  print(f"green_centroid = {green_centroid}, red_centroid = {red_centroid}, magenta_centroid = {magenta_centroid}")

#640 _> 0-213-427-640
def aparcar():
  global frontal_distance, right_distance, left_distance, back_distance, magenta_area, magenta_centroid, run, start, Aparcar
  update_variables()

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
    update_variables()

    if frontal_distance > 30:
      if right_distance < 10:
        M.movement(1, 1, False)
        last_direction = 1
        M.movement(1, 0, False)
      elif left_distance < 10:
        M.movement(1, -1, False)
        last_direction = -1
        M.movement(1, 0, False)
      else:
        M.movement(1, 0, False)

    elif frontal_distance > 10:
      if right_distance < 10:
        while frontal_distance < 25:
          update_variables()
          M.movement(1, 1, False)
          last_direction = 1
        M.movement(1, 0, False)

      elif left_distance < 10:
        while frontal_distance < 25:
          update_variables()
          M.movement(1, -1, False)
          last_direction = -1
        M.movement(1, 0, False)
      else:
        while frontal_distance < 25:
          update_variables()
          M.movement(1, -1, False)
        M.movement(1, 0, False)
    
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
    
    if green_area > red_area:
      if green_area > 10000:
        M.movement(1, -1, False)
        print("V>R")
    
    else:
      if red_area > 10000:
        M.movement(1, 1, False)
        print("R>V")

    #AÑADIR AQUÍ EL DETECTOR TCS PARA SABER SI HEMOS DADO UNA VUELTA

    if vueltas == 3:
      if magenta_area > 10000:
        Aparcar = True
  
    while Aparcar:
        aparcar()
