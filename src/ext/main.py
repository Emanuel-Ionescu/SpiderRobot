
import time
import numpy as np
import os
import sequences
import socket
import cv2
import importlib

from copy import deepcopy
from math import cos, sin, radians, pi as PI
from utils import Offsetter, lean, Client, SerialClient, move_leg, get_htop
from inverse_kinematics import SpiderLeg
from inverse_kinematics import plot_base, plot_leg, spider_show
from web_gui import run_server, set_frame_queue, app
from multiprocessing import Queue, Process
'''
End of imports
'''

'''
Global variables
'''

LEGS = [
        SpiderLeg("Leg1", COXA=60.5, FEMUR=96.3, TIBIA=113.5),
        SpiderLeg("Leg2", COXA=60.5, FEMUR=96.3, TIBIA=113.5),
        SpiderLeg("Leg3", COXA=60.5, FEMUR=96.3, TIBIA=113.5),
        SpiderLeg("Leg4", COXA=60.5, FEMUR=96.3, TIBIA=113.5)
]

BASE = (160, 83.7) 
OFFSET = Offsetter(BASE)
try:
    REAL_SENDER = SerialClient("/dev/ttyACM1")
    print("PICO found!")
except Exception as e:
    print("No PICO found: ", e)
    REAL_SENDER = None
# SIMULATOR_SENDER = Client("localhost", 5005)

'''
End of global variables

Helper functions
'''
def execute_position(position : list[list[float]], debug : bool = True):
    global LEGS, BASE, OFFSET, SIMULATOR_SENDER, REAL_SENDER

    to_send = "set_angles "
    aux = OFFSET.remove_offset(position)
    for i in range(4):
        angles, joint_positions = LEGS[i].compute_angles(aux[i])
        joint_position = OFFSET.apply_offset_JP(joint_positions, i)
        to_send += f"{int(angles[0])}:{int(angles[1])}:{int(angles[2])}:"

        plot_leg(joint_positions, i) 

    if debug:
        print("SENT:", to_send[:-1])

    if REAL_SENDER:
        response = REAL_SENDER(to_send[:-1])
        if debug:
            print("PICO:", response)

    plot_base(*BASE)
    frame = spider_show(0.01, draw=False)
    return frame

'''
End of helper functions

MAIN Function
'''

iter = 0
def main():
    global OFFSET

    frame_queue = Queue(maxsize=2)
    command_queue = Queue(maxsize=2)
    server_process = Process(target=run_server, args=(frame_queue, command_queue))
    server_process.start()

    htop_frame_queue = Queue(maxsize=1)
    htop_process = Process(target=run_htop, args=(htop_frame_queue,))
    htop_process.start()

    animation = None
    while True:
        if not command_queue.empty():
            command = command_queue.get()
            print("Command received: ", command)
            if command == "pause":
                animation = None
                importlib.reload(sequences)
            elif command == "stand_up":
                animation = sequences.stand_up
            elif command == "sit_down":
                animation = sequences.sit_down
            elif command == "walk":
                animation = sequences.walk

            iter = 0

        plot_frame = np.zeros((480, 1280, 3), dtype=np.uint8)
        if animation is not None:
            iter += 1
            plot_frame = execute_position(animation[iter], debug=True)
            if iter == len(animation) - 1:
                animation = None
                iter = 0
        else:
            iter = 0

        composed_frame = np.concatenate((plot_frame, get_htop()), axis=0)

        frame_queue.put(composed_frame)
        time.sleep(0.01)

if __name__ == "__main__":
    print("Welcome to the Spider Robot!")
    print("Starting the main loop...")
    main()