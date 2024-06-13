#BASIC LIBRARIES
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

#OUR LIBRARIES                                     # FUNCTIONS THAT WE ARE GOING TO USE
from Libraries import Boton as B                   #button_state()
from Libraries import Motor as M                   #movement(vel, dir, stop)
from Libraries import Ultrasonidos as HC           #measure_distance(position) 1 Front; 2 Right; 3 Back; 4 Left
from Libraries import New_color_detector as CAM    #detect_green(frame)    detect_red(frame)   detect_magenta(frame)

# Initialize the camera 
camera = PiCamera()
camera.resolution = (640, 480)
raw_capture = PiRGBArray(camera, size=(640, 480))

#Create the global variables
front_distance = 0
right_distance = 0
left_distance = 0
back_distance = 0

green_centroid = None
red_centroid = None
magenta_centroid = None
green_area = None
red_area = None
magenta_area = None

direction = 0
traction = 0
start = False
go = False

# Take the frames continuously
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array

    if start:
        # Detect the centroids of the colors
        green_centroid, green_area = CAM.detect_green(image)
        red_centroid, red_area = CAM.detect_red(image)
        magenta_centroid, magenta_area = CAM.detect_magenta(image)

        # Detect the distances
        front_distance = HC.measure_distance(1)
        right_distance = HC.measure_distance(2)
        left_distance = HC.measure_distance(4)
        back_distance = HC.measure_distance(3)

        # Principal logic
        if green_area is None and red_area is None:
            if front_distance > 30:
                traction = 1
                if right_distance < 5:
                    direction = -1
                elif left_distance < 5:
                    direction = 1
                else:
                    direction = 0
            elif front_distance > 10:
                traction = 1
                if right_distance > left_distance:
                    direction = 1
                else:
                    direction = -1
            else:
                if right_distance > left_distance:
                    traction = -1
                    direction = -1
                else:
                    traction = -1
                    direction = 1
        else:
            if (green_area is not None and red_area is None) or (green_area > red_area):
                if green_area > 10:
                    traction = 1
                    direction = 1
            elif green_area is None and red_area is not None or (green_area < red_area):
                if red_area > 10:
                    traction = 1
                    direction = -1
            else:
                if green_area > red_area:
                    if green_area > 10:
                        traction = 1
                        direction = 1
                else:
                    if red_area > 10:
                        traction = 1
                        direction = -1

        # Move the car depending the desitions thet are taken about the movement of the car
        M.movement(traction, direction, go)

    else:
        # Wait for the button to be pressed
        if B.button_state():
            start = True

    # Clean the stream for the next frame
    raw_capture.truncate(0)

# Close the camera
camera.close()