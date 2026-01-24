import ujson
import time
import socket
import sys
import select

from servo import Servo
from machine import Pin, PWM, I2C
from mpu6500 import MPU6500, SF_G, SF_DEG_S

servos = []

def init():
    global servos
    with open("./config_old.json", 'r') as f:
        parameters_old = ujson.load(f)
    with open("./config.json", 'r') as f:
        parameters = ujson.load(f)
    servos = [Servo(parameters_old["servo"][i], parameters["servo"][i]) for i in range(12)]

def set_old(index, angle):
    global servos
    servos[index].set_degree_old(angle)
    print("Servo", index, "set to", angle)
    
def set(index, angle):
    global servos
    servos[index].set_degree(angle)
    print("Servo", index, "set to", angle)

def raw(index, percent):
    global servos
    print("Duty:", int(percent/100 *2**16))
    print("Percent:", f"{percent/100}%")
    servos[index].pwm_pin.duty_u16(int(percent/100 *2**16))
    print("Servo", index, "set to", percent, "%")

def identify(index):
    servos[index].set_degree(-3)
    time.sleep(0.5)
    servos[index].set_degree(3)
    time.sleep(0.5)
    servos[index].set_degree(0)
    
    
if __name__ == "__main__":
    #test old vs new
    init()
    for i in [6, 9]:
        dist = 5 if i in [0, 3, 6, 9] else 10
        print("\n\n")
        input("Press Enter to continue...")
        print("Servo", i)
        print("Old")
        set_old(i, dist)
        time.sleep(0.5)
        set_old(i, 0)
        time.sleep(0.5)
        print("\n")
        print("New")
        set(i, dist)
        time.sleep(0.5)
        set(i, 0)
        time.sleep(0.5)
        print("======================")
        
    
    