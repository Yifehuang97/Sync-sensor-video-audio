import json
import os
import cv2
import threading
import jpysocket
from socket import *
import time
import numpy as np
from pympler.asizeof import asizeof
import logging
from video_recorder import VideoRecorder
from socket_utils import get_current_timestamp, estimate_offset, receive_start_recording_msg, wait_for_end_msg

import argparse
parser = argparse.ArgumentParser(description="Args for the event counting data collection python end.")
parser.add_argument('--name', required=True, type=str,
                    help="This name should be same as the name in the watch APP.")
parser.add_argument('--save_path', required=False, type=str, default='./',
                    help="Root save path of the python end's file.")
parser.add_argument('--host', required=False, type=str, default='130.245.68.71',
                    help="Ip address of the PC socket server.")
parser.add_argument('--port', required=False, type=int, default=8080,
                    help="Port of the PC socket server.")
args = parser.parse_args()
# Setting of data collection
ROOT_DIR = args.save_path
NAME = args.name
SAVE_DIR = os.path.join(ROOT_DIR, NAME)
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)
HOST = args.host
PORT = args.port
LOG_SAVE_PATH = os.path.join(SAVE_DIR, 'logging.log')
logging.basicConfig(filename=LOG_SAVE_PATH, encoding='utf-8', level=logging.DEBUG)
vid = VideoRecorder(SAVE_DIR, logging)
important_timestamp = {}
ts = get_current_timestamp()
estimate_offset(HOST, PORT, important_timestamp, logging)
receive_start_recording_msg(HOST, PORT, important_timestamp, logging)
status_q = list()
status_q.append(False)
# Start video recording thread
vid.start(status_q)
# Start end listening thread
t1 = threading.Thread(target=wait_for_end_msg, args=(HOST, PORT, status_q,))
t1.start()
with open(os.path.join(SAVE_DIR, "important_timestamp.json"), "w") as outfile:
    json.dump(important_timestamp, outfile)

