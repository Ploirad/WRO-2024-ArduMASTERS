#Libraries                             #Functions
import Libraries.Motor as M            #movement(vel, dir, stop)
import Libraries.Ultrasonidos as US    #measure_distance(position)  -> distance
import Libraries.color_detector as cam #obtener_centroide           -> green_area, red_area, magent_area, cv, cr, cm
import Libraries.Boton as B            #button_state()              -> True/False

#Variables
start = False #It says if the car have to start or not

#This distances are the distances of the ultrasounds sensors
frontal_distance = 0
right_distance = 0
left_distance = 0
back_distance = 0

#The areas detected by the camera
green_area = 0
red_area = 0
magenta_area = 0

#The position in the X edge of the centroids of the colors detected by the camera
green_centroid = 0
red_centroid = 0
magenta_centroid = 0

while True:
  if B.button_state():
    start = True
  
  if start:
    
