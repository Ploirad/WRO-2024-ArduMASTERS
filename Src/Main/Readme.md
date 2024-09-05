<p  align="center">
  <img width="200" height="200" Src="https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Process/MASTERS.jpeg">
</p> 

# Files
- [Camera_Main.py](#camera_mainpy)
- [MAIN.py](#main)
- [Movement_Main.py](#movement_main)
- [Tcs_Main.py](#tcs_mainpy)

In [Libraries](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/Main/Libraries) we got all the functions and Json files that we use in our main files:
- [Boton.py](#botonpy)
- [End_rounds.py](#end_roundspy)
- [Movement_Functions.py](#movement_functionspy)
- [MOTOR_DRIVER.py](#motor_driverpy)
- [New_color_detector.py](#new_color_detectorpy)
- [Tcs34725.py](#tcs34725py)
- [Jsons](#jsons)
# Main
## [Camera_Main.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Camera_Main.py)
This code detect colors and calculate areas of different colors in the camera's view. This information is sent to a Json that is read by the main code. This code use the library [New_color_detector.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/New_color_detector.py).

## [MAIN.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/MAIN.py)
This code is designed to control a robot's movement based on color detection and sensor data written in Json files in other mains. This code uses the libraries [MOTOR_DRIVER.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/MOTOR_DRIVER.py), [Boton.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/Boton.py), [Movement_Functions](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/Movement_Functions.py) and [End_rounds](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/End_rounds.py).

## [Movement_Main](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Movement_Main.py)
This code continuously measure distances using ultrasonic sensors and write the measurements to a JSON file.

## [Tcs_Main.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Tcs_Main.py)
This code is designed to detect colors using a TCS34725 color sensor and write the detection results to a JSON file. This code uses the library [tcs34725.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/tcs34725.py).

# Libraries
## [Boton.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/Boton.py)
This code detects when the starting button is pressed.

## [End_rounds.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/End_rounds.py)
This code have the functions that is used in the end of its challenge, in case of the open challenge it try to find the exact place it started, in the obstacle challenge it execute the parking function.

## [MOTOR_DRIVER.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/MOTOR_DRIVER.py)
This code makes the DC Motors move in the direction we want.

## [Movement_functions.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/Movement_Functions.py)
This code have built-in functions that controls the movement: pivot_aproximation looks if there are a traffic sign after traspassing another one, backward goes back until it can move correctly and change_direction do a 180 degrees turn if the last traffic sign is red in the end of the second lap.

## [New_color_detector.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/New_color_detector.py)
This code checks if the camera sees the colours of the traffic signs in a certain range that we gave previously.

## [Tcs34725.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/tcs34725.py)
This code reads the tcs color values and with a range of colours it returns a variable with the stimated colour.

## [Jsons](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/Main/Libraries/Json)
The [CAM.json](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/Main/Libraries/Json/CAM.json), [Move.json](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/Main/Libraries/Json/Move.json) and [tcs_color_detection.json](https://github.com/Ploirad/WRO-2024-ArduMASTERS/tree/main/Src/Main/Libraries/Json/tcs_color_detection.json) files stores the information of the mains.