from machine import PWM

class Servo:
    def __init__(self, configuration : dict) -> None:
        self.m = configuration["m"]
        self.b = configuration["b"]
        self.max_duty = configuration["max_duty"]
        self.min_duty = configuration["min_duty"]
        self.max_ang = configuration["max_angle"]
        self.min_ang = configuration["min_angle"]
        
        self.pwm_pin = PWM(configuration["pin"])
        self.pwm_pin.freq(50)
        
        #power the servo 
        self.set_degree(0)

    def set_degree(self, deg : int) -> None:
        deg = max(self.min_ang, min(deg, self.max_ang))
        #deg = duty * m + b => deg - b = duty * m => duty = (deg - b)/m
        percent_duty = (deg - self.b)/self.m
        percent_duty = max(self.min_duty, min(percent_duty, self.max_duty))
        self.pwm_pin.duty_u16(int(percent_duty/100 *2**16))
        self.pos = deg

    