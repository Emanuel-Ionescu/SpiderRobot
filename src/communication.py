from machine import Pin, Timer, PWM, I2C
from mpu9250 import MPU9250
from mpu6500 import MPU6500, SF_G, SF_DEG_S
import time
import network
import socket

class Communication:
    """ Abstract Class """

    def send(self, arg):
        pass
    
    def recv(self):
        pass

class WiFi(Communication):
    
    def __init__(self, ssid, password):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(ssid, password)
        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)

        if self.wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = self.wlan.ifconfig()
            print( 'ip = ' + status[0] )

        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
