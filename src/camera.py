from picamera2 import Picamera2, Preview

def record_video():
    Picam = Picamera2
    Picam.resolution = (640, 480)
    Picam.framerate = 30

        # Preview configuration
    preview_config = Picam
    Picam.Preview.create()
    preview_config.set_parameter(Picam.Preview.Parameter.FRAME_RATE, Picam.framerate)
    preview_config.set_parameter(Picam.Preview.Parameter.RESOLUTION, Picam.resolution)

        # Video configuration
    video_config = Picam.Video.create()
    video_config.set_parameter(Picam.Video.Parameter.FRAME_RATE, Picam.framerate)
    video_config.set_parameter(Picam.Video.Parameter.RESOLUTION, Picam.resolution)

    Picam.start_preview(preview_config)

        # Allow camera warm-up time
    Picam.wait(2000)

        # Create a software encoder
    encoder = picamera2.SoftwareEncoder(picamera2, 'mp4', video_config)

        # Create a file object for the output video
    with open('video.h264', 'wb') as output_file:
        for frame in encoder.capture_continuous(output_file, format='mp4', use_video_port=True):
            if frame.time > 30000:  # Stop recording after 30 seconds
                break

record_video()
