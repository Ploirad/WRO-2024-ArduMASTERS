import time
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder

def record_video():
    with Picamera2() as picam2:
        picam2.resolution = (640, 480)
        picam2.framerate = 30

        # Preview configuration
        preview_config = picam2.preview_configuration(main={"size": picam2.resolution})
        preview_config.set_parameter(picam2.Preview.Parameter.FRAME_RATE, picam2.framerate)
        preview_config.set_parameter(picam2.Preview.Parameter.RESOLUTION, picam2.resolution)

        # Video configuration
        video_config = picam2.video_configuration(main={"size": picam2.resolution, "frame_rate": picam2.framerate})

        picam2.start_preview(preview_config)

        # Allow camera warm-up time
        time.sleep(2)

        # Create a software encoder
        encoder = H264Encoder(picam2, 'mp4', video_config)

        # Create a file object for the output video
        with open('video.mp4', 'wb') as output_file:
            for frame in encoder.capture_continuous(output_file, format='mp4'):
                pass
if  __name__ == "__main__":
    try:
        record_video()
    except KeyboardInterrupt:
        print("Stopping recording...")