<p align="center">
  <img width="200" height="200" Src="https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Process/MASTERS.jpeg">
</p> 

# Sumary
These codes are used in order to test the different components of the ArduMASTERS 

# Files
- [Camera_color_detection_test.py](#camera_color_detection_testpy)
- [Camera_color_extractor_test.py](#camera-color-extractor-testpy)
- [Movement_test.py](#movement_testpy)
- [Tc34725_test.py](#tcs34725_testpy))
- [Ultrasound.py](#ultrasound_testpy)

> I don't write the file MOTOR_DRIVER in libraries becouse isn't a test code

# Test codes
## [Camera_color_detection_test.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Test%20codes/camera_color_detection_test.py)
This code is used to show a cloud of points of the green, red and magenta in different windows is used in conjuction with the next code.

## [Camera color extractor test.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Test%20codes/Camera_color_extractor_test.py)
This code is used for extract a color from a photo, then it print the highest and lowest value in [HSV](https://pro.arcgis.com/es/pro-app/latest/help/analysis/raster-functions/color-model-conversion-function.htm#:~:text=El%20modelo%20de%20color%20HSV,admite%20entradas%20de%203%20bandas) and put in the camera a cloud of points with its centroid in the range of color.

If you want to adjust the colors go to [this file](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Main/Libraries/New_color_detector.py) and put your values in the spaces marked in green in the photo.

![Foto camara](https://github.com/user-attachments/assets/9910ef55-61b3-4c22-b79f-0179ffdf60ef)

> Where we have "alto" means the highest value and "bajo" the lowest one.

> WARNING the first codes can only run in a rasberry pi with enviroment or x.

## [Movement_test.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Test%20codes/Movement_test.py)

This code ask you in the terminal the percentage of direction and traction and move the car according to the inputs.

## [Tcs34725_test.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/main/Src/Test%20codes/Tcs34725_test.py)

This code prints the values of the tcs34725 and its color based in aproximated values, being unknown if the code isn't one that we want.

## [Ultrasound_test.py](https://github.com/Ploirad/WRO-2024-ArduMASTERS/blob/mainV2/Src/Test%20codes/Ultrasound_test.py)

This code prints the distance value of the four HC sensors.
