import ujson
import time
import socket
import sys
import select

from servo import Servo
from machine import Pin, PWM, I2C
from mpu6500 import MPU6500, SF_G, SF_DEG_S

with open("./config.json", 'r') as f:
    parameters = ujson.load(f)

# Servos
servos = [Servo(parameters["servo"][i]) for i in range(12)]

while True:
    command = input("Command: ")
    if command == "exit":
        break
    else:
        com_w_args = command.split(" ")
        if com_w_args[0] == "set": 
            index = int(com_w_args[1])
            angle = int(com_w_args[2])
            servos[index].set_degree(angle)
            print("Servo", index, "set to", angle)
        if com_w_args[0] == "max":
            index = int(com_w_args[1])
            angle = int(com_w_args[2])
            parameters["servo"][index]["max_angle"] = angle
            print("Servo", index, "max angle set to", angle)
        if com_w_args[0] == "min":
            index = int(com_w_args[1])
            angle = int(com_w_args[2])
            parameters["servo"][index]["min_angle"] = angle
            print("Servo", index, "min angle set to", angle)
        if com_w_args[0] == "ofs":
            index = int(com_w_args[1])
            angle = int(com_w_args[2])
            parameters["servo"][index]["offset"] = angle
            print("Servo", index, "offset set to", angle)
        if com_w_args[0] == "save":
            with open("./config.json", 'w') as f:
                ujson.dump(parameters, f)
            print("Config saved")