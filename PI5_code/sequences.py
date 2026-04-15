from utils import Offsetter, lean, move_leg
from inverse_kinematics import SpiderLeg
from inverse_kinematics import plot_base, plot_leg, spider_show
from math import cos, sin, pi as PI, sqrt, radians
from copy import deepcopy

class SequenceManager:
    def __init__(self):
        self.robot_base = (160, 160) 
        self.offset = Offsetter(self.robot_base)

        self.robot_legs = [
                SpiderLeg("Leg1", COXA=60.5, FEMUR=96.3, TIBIA=113.5),
                SpiderLeg("Leg2", COXA=60.5, FEMUR=96.3, TIBIA=113.5),
                SpiderLeg("Leg3", COXA=60.5, FEMUR=96.3, TIBIA=113.5),
                SpiderLeg("Leg4", COXA=60.5, FEMUR=96.3, TIBIA=113.5)
        ]

        self.start_position = [
                [ 90,  90, 0],
                [ 90, -90, 0],
                [-90,  90, 0],
                [-90, -90, 0] 
            ]
        self.normal_position = [
                [ 90,  90, -95],
                [ 90, -90, -95],
                [-90,  90, -95],
                [-90, -90, -95] 
            ]
        self.current_pos = deepcopy(self.normal_position)

        self.dict_object = {
            "stand_up"     : { "commands" : [], "frames" : [], "delay" : 0.01 },
            "sit_down"     : { "commands" : [], "frames" : [], "delay" : 0.01 },
            "walk_forward" : { "commands" : [], "frames" : [], "delay" : 0.1  },
            "turn_left"    : { "commands" : [], "frames" : [], "delay" : 0.25 },
            "turn_right"   : { "commands" : [], "frames" : [], "delay" : 0.25 },
            "fast_walk_forward" : { "commands" : [], "frames" : [], "delay" : 0.1  },
            "fast_turn_left"    : { "commands" : [], "frames" : [], "delay" : 0.25 },
            "fast_turn_right"   : { "commands" : [], "frames" : [], "delay" : 0.25 }
        }   

    # computing angles based on a position (from sequences)
    def _compute_angles(self, position : list[list[float]]) -> tuple[str, list[list[float]]]:

        resulted_command = "set_angles "
        resulted_positions = []
        for i in range(4):
            angles, joint_positions = self.robot_legs[i].compute_angles(position[i])
            resulted_positions.append(self.offset.apply_offset_JP(joint_positions, i))
            resulted_command += f"{int(angles[0])}:{int(angles[1])}:{int(angles[2])}:"

        return resulted_command[:-1], resulted_positions

    # creating frames from positions
    def _create_frame_from_positions(self, legs_positions : list[list[float]]):
        for i, pos in enumerate(legs_positions):
            plot_leg(pos, i)
        plot_base(*self.robot_base)
        frame = spider_show()
        return frame

    # Spider leg numbering
    # \         /
    #  3       1
    #   \     /
    #    +-o-+
    #    |   |
    #    +---+
    #   /     \
    #  4       2
    # /         \
    def _create_walk_forward_sequence(self, target_Y):

        target_Y /= 2
        walk = [
            deepcopy(self.normal_position),    
        ]
        # lean forward
        walk.append(lean(self.normal_position, 0, target_Y))

        # move legs
        for moved_leg, opposite_leg in zip([2, 4, 1, 3], [3, 1, 4, 2]):
            walk.append(move_leg(walk[-1], leg_no=opposite_leg, x=0, y=0, z=60))

            walk.append(move_leg(walk[-1], leg_no=moved_leg, x=0, y=target_Y, z=50))
            walk.append(move_leg(walk[-1], leg_no=moved_leg, x=0, y=target_Y, z=-50)) 

            walk.append(move_leg(walk[-1], leg_no=opposite_leg, x=0, y=0, z=-60))

        # lean forward again
        walk.append(lean(walk[-1], 0, target_Y))
        return walk

    def _create_turning_sequence(self, target_angle):
        
        if target_angle < 0: # turning right
            leg_order = zip(
                [1,    2,  4,   3], # leg
                [4,    3,  1,   2], # oposite leg
                [45, -45, 45, -45], # start angle
                [1,    1, -1,  -1]  # sign
            )
        elif target_angle > 0: # turning left
            leg_order = zip(
                [1,    3,  4,   2], # leg
                [4,    2,  1,   3], # oposite leg 
                [45, -45, 45, -45], # start angle 
                [1,   -1, -1,   1]  # sign 
            )

        seq = [
            deepcopy(self.normal_position)
        ]
        for leg, opposite_leg, start_angle, sign in leg_order:
            # lift one leg
            aux = deepcopy(seq[-1])
            
            new_x = sign * 90*sqrt(2) * cos(radians(target_angle/2 + start_angle))
            new_y = sign * 90*sqrt(2) * sin(radians(target_angle/2 + start_angle))
            aux[leg-1] = [new_x, new_y, -45]
            aux[opposite_leg-1][2] = -35
            
            seq.append(aux)

            # put down one leg
            aux = deepcopy(seq[-1])
            
            new_x = sign * 90*sqrt(2) * cos(radians(target_angle + start_angle))
            new_y = sign * 90*sqrt(2) * sin(radians(target_angle + start_angle))
            aux[leg-1] = [new_x, new_y, -95]
            aux[opposite_leg-1][2] = -95

            
            seq.append(aux)

        seq.append(deepcopy(self.normal_position))
        return seq

    # ====================================
    # sequences
    # ====================================

    def generate(self):

        stand_up = [
            lean(self.normal_position, 0, 0, -95),
            lean(self.normal_position, 0, 0, -90),
            lean(self.normal_position, 0, 0, -80),
            lean(self.normal_position, 0, 0, -70),
            lean(self.normal_position, 0, 0, -60),
            lean(self.normal_position, 0, 0, -50),
            lean(self.normal_position, 0, 0, -40),
            lean(self.normal_position, 0, 0, -30),
            lean(self.normal_position, 0, 0, -20),
            lean(self.normal_position, 0, 0, -10),
            deepcopy(self.normal_position)
        ]
        
        sit_down = [
            deepcopy(self.normal_position),
            lean(self.normal_position, 0, 0, -10),
            lean(self.normal_position, 0, 0, -20),
            lean(self.normal_position, 0, 0, -30),
            lean(self.normal_position, 0, 0, -40),
            lean(self.normal_position, 0, 0, -50),
            lean(self.normal_position, 0, 0, -60),
            lean(self.normal_position, 0, 0, -70),
            lean(self.normal_position, 0, 0, -80),
            lean(self.normal_position, 0, 0, -90),
            lean(self.normal_position, 0, 0, -95)
        ]

        walk_forward = self._create_walk_forward_sequence(75)
        fast_walk_forward = self._create_walk_forward_sequence(150)

        turn_left = self._create_turning_sequence(30)
        turn_right = self._create_turning_sequence(-30)

        fast_turn_left  = self._create_turning_sequence(50)
        fast_turn_right = self._create_turning_sequence(-50)

        for key, seq in zip(
            ["stand_up", "sit_down", "walk_forward", "turn_left", "turn_right", "fast_walk_forward", "fast_turn_left", "fast_turn_right"],
            [ stand_up ,  sit_down ,  walk_forward,   turn_left,   turn_right,   fast_walk_forward,   fast_turn_left,   fast_turn_right ]
        ):
            for pos in seq:
                command, joints_coords = self._compute_angles(pos)
                frame = self._create_frame_from_positions(joints_coords)
                self.dict_object[key]["commands"].append(command)
                self.dict_object[key]["frames"  ].append(frame)

    def __getitem__(self, key):
        return self.dict_object[key]
