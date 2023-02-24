import os
import cv2
import json
import threading
from socket_utils import get_current_timestamp


class VideoRecorder():
    def __init__(self,
                 save_path,
                 logger,
                 device_index=0,
                 video_width=1280,
                 video_height=720,
                 ):
        self.video_save_path = os.path.join(save_path, 'video.avi')
        self.dict_save_path = os.path.join(save_path, "frame_timestamp_mapping.json")
        self.device_index = device_index
        self.logger = logger
        self.video_cap = cv2.VideoCapture(self.device_index)
        self.fps = int(self.video_cap.get(5))
        self.video_width = video_width
        self.video_height = video_height
        self.video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.video_out = cv2.VideoWriter(self.video_save_path,
                                         cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                         self.fps,
                                         (self.video_width, self.video_height))
        self.frame_timestamp_mapping_dict = {}
        try:
            _, _ = self.video_cap.read()
        except RuntimeError:
            print("Error: Fail to read frame from camera.")
            self.logger.error("Fail to read frame from camera.")

    def record(self, end_status):
        frame_index = 0
        while True:
            frame_index += 1
            ret, video_frame = self.video_cap.read()
            if ret:
                time_stamp = get_current_timestamp()
                self.frame_timestamp_mapping_dict[frame_index] = time_stamp
                self.video_out.write(video_frame)
                if frame_index == 1:
                    self.logger.info("Video recorder start video recording: " + str(time_stamp))
            is_end = end_status[-1]
            if is_end:
                break
        time_stamp = get_current_timestamp()
        self.logger.info("Video recorder end video recording: " + str(time_stamp))
        self.video_out.release()
        self.video_cap.release()
        cv2.destroyAllWindows()
        # Save the dict
        print(len(self.frame_timestamp_mapping_dict))
        with open(self.dict_save_path, "w") as outfile:
            json.dump(self.frame_timestamp_mapping_dict, outfile)

    def start(self, end_status):
        video_thread = threading.Thread(target=self.record, args=(end_status, ))
        video_thread.start()


