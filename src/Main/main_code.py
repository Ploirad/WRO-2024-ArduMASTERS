#BASIC LIBRARIES
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

#OUR LIBRARIES                                     # FUNCTIONS THAT WE ARE GOING TO USE
from Libraries import Boton as B                   # B.button_state()
from Libraries import Motor as M                   # M.movement(vel, dir, stop)
from Libraries import Ultrasonidos as HC           # HC.measure_distance(position) 1 Front; 2 Right; 3 Back; 4 Left
from Libraries import New_color_detector as CAM    # CAM.detect_green(frame)    CAM.detect_red(frame)   CAM.detect_magenta(frame)

# Initialize the camera as a picamera
camera = PiCamera()

# With a reslution of 320*240 px 
camera.resolution = (320, 240)
raw_capture = PiRGBArray(camera, size=(320, 240))

#Create the global variables
#Variables for HC
front_distance = 0
right_distance = 0
left_distance = 0
back_distance = 0

#Variables for CAM
green_centroid = None
red_centroid = None
magenta_centroid = None
green_area = 0
red_area = 0
magenta_area = 0

#Variables for M
direction = 0
traction = 0
go = False

#Variable for B
start = False

told = time.time()

# Take the frames continuously (without stop)
while True:
    frame = next(camera.capture_continuous(raw_capture, format="bgr", use_video_port=True))
    
    tnew = time.time()
    t = tnew - told
    print (f"Tiempo que tarda el frame: {t}")

    image = frame.array

    # PRINCIPAL LOGIC
    # If the button has been pressed
    if start:
        # Detect the centroids of the colors
        green_centroid, green_area = CAM.detect_green(image)
        red_centroid, red_area = CAM.detect_red(image)
        magenta_centroid, magenta_area = CAM.detect_magenta(image)

        # If we aren't seeing none color of the second round
        if (green_area < 10) and (red_area < 10):
            # Detect the distances
            front_distance = HC.measure_distance(1)
            right_distance = HC.measure_distance(2)
            left_distance = HC.measure_distance(4)
            #back_distance = HC.measure_distance(3)

            # And print them
            print(f"Front Distance: {front_distance}; Right Distance: {right_distance}; Left Distance: {left_distance}")#; Back Distance: {back_distance}")
            print("No color detected")

            # We comprobate if we can go forward without knock
            if front_distance > 30:
                print("FD > 30")

                # If we can we go forward
                traction = 1

                # We comprobate if we are very near to the walls
                if right_distance < 5:
                    # If we are very near to the right wall we go to the left
                    direction = -1
                    print("Going to the left")

                elif left_distance < 5:
                    # Else if we are very near to the left wall we go to the right
                    direction = 1
                    print("Going to the right")

                else:
                    # Else if we are not very near to none wall we go straight
                    direction = 0
                    print("Going straight")

            # Then if we can't go ahead too much time we turn the direction to the right or left
            elif front_distance > 10:
                print("10 < FD < 30")

                # We start going forward
                traction = 1

                # If the right distance is bigger than the left distance
                if right_distance > left_distance:
                    # We go to the right
                    direction = 1
                    print("Going to the right")

                # Else if the left is bigger than the right distance
                else:
                    # We go to the left
                    direction = -1
                    print("Going to the left")

            # If we can't go ahead
            else:
                print("FD < 10")

                # We go backward
                traction = -1

                # Then we decide if we can go to the right or to the left depending what is the bigest distance
                if right_distance > left_distance:
                    direction = -1
                    print("Backward + Right")
                
                else:
                    direction = 1
                    print("Backward + Left")

        # If we see any color
        else:
            print(f"Green Area: {green_area}; Red Area: {red_area}; Magenta Area: {magenta_area}")
            print(f"Green Centroid: {green_centroid}; Red Centroid: {red_centroid}; Magenta Centroid: {magenta_centroid}")
            print("Color detected")

            # We go forward
            traction = 1

            # Then we comprobate what is the nearest pillar
            # If is the green
            if green_area > red_area:
                # We overtake the green pillar by the right
                direction = 1
                print("Green detected, overtaking by the right")
            
            # Else if is red
            else:
                # We overtake the red pillar by the left
                direction = -1
                print("Red detected, overtaking by the left")

        # Move the car depending the desitions thet are taken about the movement of the car
        M.movement(traction, direction, go)
        print(f"Traction: {traction}; Direction: {direction}")

    # Then if the button has not been pressed
    else:
        # We wait for the button to be pressed
        print("Waiting for the button")
        if B.button_state():
            print("Button pressed")
            start = True

    # Clean the stream for the next frame
    raw_capture.truncate(0)

    tnew = time.time()
    t = tnew - told
    print(f"ULTIMA t: {t}")
    told = time.time()
    print("")

print("ENDING CODE")
# Close the camera
camera.close()