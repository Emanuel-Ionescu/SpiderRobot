from utils import Offsetter, lean, move_leg
from math import cos, pi as PI
from copy import deepcopy

OFFSET = Offsetter((160, 160))

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

'''
Stand up/down animation
'''
stand_up = [
    lean(normal_position, 0, 0, -95),
    lean(normal_position, 0, 0, -90),
    lean(normal_position, 0, 0, -80),
    lean(normal_position, 0, 0, -70),
    lean(normal_position, 0, 0, -60),
    lean(normal_position, 0, 0, -50),
    lean(normal_position, 0, 0, -40),
    lean(normal_position, 0, 0, -30),
    lean(normal_position, 0, 0, -20),
    lean(normal_position, 0, 0, -10),
    deepcopy(normal_position)
]

sit_down = [
    deepcopy(normal_position),
    lean(normal_position, 0, 0, -10),
    lean(normal_position, 0, 0, -20),
    lean(normal_position, 0, 0, -30),
    lean(normal_position, 0, 0, -40),
    lean(normal_position, 0, 0, -50),
    lean(normal_position, 0, 0, -60),
    lean(normal_position, 0, 0, -70),
    lean(normal_position, 0, 0, -80),
    lean(normal_position, 0, 0, -90),
    lean(normal_position, 0, 0, -95)
]

'''
Walking animation
'''

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


def create_walk_sequence(target_Y):

    target_Y /= 2

    walk = [
        deepcopy(normal_position),    
    ]
    # lean forward
    
    # for loops for slower movement
    # for i in range(1, 6):
    #     walk.append(lean(normal_position, 0, i*target_Y/5))
    walk.append(lean(normal_position, 0, target_Y))

    # move legs
    for moved_leg, opposite_leg in zip([2, 4, 1, 3], [3, 1, 4, 2]):
        walk.append(move_leg(walk[-1], leg_no=opposite_leg, x=0, y=0, z=60))

        walk.append(move_leg(walk[-1], leg_no=moved_leg, x=0, y=target_Y, z=50))
        walk.append(move_leg(walk[-1], leg_no=moved_leg, x=0, y=target_Y, z=-50)) 

        walk.append(move_leg(walk[-1], leg_no=opposite_leg, x=0, y=0, z=-60))


    walk.append(lean(walk[-1], 0, target_Y))

    return walk

walk = create_walk_sequence(150)
