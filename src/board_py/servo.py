from machine import PWM

class Servo:
    def __init__(self, configuration : dict) -> None:
    # def __init__(self, old_configuration : dict, configuration : dict) -> None:
        # self.old_max     = old_configuration["max_percent"]
        # self.old_min     = old_configuration["min_percent"]
        # self.old_max_ang = old_configuration["max_angle"]
        # self.old_min_ang = old_configuration["min_angle"]
        # self.old_pos     = old_configuration["start_deg"]
        # self.old_offset  = old_configuration["offset"]
        # self.old_orient  = old_configuration["orientation"]

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
        #self.set_degree_old(self.old_pos)
        

    # def __get_duty_from_percent(self, percent : float) -> int:
    #     percent = max(0, min(percent, 100))
    #     return int(percent/100 *2**16)
    
    # def __get_duty_from_degree(self, degree: int) -> int:
    #     degree = max(-90, min(degree, 90))
    #     percent = (degree + 90)/180 * (self.old_max - self.old_min) + self.old_min # scale the degree into operating interval
    #     print("Duty:", percent, "%")
    #     return self.__get_duty_from_percent(percent)

    # def set_position(self, pos_percent : float) -> None:
    #     self.pwm_pin.duty_u16(self.__get_duty_from_percent(pos_percent))
        
    # def set_degree_old(self, deg : int) -> None:
    #     deg -= self.old_offset
    #     deg *= self.old_orient
    #     self.pwm_pin.duty_u16(self.__get_duty_from_degree(deg))
    #     self.old_pos = deg    

    def set_degree(self, deg : int) -> None:
        deg = max(self.min_ang, min(deg, self.max_ang))
        #deg = duty * m + b => deg - b = duty * m => duty = (deg - b)/m
        percent_duty = (deg - self.b)/self.m
        percent_duty = max(self.min_duty, min(percent_duty, self.max_duty))
        print("Duty:", percent_duty, "%")
        self.pwm_pin.duty_u16(int(percent_duty/100 *2**16))
        self.pos = deg

    