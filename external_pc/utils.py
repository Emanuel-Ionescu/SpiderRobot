from copy import deepcopy
import math
import numpy as np
import socket
import serial
import time
import cv2 
import psutil
import os

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
