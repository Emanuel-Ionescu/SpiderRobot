from machine import PWM

class Servo:
    def __init__(self, configuration : dict, PWM_PIN : PWM) -> None:
        self.idx    = configuration["id"]
        self.max    = configuration["max_percent"]
        self.min    = configuration["min_percent"]
        self.pos    = configuration["start_deg"]
        self.offset = configuration["offset"]
        self.pwm_pin = PWM_PIN

        self.pwm_pin.freq(50)
        
        #power the servo 
        self.set_degree(self.pos)
        
    def __get_duty_from_percent(self, percent : float) -> int:
        percent = max(0, min(percent, 100))
        return int(percent/100 *2**16)
    
    def __get_duty_from_degree(self, degree: int) -> int:
        degree = max(-90, min(degree, 90))
        percent = (degree + 90)/180 * (self.max - self.min) + self.min # scale the degree into operating interval
        return self.__get_duty_from_percent(percent)

    def set_position(self, pos_percent : float) -> None:
        self.pwm_pin.duty_u16(self.__get_duty_from_percent(pos_percent))
        
    def set_degree(self, deg : int) -> None:
        deg -= self.offset
        self.pwm_pin.duty_u16(self.__get_duty_from_degree(deg))
        self.pos = deg    

    