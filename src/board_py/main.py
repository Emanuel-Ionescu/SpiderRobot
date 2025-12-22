import ujson
import time
import socket
import sys
import select

from servo import Servo
from machine import Pin, PWM, I2C, reset as machine_reset
from mpu6500 import MPU6500, SF_G, SF_DEG_S

print("Pico starting!")
with open("./config.json", 'r') as f:
    parameters = ujson.load(f)
print("Config loaded!")
#
# Hardware declaration
#
class DummyMPU6500:
    acceleration = (0,0,0)
    gyro = (0,0,0)

# I2C
i2c1 = I2C(1, sda=Pin(18), scl=Pin(19))
print("I2C Devices:", i2c1.scan())
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

#
# Infinite loop
#

green_led.value(1)
while True:
    time.sleep(0.05)
    try:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            blue_led.value(1)
            red_led.value(0)
            data = sys.stdin.readline().strip()
            command = data.split(" ")[0]

            if command == "set_angles":
                angles = data.split(" ")[1]
                for index, angle in enumerate(angles.split(":")):
                    servos[index].set_degree(int(angle))
                        
                acc  = mpu6500.acceleration
                gyro = mpu6500.gyro
                
                status = {"angles" : data, "accelerometer" : list(acc), "gyroscope" : list(gyro)}
                print(ujson.dumps(status))

            if command == "reset":
                for servo in servos:
                    servo.set_degree(0)
                print("Servos reset!\nResetting PICO...")
                machine_reset()
            if command == "help":
                print("""
Help:
help                - shows this message
set_angles <angles> - sets the angles of the servos (xx:xx: ...) for 12 motors
reset               - reset the program

""")
    except Exception as e:
            print(e)