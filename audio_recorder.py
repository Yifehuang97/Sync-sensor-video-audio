import os
import pyaudio
import wave
import threading
import time
from socket_utils import get_current_timestamp
import logging


class AudioRecorder():

    # Audio class based on pyAudio and Wave
    def __init__(self,
                 save_path,
                 logger):

        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        self.logger = logger
        self.audio_save_path = os.path.join(save_path, 'audio.wav')
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []


    # Audio starts being recorded
    def record(self, end_status):

        self.stream.start_stream()
        frame_index = 0
        time_stamp = get_current_timestamp()
        print("Audio recording start.")
        self.logger.info("Audio recorder start recording: " + str(time_stamp))
        while True:
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
            ts = get_current_timestamp()
            frame_index += 1
            is_end = end_status[-1]
            if is_end:
                break
        time_stamp = get_current_timestamp()
        self.logger.info("Audio recorder end recording: " + str(time_stamp))
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        waveFile = wave.open(self.audio_save_path, 'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.audio.get_sample_size(self.format))
        waveFile.setframerate(self.rate)
        waveFile.writeframes(b''.join(self.audio_frames))
        waveFile.close()
        print("Audio recording end.")


    # Launches the audio recording function using a thread
    def start(self, end_status):
        audio_thread = threading.Thread(target=self.record, args=(end_status, ))
        audio_thread.start()



