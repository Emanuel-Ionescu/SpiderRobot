import serial
import time

class SerialClient:

    def __init__(self, port : str, baud_rate : int = 115200):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
        self.ser.flush()
        time.sleep(2)
    
    def __call__(self, data : str):
        self.ser.write((data + '\n').encode('utf-8'))
        line = self.ser.readline().decode('utf-8', errors='replace').rstrip()
        if line:
            return line
        else:
            return "TIMEOUT"

class DummySerialClient:

    def __init__(self):
        pass
    
    def __call__(self, data : str):
        return "Dummy response!"