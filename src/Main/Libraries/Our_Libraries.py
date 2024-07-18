import Boton as B                        # B.button_state()
import MOTOR_DRIVER as MD                # MD.move(percent_vel, percent_dir)
import Read_UltraSonic_sensors as RHC    # RHC.read_HC(i); 0/1/2/3 = FD/RD/BD/LD
import New_color_detector as CAM         # CAM.detect_green(frame)    CAM.detect_red(frame)   CAM.detect_magenta(frame)
import tsc34725 as tcs                   # get_color()
import Extra_Functions as F              # backward(traction, initial_direction)
