# This library is for do the parking part

# Import the libraries
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
from Libraries import Boton as B                        # B.button_state()
from Libraries import MOTOR_DRIVER as MD                # MD.move(percent_vel, percent_dir)
from Libraries import Read_UltraSonic_sensors as RHC    # RHC.read_HC(i); 0/1/2/3 = FD/RD/BD/LD
from Libraries import New_color_detector as CAM         # CAM.detect_green(frame)    CAM.detect_red(frame)   CAM.detect_magenta(frame)
from Libraries import tcs34725 as tcs                   # get_color()
from Libraries import Extra_Functions as F              # backward(traction, initial_direction)

# We start counting the time in that we do the race
started_time = time.time()

# Initialize the camera as a picamera
camera = CAM.camera
camera.framerate = 90 #65

# With a reslution of 320*240 px 
camera.resolution = (320, 240)
raw_capture = PiRGBArray(camera, size=(320, 240))

#Create the global variables
#Variables for HC
front_distance = 0
right_distance = 0
left_distance = 0
back_distance = 0

#Global variables for CAM
magenta_centroid = None
magenta_area = 0

#Variables for MD
direction = 0
traction = 0

# This function is for the final part of the parking
def parking():
    global direction
    print("Parking mode")
    not_park = True
    not_parked = True
    parking = True
    if parking:
        for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
            image = frame.array
        
            # Detect the centroid and area of the magenta
            magenta_centroid, _ = CAM.detect_magenta(image)

            # We save the back distance in back_distance
            back_distance = RHC.read_HC(2)

            # If we aren't parked we do this
            if not_parked:
                if magenta_centroid is not None and not_park:
                    direction = pass_wall(magenta_centroid)
                    MD.move(100, direction)
                
                else:
                    not_park = False
                    MD.move(-100, -direction)
                    
            # If we are parked we do this
            elif back_distance < 3:
                MD.move(0, 0)
                not_parked = False
                parking = False
                camera.close()
            # Clean the stream for the next frame
            raw_capture.truncate(0)

    print("parked")

# This function is for give the direction depending the magenta centroid
def pass_wall(magenta_centroid):
    # If the centroid is in the left of the screen
    if magenta_centroid < 320:
        direction = 100
        print("Parking, turn right")
    
    # If the centroid is in the right of the screen or in the center
    else:
        direction = -100
        print("Parking, turn left")
    return direction
