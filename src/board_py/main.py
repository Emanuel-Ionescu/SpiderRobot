from machine import Pin, PWM, I2C
from mpu6500 import MPU6500, SF_G, SF_DEG_S
import ujson
import time
import socket
from servo import Servo

with open("./config.json", 'r') as f:
    parameters = ujson.load(f)

#
# Hardware declaration
#
class DummyMPU6500:
    acceleration = (0,0,0)
    gyro = (0,0,0)

# I2C
i2c1 = I2C(1, sda=Pin(18), scl=Pin(19))
print("Devices:", i2c1.scan())
if len(i2c1.scan()) == 0:
    mpu6500 = DummyMPU6500()
else:
    mpu6500 = MPU6500(i2c1, accel_sf=SF_G, gyro_sf=SF_DEG_S)

# LEDs
green_led = Pin("LED", Pin.OUT)
red_led = Pin(15, Pin.OUT)
blue_led = Pin(14, Pin.OUT)

blue_led.value(0)
red_led.value(1)

# Servos
servos = [Servo(parameters["servo"][i]) for i in range(12)]

green_led.value(1)

#
# WiFi
#
import network

ssid     = parameters["network"]["SSID"]
password = parameters["network"]["password"]

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    green_led.toggle()
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    red_led.value(1)
    for i in range(10000):
        green_led.toggle()
        red_led.toggle()
        time.sleep(0.3)
    raise RuntimeError('network connection failed')
else:
    red_led.value(0)
    blue_led.value(1)
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    green_led.value(1)
    
#
# Server socket
#
addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
server_sock = socket.socket()
server_sock.bind(addr)
server_sock.listen(1)
print('listening on', addr)

#
# Infinite loop
#

del parameters
del ujson

while True:
    time.sleep(0.05)
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(2048).decode()
        
        for i, val in enumerate(request.split(',')):
            servos[i].set_degree(int(val))
            
        acc  = mpu6500.acceleration
        gyro = mpu6500.gyro
        
        status = f"""
            "accelerometer" : {list(acc)},
            "gyroscope" : {list(gyro)} 
        """
        cl.send(status.encode())
        cl.close()
    except OSError as e:
        cl.close()
        print('connection closed')
        blue_led.value(0)
        red_led.value(1)
