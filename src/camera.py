from picamera2 import Picamera2, Preview

def record_video():
    with Picamera2() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 30

        # Preview configuration
        preview_config = Picamera2.Preview.create()
        preview_config.set_parameter(Picamera2.Preview.Parameter.FRAME_RATE, camera.framerate)
        preview_config.set_parameter(picamera2.Preview.Parameter.RESOLUTION, camera.resolution)

        # Video configuration
        video_config = Picamera2.Video.create()
        video_config.set_parameter(Picamera2.Video.Parameter.FRAME_RATE, camera.framerate)
        video_config.set_parameter(Picamera2.Video.Parameter.RESOLUTION, camera.resolution)

        camera.start_preview(preview_config)

        # Allow camera warm-up time
        camera.wait(2000)

        # Create a software encoder
        encoder = Picamera2.SoftwareEncoder(camera, 'mp4', video_config)

        # Create a file object for the output video
        with open('video.h264', 'wb') as output_file:
            for frame in encoder.capture_continuous(output_file, format='mp4', use_video_port=True):
                if frame.time > 30000:  # Stop recording after 30 seconds
                    break

record_video()
