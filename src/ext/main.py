import argparse
parser = argparse.ArgumentParser(
                    prog='SpiderBrain',
                    description='Computes the spider moves',
                    epilog='')

parser.add_argument('-p', '--plot', action='store_true', help='Plots the spider')
parser.add_argument('-s', '--simulate', action='store_true', help='Sends the data to the simulator')
parser.add_argument('-r', '--real', action='store_true', help='Sends the data to the real robot')
parser.add_argument('--serial', type=str, default="/dev/ttyS7", help='Pico Serial Port')
args = parser.parse_args()

import numpy as np
from copy import deepcopy
from math import cos, sin, radians, pi as PI
import time
from utils import Offsetter, lean, Client, SerialClient, move_leg
from spider_leg import SpiderLeg
if args.plot:
    from leg_plotter import plot_base, plot_leg, spider_show

'''
End of imports
'''

'''
Global variables
'''

LEGS = [
        SpiderLeg("Leg1", COXA=60.5, FEMUR=96.3, TIBIA=117.5),
        SpiderLeg("Leg2", COXA=60.5, FEMUR=96.3, TIBIA=117.5),
        SpiderLeg("Leg3", COXA=60.5, FEMUR=96.3, TIBIA=117.5),
        SpiderLeg("Leg4", COXA=60.5, FEMUR=96.3, TIBIA=117.5)
]

BASE = (160, 83.7) 
OFFSET = Offsetter(BASE)
SIMULATOR_SENDER = Client("localhost", 5005)
REAL_SENDER = SerialClient(args.serial)

'''
End of global variables

Helper functions
'''

def execute_position(position : list[list[float]]):
    global LEGS, BASE, OFFSET, SIMULATOR_SENDER, REAL_SENDER

    colors = ["blue", "red", "green", "orange"]
    if args.plot:
        plot_base(*BASE, "purple") # type: ignore

    to_send = ""
    aux = OFFSET.remove_offset(position)
    for i in range(4):
        angles, joint_positions = LEGS[i].compute_angles(aux[i])
        joint_position = OFFSET.apply_offset_JP(joint_positions, i)
        if args.plot:
            plot_leg(joint_positions, colors[i], i+1) # type: ignore

        to_send += f"{int(angles[0])}:{int(angles[1])}:{int(angles[2])}:"

    print("Angles:", to_send[:-1])

    if args.simulate:
        SIMULATOR_SENDER(to_send[:-1])
    if args.real:
        REAL_SENDER(to_send[:-1])

    if args.plot:
        a = spider_show(0.01) # type: ignore
        if a:
            exit()

'''
End of helper functions

MAIN Function
'''

def main():
    global OFFSET

    start_position = OFFSET.apply_offset([
        [ 90,  90, 0],
        [ 90, -90, 0],
        [-90,  90, 0],
        [-90, -90, 0] 
    ])

    normal_position = OFFSET.apply_offset([
        [ 90,  90, -95],
        [ 90, -90, -95],
        [-90,  90, -95],
        [-90, -90, -95] 
    ])

    current_pos = deepcopy(normal_position)

    standup_animation = [
        lean(normal_position, 0, 0, -95),
        deepcopy(normal_position)
    ]



    walking_animation = [start_position]
    # walking_animation.append(lean(walking_animation[-1], 40, 40))
    # walking_animation.append(move_leg(walking_animation[-1], 3, 80, 0, 40))
    # walking_animation.append(move_leg(walking_animation[-1], 3, 50, 0, -40))
    # for i in range(80):
    #     walking_animation.append(lean(walking_animation[-1], 0, -1))

    # for i in range(int((PI * 2) * 2)):
    #     walking_animation.append(lean(START_POSITION, cos(i/2)*50, 0))

    # first wake up
    # for step in standup_animation:
    #     time.sleep(0.1)
    #     if input() != "":
    #         exit()

    #     if args.plot:
    #         plot_base(*base, "purple") # type: ignore

    #     to_send = ""
    #     aux = offset.remove_offset(step)
    #     for i in range(4):
    #         angles, joint_positions = legs[i].compute_angles(aux[i])
    #         joint_position = offset.apply_offset_JP(joint_positions, i)
    #         if args.plot:
    #             plot_leg(joint_positions, colors[i], i+1) # type: ignore

    #         to_send += f"{int(angles[0])}:{int(angles[1])}:{int(angles[2])}:"

    #     if args.simulate:
    #         simulator_sender(to_send[:-1])
    #     if args.real:
    #         print("Sent:", to_send[:-1])
    #         real_sender(to_send[:-1])

    #     if args.plot:
    #         a = spider_show(0.01) # type: ignore
    #         if a:
    #             exit()

    REAL_SENDER(
        "20:0:0:" + 
        "-20:0:0:" + 
        "20:0:0:" + 
        "-20:0:0"
    )

    # iter = 0
    # while True:
    #     time.sleep(1.5)
    #     iter += 1
        
    #     execute_position(walking_animation[iter % len(walking_animation)])


if __name__ == "__main__":
    main()