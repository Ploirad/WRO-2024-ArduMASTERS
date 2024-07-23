import numpy as np
from Libraries import Extra_Functions as F

front_ultrasonic_measure_list = []

def ultrasonic_deviation(ultrasonic_measure, right, left, normal_traction):
    front_deviation = calc(ultrasonic_measure)
    print(f"front_deviation: {front_deviation}")
    if front_deviation > 10:
        if right > left:
            F.backward(normal_traction, 100, True)
        else:
            F.backward(normal_traction, -100, True)

def calc(ultrasonic_measure):
    global front_ultrasonic_measure_list
    front_ultrasonic_measure_list.append(ultrasonic_measure)
    if len(front_ultrasonic_measure_list) > 5:
        front_ultrasonic_measure_list.pop(0)
    print(f"front_ultrasonic_measure_list: {front_ultrasonic_measure_list}")
    if len(front_ultrasonic_measure_list) > 4:
        front_deviation = np.std(front_ultrasonic_measure_list)
        return front_deviation
    else:
        return 10