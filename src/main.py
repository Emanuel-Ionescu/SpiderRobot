from machine import Pin, PWM, I2C
from mpu6500 import MPU6500, SF_G, SF_DEG_S
import ujson
from servo import Servo

with open("./servo_calibration.json", 'r') as f:
    parameters = ujson.load(f)

#
# Objecs declaration
#

i2c1 = I2C(1, sda=Pin(18), scl=Pin(19))
print("Devices:", i2c1.scan())

mpu6500 = MPU6500(i2c1, accel_sf=SF_G, gyro_sf=SF_DEG_S)

led = Pin("LED", Pin.OUT)

servos = [Servo(i, PWM(i), 0, 1, []) for i in range(12)]

#
# Infinite loop
#

while True:
    led.toggle()
    
