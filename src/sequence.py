from typing import Any
import json

#
# Objects definitions
#

class StepBase:
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        ...

class Delay(StepBase):
    def __init__(self, secs : float) -> None:
        self.description = secs

    def __float__(self)  -> float:
        return float(self.description) 

class Move(StepBase):
    def __init__(self, move_description : dict) -> None:
        self.description = move_description

    def __bytes__(self) -> bytes:
        return json.dumps(self.description).encode()
    
    def __str__(self) -> str:
        return json.dumps(self.description)

class FullMove(StepBase):
    def __init__(self, move_description : list, step_time : float = 1) -> None:
        self.description = {}
        self.description["step_time"] = step_time
        if len(move_description) == 12:
            index = 0
            for leg in ["L1", "L2", "L3", "L4"]:
                self.description[leg] = {}
                for piece in ["1", "2", "3"]:
                    self.description[leg][piece] = move_description[index]
                    index += 1
             
    def __bytes__(self) -> bytes:
        return json.dumps(self.description).encode()
    
    def __str__(self) -> str:
        return json.dumps(self.description)

class Sequence:
    def __init__(self, delay_between_steps : float = 0) -> None:
        self.steps = []
        self.between_steps_time = delay_between_steps
        self.length = 0
        self.internal_index = 0

    def addStep(self, step : Move | FullMove | Delay ) -> None:
        self.steps.append(step)
        self.length += 1
        if self.between_steps_time > 0:
            self.length += 1
            self.steps.append(Delay(self.between_steps_time))

    def getStep(self, idx : int = -1) -> Move | Delay:
        if idx > -1:
            idx %= self.length
            self.internal_index = idx

        res = self.steps[self.internal_index]
        self.internal_index = (self.internal_index + 1) % self.length 
        return res

#==================================================================
#
# "Constants" moves and sequences
#
#==================================================================

from leg_positions import *

#==================================================================
#
# PushUPs 
#
#==================================================================

PushupSequence = Sequence(1)
PushupSequence.addStep(FullMove(STAND_POSITION))
PushupSequence.addStep(FullMove(LIFTED_LEGS_POSITION))
PushupSequence.addStep(FullMove(STAND_POSITION))
PushupSequence.addStep(FullMove(LIFTED_LEGS_POSITION))

#==================================================================
#
# Walking Forward
#
#==================================================================
WalkForwardSequence = Sequence(1)
WalkForwardSequence.addStep(FullMove(STAND_POSITION))

# first physical step
WalkForwardSequence.addStep(
    FullMove(
        POSITION(LEG1_STAND, LEG2_STAND, LEG3_LIFTED_FORWARD, LEG4_STAND)
    ))
WalkForwardSequence.addStep(
    FullMove(
        POSITION(LEG1_STAND, LEG2_STAND, LEG3_STAND_FORWARD, LEG4_STAND)
    ))

# second physical step
WalkForwardSequence.addStep(
    FullMove(
        POSITION(LEG1_LIFTED_FORWARD, LEG2_STAND, LEG3_STAND_FORWARD, LEG4_STAND)
    ))
WalkForwardSequence.addStep(
    FullMove(
        POSITION(LEG1_STAND_FORWARD, LEG2_STAND, LEG3_STAND_FORWARD, LEG4_STAND)
    ))

# third physical step
WalkForwardSequence.addStep(
    FullMove(
        POSITION(LEG1_STAND_FORWARD, LEG2_LIFTED_FORWARD, LEG3_STAND_FORWARD, LEG4_STAND)
    ))
WalkForwardSequence.addStep(
    FullMove(
        POSITION(LEG1_STAND_FORWARD, LEG2_STAND_FORWARD, LEG3_STAND_FORWARD, LEG4_STAND)
    ))

# third physical step
WalkForwardSequence.addStep(
    FullMove(
        POSITION(LEG1_STAND_FORWARD, LEG2_STAND_FORWARD, LEG3_STAND_FORWARD, LEG4_LIFTED_FORWARD)
    ))
WalkForwardSequence.addStep(
    FullMove(
        POSITION(LEG1_STAND_FORWARD, LEG2_STAND_FORWARD, LEG3_STAND_FORWARD, LEG4_STAND_FORWARD)
    ))

# return to standing position
WalkForwardSequence.addStep(FullMove(STAND_POSITION))

