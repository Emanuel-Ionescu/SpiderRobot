
def POSITION(l1 : list[int], l2 : list[int], l3 : list[int], l4 : list[int]) -> list[int]:
    return [sum(x) for x in zip(l1, l2, l3, l4)]

# standing
LEG1_STAND = [0, 0, 0] * 0 + [0, -40, 20] + [0, 0, 0] * 3
LEG2_STAND = [0, 0, 0] * 1 + [0, -40, 15] + [0, 0, 0] * 2
LEG3_STAND = [0, 0, 0] * 2 + [0, -40, 15] + [0, 0, 0] * 1
LEG4_STAND = [0, 0, 0] * 3 + [0, -40, 10] + [0, 0, 0] * 0
STAND_POSITION = POSITION(
    LEG1_STAND, 
    LEG2_STAND, 
    LEG3_STAND, 
    LEG4_STAND
)

# leg lifted
LEG1_LIFTED = [0, 0, 0] * 0 + [0, 40,  80] + [0, 0, 0] * 3
LEG2_LIFTED = [0, 0, 0] * 1 + [0, 40,  80] + [0, 0, 0] * 2
LEG3_LIFTED = [0, 0, 0] * 2 + [0, 40,  80] + [0, 0, 0] * 1
LEG4_LIFTED = [0, 0, 0] * 3 + [0, 40,  80] + [0, 0, 0] * 0
LIFTED_LEGS_POSITION = POSITION(
    LEG1_LIFTED, 
    LEG2_LIFTED, 
    LEG3_LIFTED, 
    LEG4_LIFTED
)

# leg lifted at an angle

# leg lifted forward
LEG1_LIFTED_FORWARD = [0, 0, 0] * 0 + [-45, 40,  80] + [0, 0, 0] * 3
LEG2_LIFTED_FORWARD = [0, 0, 0] * 1 + [ 45, 40,  80] + [0, 0, 0] * 2
LEG3_LIFTED_FORWARD = [0, 0, 0] * 2 + [ 45, 40,  80] + [0, 0, 0] * 1
LEG4_LIFTED_FORWARD = [0, 0, 0] * 3 + [-45, 40,  80] + [0, 0, 0] * 0

# leg lifted backward
LEG1_LIFTED_BACKWARD = [0, 0, 0] * 0 + [ 45, 40,  80] + [0, 0, 0] * 3
LEG2_LIFTED_BACKWARD = [0, 0, 0] * 1 + [-45, 40,  80] + [0, 0, 0] * 2
LEG3_LIFTED_BACKWARD = [0, 0, 0] * 2 + [-45, 40,  80] + [0, 0, 0] * 1
LEG4_LIFTED_BACKWARD = [0, 0, 0] * 3 + [ 45, 40,  80] + [0, 0, 0] * 0

# leg standing at an angle

# leg standing forward
LEG1_STAND_FORWARD = [0, 0, 0] * 0 + [-45, -40, 20] + [0, 0, 0] * 3
LEG2_STAND_FORWARD = [0, 0, 0] * 1 + [ 45, -40, 15] + [0, 0, 0] * 2
LEG3_STAND_FORWARD = [0, 0, 0] * 2 + [ 45, -40, 15] + [0, 0, 0] * 1
LEG4_STAND_FORWARD = [0, 0, 0] * 3 + [-45, -40, 10] + [0, 0, 0] * 0

# leg standing backward
LEG1_STAND_BACKWARD = [0, 0, 0] * 0 + [ 45, -40, 20] + [0, 0, 0] * 3
LEG2_STAND_BACKWARD = [0, 0, 0] * 1 + [-45, -40, 15] + [0, 0, 0] * 2
LEG3_STAND_BACKWARD = [0, 0, 0] * 2 + [-45, -40, 15] + [0, 0, 0] * 1
LEG4_STAND_BACKWARD = [0, 0, 0] * 3 + [ 45, -40, 10] + [0, 0, 0] * 0