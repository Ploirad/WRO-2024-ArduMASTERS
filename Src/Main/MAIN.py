# LIBRARIES
import time
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
from Libraries import Boton as B                        # B.button_state()
from Libraries import MOTOR_DRIVER as MD                # MD.move(percent_vel, percent_dir)
from Libraries import Read_UltraSonic_sensors as RHC    # RHC.read_HC(i); 0/1/2/3 = FD/RD/BD/LD
from Libraries import New_color_detector as CAM         # CAM.detect_green(frame)    CAM.detect_red(frame)   CAM.detect_magenta(frame)
from Libraries import tsc34725 as tcs                   # get_color()
from Libraries import Extra_Functions as F              # backward(traction, initial_direction)
from Libraries import parking as P
from Libraries import Ultrasonic_deviation as UD

# We start counting the time in that we do the race
started_time = time.time()

# Initialize the camera as a picamera
camera = CAM.camera
camera.framerate = 30 #65

# With a reslution of 320*240 px 
camera.resolution = (640, 480)
raw_capture = PiRGBArray(camera, size=(640, 480))

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

#Variables for MD
direction = 0
traction = 0
normal_traction = int(input("vel: "))

#Variable for B
start = False

#Variables for count the turns
vertex_turns = 0
turns = 0
count_turns = True
first_color_detected = None
delay = False

#Variables for parking
pillar_has_been_detected = False
stop = False

told = time.time()
tnew = time.time()

try:
    # If we aren't finished running
    if not stop:
        raw_capture.truncate(0)
        
        print(f"Try: {time.time()-tnew}")

        # Take the frames continuously (without stop)
        for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

            tnew = time.time()
            t = tnew - told
            print (f"Tiempo que tarda el frame: {t}")

            image = frame.array

            # Get the image dimensions
            height, width = image.shape[:2]
        
            # Cut the image to take the inferior half part of it
            lower_half = image[height//2:, :]

            # MAIN LOGIC
            # If the button has been pressed
            if start:
                # Detect the centroids of the colors
                green_centroid, green_area = CAM.detect_green(lower_half)
                red_centroid, red_area = CAM.detect_red(lower_half)
                magenta_centroid, magenta_area = CAM.detect_magenta(lower_half)

                print(f"Green Area: {green_area}; Red Area: {red_area}; Magenta Area: {magenta_area}")
                print(f"Green Centroid: {green_centroid}; Red Centroid: {red_centroid}; Magenta Centroid: {magenta_centroid}")

                # If we need detect the lines:
                if count_turns:
                    # Take the color of the floor lines as a string
                    color = tcs.get_color()
                    print(color)

                # If we aren't seeing none color of the second round
                if (green_area < 1000) and (red_area < 550):
                    # Detect the distances
                    front_distance = RHC.read_HC(0)
                    right_distance = RHC.read_HC(1)
                    left_distance = RHC.read_HC(3)

                    UD.ultrasonic_dev(front_distance, right_distance, left_distance, normal_traction)

                    if front_distance > 1199:
                        F.backward(normal_traction, 0)

                    # If we detect that we aren't in the zone between orange and blue lines
                    if color == "Gray":
                        # We let the car incrementate vortex_turn in 1 unit when we detect a line in the floor
                        delay = False

                    # And print them
                    print(f"Front Distance: {front_distance}; Right Distance: {right_distance}; Left Distance: {left_distance}")
                    print("No color detected")

                    # We comprobate if we can go forward without knock
                    if front_distance > 70:
                        print("FD > 70")

                        # If we can we go forward
                        traction = normal_traction

                        # We comprobate if we are very near to the walls
                        if right_distance < 15:
                            # If we are very near to the right wall we go to the left
                            direction = -100
                            print("Going to the left")

                        elif left_distance < 15:
                            # Else if we are very near to the left wall we go to the right
                            direction = 100
                            print("Going to the right")

                        else:
                            # Else if we are not very near to none wall we go straight
                            direction = 0
                            print("Going straight")

                    # Then if we can't go ahead too much time we turn the direction to the right or left
                    elif front_distance > 30:
                        print("30 < FD < 70")

                        # We start going forward
                        traction = normal_traction

                        # If the right distance is bigger than the left distance
                        if right_distance > left_distance:
                            # We go to the right
                            direction = 100
                            print("Going to the right")
                            if color == "Orange" and (first_color_detected == None or first_color_detected == "Orange") and not delay and count_turns:
                                vertex_turns += 1
                                first_color_detected = "Orange"
                                delay = True

                        # Else if the left is bigger than the right distance
                        else:
                            # We go to the left
                            direction = -100
                            print("Going to the left")
                            if color == "Blue" and (first_color_detected == None or first_color_detected == "Blue") and not delay and count_turns:
                                vertex_turns += 1
                                first_color_detected = "Blue"
                                delay = True

                    # If we can't go ahead
                    else:
                        print("FD < 30")

                        # Then we decide if we can go to the right or to the left depending what is the bigest distance
                        if right_distance > left_distance:
                            F.backward(normal_traction, 100)
                            print("Backward + Right")
                            if color == "Blue" and (first_color_detected == None or first_color_detected == "Blue") and not delay and count_turns:
                                vertex_turns += 1
                                first_color_detected = "Blue"
                                delay = True
                        
                        else:
                            F.backward(normal_traction, -100)
                            print("Backward + Left")
                            if color == "Orange" and (first_color_detected == None or first_color_detected == "Orange") and not delay and count_turns:
                                vertex_turns += 1
                                first_color_detected = "Orange"
                                delay = True

                # If we see any color
                else:
                    # We say that we detected a color least 1 time
                    pillar_has_been_detected = True

                    print("Color detected")

                    # We go forward
                    traction = normal_traction

                    # Then we comprobate what is the nearest pillar
                    # If is the green
                    if green_area > red_area and green_area > 1000:
                        # We overtake the green pillar by the right
                        direction = 100
                        print("Green detected, overtaking by the right")
                    
                    # Else if is red
                    elif red_area > green_area and red_area > 550:
                        if turns == 3:
                            print("Changing direction")
                            F.change_direction()
                        else:
                            # We overtake the red pillar by the left
                            direction = -100
                            print("Red detected, overtaking by the left")

                # Move the car depending the desitions thet are taken about the movement of the car
                print(f"Traction: {traction}; Direction: {direction}")
                MD.move(traction, direction)
                print(f"Traction: {traction}; Direction: {direction}")

            # Then if the button has not been pressed
            else:
                # We wait for the button to be pressed
                print("Waiting for the button")
                if B.button_state():
                    print("Button pressed")
                    start = True

            # We obtain the number of complete turns that we done by taking vertex_turns and we divide it by the number of vertex
            turns = vertex_turns/4
            print(f"turns: {turns}")
            print(f"vertex_turns: {vertex_turns}")

            # If we done the 3 turns we comprobate if we are in the first or in the second round
            if turns >= 3:
                count_turns = False
                if pillar_has_been_detected:
                    parked = P.run_until_magenta_detected()
                    stop = parked
                    start = not parked
                else:
                    start = False
                    stop = True

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

    time_all_code = time.time() - started_time
    print("CODE ENDED")
    print("Congratulations you win in {time_all_code}")

except Exception as e:
    print(e)
    MD.GPIO.cleanup()
