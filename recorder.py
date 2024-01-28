import cv2
import time
import os
from datetime import datetime
import shutil

class VideoRecorder:
    def __init__(self, camera_index=0, save_directory='local_videos', temp_directory='temp_videos'):
        self.camera_index = camera_index
        self.save_directory = save_directory
        self.temp_directory = temp_directory
        self.is_recording = False
        self.video_writer = None
        self.video_filename = None

        if not cv2.VideoCapture(self.camera_index).isOpened():
            raise Exception("Camera not found. Make sure the camera is connected.")

        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

        if not os.path.exists(self.temp_directory):
            os.makedirs(self.temp_directory)

    def create_video_file(self):
        self.video_filename = os.path.join(self.temp_directory, f"video_{datetime.now().strftime('%Y%m%d%H%M%S')}.avi")
        self.video_writer = cv2.VideoWriter(
            self.video_filename,
            cv2.VideoWriter_fourcc(*'XVID'),
            20.0,
            (640, 480)
        )

    def start_recording(self):
        self.is_recording = True
        cap = cv2.VideoCapture(self.camera_index)

        self.create_video_file()

        start_time = time.time()
        while self.is_recording and time.time() - start_time < 3600:  # Record for an hour
            ret, frame = cap.read()
            if not ret:
                break

            self.video_writer.write(frame)

        cap.release()

    def stop_recording(self):
        self.is_recording = False

        if self.video_writer is not None:
            self.video_writer.release()

            # Move the file to the final directory
            final_filename = os.path.join(self.save_directory, os.path.basename(self.video_filename))
            shutil.move(self.video_filename, final_filename)

            print(f"Video saved locally: {final_filename}")

if __name__ == "__main__":
    recorder = VideoRecorder(camera_index=0, save_directory='local_videos', temp_directory='temp_videos')

    try:
        while True:
            # Start recording for an hour
            recorder.start_recording()

            # Wait for an hour
            time.sleep(3600)

            # Stop recording
            recorder.stop_recording()

    except KeyboardInterrupt:
        # Stop recording if interrupted by keyboard (Ctrl+C)
        recorder.stop_recording()

    finally:
        cv2.destroyAllWindows()
