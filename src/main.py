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
i2c1 = I2C(1, sda=Pin(18), scl=Pin(19))
print("Devices:", i2c1.scan())
mpu6500 = MPU6500(i2c1, accel_sf=SF_G, gyro_sf=SF_DEG_S)
led = Pin("LED", Pin.OUT)
idx = 0
servos = {}
for leg in ["L1", "L2", "L3", "L4"]:
    servos[leg] = {}
    for joint in ["1", "2", "3"]:
        servos[leg][joint] = Servo(parameters["servo"][idx], PWM(idx))
        idx += 1     


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
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
#
# Server socket
#
addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

#
# Infinite loop
#

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(2048).decode()
        print(request)
        
        try:
            move = ujson.loads(request)
            for leg in move.keys():
                for joint in move[leg].keys():
                    servos[leg][joint].set_degree(move[leg][joint])
        except Exception as e:
            print(e)
            
        acc  = mpu6500.acceleration
        gyro = mpu6500.gyro
        
        status = {
            "accelerometer" : {
                    "x" : acc[0],
                    "y" : acc[1],
                    "z" : acc[2]
                },
            "gyroscope" : {
                "x" : gyro[0],
                "y" : gyro[1],
                "z" : gyro[2]
                }
            }
        cl.send(ujson.dumps(status).encode())
        cl.close()
    except OSError as e:
        cl.close()
        print('connection closed')
