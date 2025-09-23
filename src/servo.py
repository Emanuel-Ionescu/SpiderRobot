from machine import PWM

class Servo:
    def __init__(self, idx : int, pwm_pin : PWM,  min_percent : float, max_percent : float, positions : list[float]) -> None:
        self.ID = idx
        self.MAX = max_percent
        self.MIN = min_percent
        self.POS = 0 # in pencent
        self.PWM_PIN = pwm_pin
        self.POSITIONS = positions

        self.PWM_PIN.freq(50)
        
    def __get_duty_from_percent(self, percent : float) -> int:
        return int(percent/100 *2**16)
    
    def set_position(self, pos : float) -> None:
        self.PWM_PIN.duty_u16(self.__get_duty_from_percent(pos))
        self.POS = pos
        
        
    