import cv2
import threading
import jpysocket
import numpy as np
from socket import *
import time


def get_current_timestamp():
    time_stamp = time.time()
    time_stamp = (np.around(time_stamp, 3) * 1000).astype(np.int64).item()
    return time_stamp


def estimate_offset(host, port, result_dict, logger):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print("Waiting for the wearOS device to estimate the network offset......")
    connection, address = s.accept()
    # Receive the first wearOS timestamp from wearOS
    wearos_timestamp_1 = connection.recv(1024)
    wearos_timestamp_1 = jpysocket.jpydecode(wearos_timestamp_1)
    result_dict['OFFSET_wearos_timestamp_1'] = wearos_timestamp_1
    logger.info("[Offset estimation]Received wearOS's first timestamp: " + str(wearos_timestamp_1))
    # Send the first PC timestamp to wearOS
    pc_time_stamp_1 = get_current_timestamp()
    pc_time_stamp_1_encode = jpysocket.jpyencode(str(pc_time_stamp_1))
    logger.info("[Offset estimation]Send PC's first timestamp: " + str(pc_time_stamp_1))
    connection.send(pc_time_stamp_1_encode)
    result_dict['OFFSET_pc_timestamp_1'] = pc_time_stamp_1
    # Receive the second wearOS timestamp from wearOS
    wearos_timestamp_2 = connection.recv(1024)
    wearos_timestamp_2 = jpysocket.jpydecode(wearos_timestamp_2)
    logger.info("[Offset estimation]Received wearOS's second timestamp: " + str(wearos_timestamp_2))
    result_dict['OFFSET_wearos_timestamp_2'] = wearos_timestamp_2
    # Send the second PC timestamp to wearOS
    pc_time_stamp_2 = get_current_timestamp()
    pc_time_stamp_2_encode = jpysocket.jpyencode(str(pc_time_stamp_2))
    logger.info("[Offset estimation]Send PC's second timestamp: " + str(pc_time_stamp_2))
    connection.send(pc_time_stamp_2_encode)
    result_dict['OFFSET_pc_time_stamp_2'] = pc_time_stamp_2
    s.close()
    print("Finished offset estimation.")
    return result_dict


def receive_start_recording_msg(host, port, result_dict, logger):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print("Waiting for the start recording message from wearOS......")
    connection, address = s.accept()
    # Receive the start timestamp of wearOS
    wearos_start_timestamp = connection.recv(1024)
    wearos_start_timestamp = jpysocket.jpydecode(wearos_start_timestamp)
    result_dict['START_wearos_start_timestamp'] = wearos_start_timestamp
    logger.info("[Start recording]Received wearOS's start recording timestamp: " + str(wearos_start_timestamp))
    # Receive the start timestamp of PC
    pc_start_timestamp = get_current_timestamp()
    pc_start_timestamp_encode = jpysocket.jpyencode(str(pc_start_timestamp))
    logger.info("[Start recording]Send PC's start recording timestamp: " + str(pc_start_timestamp))
    connection.send(pc_start_timestamp_encode)
    result_dict['START_pc_start_timestamp'] = pc_start_timestamp
    print("Have received the start recording message from wearOS.")
    s.close()
    return result_dict


def wait_for_end_msg(host, port, end_status):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    connection, address = s.accept()
    msg = connection.recv(1024)
    msg = jpysocket.jpydecode(msg)
    s.close()
    end_status.append(True)
