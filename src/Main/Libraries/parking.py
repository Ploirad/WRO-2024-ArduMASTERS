from picamera import PiCamera
from picamera.array import PiRGBArray
import time

# We start counting the time in that we do the race
started_time = time.time()

#OUR LIBRARIES                                     # FUNCTIONS THAT WE ARE GOING TO USE
from Libraries import Boton as B                   # B.button_state()
from Libraries import MOTOR_DRIVER as MD           # MD.move(percent_vel, percent_dir)
from Libraries import Ultrasonidos as HC           # HC.measure_distance(position) 1 Front; 2 Right; 3 Back; 4 Left
from Libraries import New_color_detector as CAM    # CAM.detect_green(frame)    CAM.detect_red(frame)   CAM.detect_magenta(frame)
from Libraries import tsc34725 as tcs              # get_color()
from Libraries import parking as P                 # parking()

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

# If we aren't detected magenta
def run_until_magenta_detected():
    global magenta_centroid, magenta_area, direction, traction, front_distance, right_distance, left_distance, traction, direction
    stop = False
    if not stop:
        # Take the frames continuously (without stop)
        for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

            image = frame.array
        
            # Detect the centroid and area of the magenta
            magenta_centroid, magenta_area = CAM.detect_magenta(image)

            if magenta_centroid is None:
                # Detecte the centroids and areas of the rest of colors    
                red_centroid, red_area = CAM.detect_red(image)
                green_centroid, green_area = CAM.detect_green(image)
                # If we aren't seeing none color of the second round
                if (green_area < 10) and (red_area < 10):
                    # Detect the distances
                    front_distance = HC.measure_distance(1)
                    right_distance = HC.measure_distance(2)
                    left_distance = HC.measure_distance(4)

                    # And print them
                    print(f"Front Distance: {front_distance}; Right Distance: {right_distance}; Left Distance: {left_distance}")
                    print("No color detected")

                    # We comprobate if we can go forward without knock
                    if front_distance > 30:
                        print("FD > 30")

                        # If we can we go forward
                        traction = 100

                        # We comprobate if we are very near to the walls
                        if right_distance < 5:
                            # If we are very near to the right wall we go to the left
                            direction = -100
                            print("Going to the left")

                        elif left_distance < 5:
                            # Else if we are very near to the left wall we go to the right
                            direction = 100
                            print("Going to the right")

                        else:
                            # Else if we are not very near to none wall we go straight
                            direction = 0
                            print("Going straight")

                    # Then if we can't go ahead too much time we turn the direction to the right or left
                    elif front_distance > 10:
                        print("10 < FD < 30")

                        # We start going forward
                        traction = 100

                        # If the right distance is bigger than the left distance
                        if right_distance > left_distance:
                            # We go to the right
                            direction = 100
                            print("Going to the right")

                        # Else if the left is bigger than the right distance
                        else:
                            # We go to the left
                            direction = -100
                            print("Going to the left")

                    # If we can't go ahead
                    else:
                        print("FD < 10")

                        # We go backward
                        traction = -100

                        # Then we decide if we can go to the right or to the left depending what is the bigest distance
                        if right_distance > left_distance:
                            direction = -100
                            print("Backward + Right")
                        
                        else:
                            direction = 100
                            print("Backward + Left")

                # If we see any color that is not magenta
                else:
                    print(f"Green Area: {green_area}; Red Area: {red_area}; Magenta Area: {magenta_area}")
                    print(f"Green Centroid: {green_centroid}; Red Centroid: {red_centroid}; Magenta Centroid: {magenta_centroid}")
                    print("Color detected")

                    # We go forward
                    traction = 100

                    # Then we comprobate what is the nearest pillar
                    # If is the green
                    if green_area > red_area:
                        # We overtake the green pillar by the right
                        direction = 100
                        print("Green detected, overtaking by the right")
                    
                    # Else if is red
                    else:
                        # We overtake the red pillar by the left
                        direction = -100
                        print("Red detected, overtaking by the left")

                # Move the car depending the desitions thet are taken about the movement of the car
                MD.move(traction, direction)
                print(f"Traction: {traction}; Direction: {direction}")

            else:
                parking()
                stop = True
            # Clean the stream for the next frame
            raw_capture.truncate(0)
    return True

def parking():
    print("Parking mode")
    not_park = True
    not_parked = True
    parking = True
    if parking:
        for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
            image = frame.array
        
            # Detect the centroid and area of the magenta
            magenta_centroid, _ = CAM.detect_magenta(image)

            if not_parked:
                if magenta_centroid is not None and not_park:
                    direction = pass_wall(magenta_centroid)
                    MD.move(100, direction)
                    
                else:
                    not_park = False
                    MD.move(-100, -direction)
                    
            elif back_distance < 3:
                MD.move(0, 0)
                not_parked = False
                parking = False
                camera.close()
            # Clean the stream for the next frame
            raw_capture.truncate(0)

    print("parked")

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