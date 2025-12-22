from utils import Offsetter, lean, move_leg
from math import cos, pi as PI
from copy import deepcopy

OFFSET = Offsetter((160, 83.7))

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
def create_walk_sequence(target_X):
    walk = [
        deepcopy(normal_position),    
    ]
    # lean forward
    aux_target = target_X + 30
    
    # for loops for slower movement
    # for i in range(1, 6):
    #     walk.append(lean(normal_position, i*aux_target/5, 0))
    walk.append(lean(normal_position, aux_target, 0))

    # move leg 3 forward
    walk.append(move_leg(walk[-1], 3, target_X, 0, 90))
    walk.append(move_leg(walk[-1], 3, target_X, 0, -90))

    # move leg 2 forward
    walk.append(move_leg(walk[-1], 2, target_X, 0, 90))
    walk.append(move_leg(walk[-1], 2, target_X, 0, -90))
    
    # lean a bit back
    # for i in range(1, 5):
    #     walk.append(lean(walk[-1], -10, 0)) 
    walk.append(lean(walk[-1], -40, 0))

    # move leg 1 forward
    walk.append(move_leg(walk[-1], 1, target_X, 0, 90))
    walk.append(move_leg(walk[-1], 1, target_X, 0, -90))
    
    # move leg 0 forward
    walk.append(move_leg(walk[-1], 0, target_X, 0, 90))
    walk.append(move_leg(walk[-1], 0, target_X, 0, -90))

    # forward
    aux_pos = walk[-1]
    aux_target = target_X + 10
    # for i in range(1, 6):
    #     walk.append(lean(aux_pos, i*aux_target/5, 0))
    walk.append(lean(aux_pos, aux_target, 0))

    walk.append(walk[-1])
    walk.append(walk[-1])

    return walk

walk = create_walk_sequence(20)

# walk.append(move_leg(walk[-1], 3, 50, -45, 50))
# walk.append(move_leg(walk[-1], 3, 50, 0, -50))
# #walk.append(lean(walk[-1], 50, 0))

# # walk.append(move_leg(walk[-1], 3, 100, 50, 50))
# # walk.append(move_leg(walk[-1], 3, 100, 0, -50))

# walk.append(deepcopy(normal_position))