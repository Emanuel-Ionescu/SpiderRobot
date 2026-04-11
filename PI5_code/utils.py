from copy import deepcopy
import math
import numpy as np
import socket
import serial
import time
import cv2 
import psutil
import os

blank = np.zeros((30, 1280, 3), dtype=np.uint8)

def timer(func):

    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        end = time.time()-t1
        print(f"{func.__name__} took {end} seconds")
        return result
    return wrapper

def get_htop():
    # get each core usage
    cpu_usage = psutil.cpu_percent(interval=0.1, percpu=True)
    
    # get memory usage
    memory_usage = psutil.virtual_memory().percent
    
    # get temperature
    temp = os.popen("vcgencmd measure_temp").read().strip()
    temp = temp.split("=")[1]

    frame = blank.copy()
    
    cv2.putText(frame, "CPU: {}% {}% {}% {}%".format(*cpu_usage), (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(frame, "Memory: {}%".format(memory_usage), (600, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(frame, "Temperature: " + str(temp), (1100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return frame

OFFSET = None

class Offsetter:
    
    def __init__(self, offset : tuple):
        self.offset = (offset[0]/2, offset[1]/2)
            
    def apply_offset(self, position : list[list[float]]):
        return [
            [position[0][0] + self.offset[0], position[0][1] + self.offset[1], position[0][2]],
            [position[1][0] + self.offset[0], position[1][1] - self.offset[1], position[1][2]],
            [position[2][0] - self.offset[0], position[2][1] + self.offset[1], position[2][2]],
            [position[3][0] - self.offset[0], position[3][1] - self.offset[1], position[3][2]] 
        ]

    def remove_offset(self, position : list[list[float]]):
        return [
            [position[0][0] - self.offset[0], position[0][1] - self.offset[1], position[0][2]],   
            [position[1][0] - self.offset[0], position[1][1] + self.offset[1], position[1][2]],   
            [position[2][0] + self.offset[0], position[2][1] - self.offset[1], position[2][2]],               
            [position[3][0] + self.offset[0], position[3][1] + self.offset[1], position[3][2]]    
        ]
        
    def apply_offset_JP(self, joint_position: list[list[float]], num):
        if num == 0:
            for i in range(4):
                joint_position[i][0] += self.offset[0]
                joint_position[i][1] += self.offset[1]
        if num == 1:
            for i in range(4):
                joint_position[i][0] += self.offset[0]
                joint_position[i][1] -= self.offset[1]
        if num == 2:
            for i in range(4):
                joint_position[i][0] -= self.offset[0]
                joint_position[i][1] += self.offset[1]
        if num == 3:
            for i in range(4):
                joint_position[i][0] -= self.offset[0]
                joint_position[i][1] -= self.offset[1]
        return joint_position
    
def apply_function(position : list[list[float]], fun1, fun2, fun3, fun4):
    pass

def lean(position : list[list[float]], x: float, y : float, z : float = 0):
    position_copy = deepcopy(position)
    for pos in position_copy:
        pos[0] -= x
        pos[1] -= y
        pos[2] -= z

    return position_copy

def move_leg(position : list[list[float]], leg_no : int, x : float, y : float, z : float):
    position_copy = deepcopy(position)
    position_copy[leg_no - 1][0] += x
    position_copy[leg_no - 1][1] += y
    position_copy[leg_no - 1][2] += z
    return position_copy


class SerialClient:

    def __init__(self, port : str, baud_rate : int = 115200):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
        self.ser.flush()
        time.sleep(2)
    
    def __call__(self, data : str):
        self.ser.write((data + '\n').encode('utf-8'))
        line = self.ser.readline().decode('utf-8', errors='replace').rstrip()
        if line:
            return line
        else:
            return "TIMEOUT"

class DummySerialClient:

    def __init__(self):
        pass
    
    def __call__(self, data : str):
        return "Dummy response!"