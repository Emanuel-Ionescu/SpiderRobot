from typing import Any
import json

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

StandUPSequence = Sequence()
StandUPSequence.addStep(Delay(1))
StandUPSequence.addStep(FullMove([0, 45, -135] * 4))
StandUPSequence.addStep(Delay(1))
StandUPSequence.addStep(FullMove([0,  0,  -90] * 4))

TestSequence = Sequence(1)
for leg in ["L1", "L2", "L3", "L4"]:
    TestSequence.addStep(Move({"step_time" : 1, leg : {"1" : 40}}))
    TestSequence.addStep(Move({"step_time" : 1, leg : {"2" : 40}}))
    TestSequence.addStep(Move({"step_time" : 1, leg : {"3" : 40}}))

    TestSequence.addStep(Move({"step_time" : 1, leg : {"1" : 0}}))
    TestSequence.addStep(Move({"step_time" : 1, leg : {"2" : 0}}))
    TestSequence.addStep(Move({"step_time" : 1, leg : {"3" : 0}}))

WalkForwardSequence = Sequence(0.2)
for leg in ["L1", "L2", "L3", "L4"]:
    WalkForwardSequence.addStep(Move({"step_time" : 0.2, leg : {"2" : -30}}))
    WalkForwardSequence.addStep(Move({"step_time" : 0.2, leg : {"1" : 60}}))
    WalkForwardSequence.addStep(Move({"step_time" : 0.2, leg : {"3" : 40}}))

for leg in ["L1", "L2", "L3", "L4"]:
    WalkForwardSequence.addStep(Move({"step_time" : 0.2, leg : {"2" : 0}}))
    WalkForwardSequence.addStep(Move({"step_time" : 0.2, leg : {"3" : -60}}))
    WalkForwardSequence.addStep(Move({"step_time" : 0.2, leg : {"1" : 0}}))
