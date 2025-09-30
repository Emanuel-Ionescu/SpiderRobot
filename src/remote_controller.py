import socket
import time
from sequence import *
PICO_IP = "192.168.1.14"

current_sequence = WalkForwardSequence
print(current_sequence.length)

while True:

    
    step = current_sequence.getStep()

    if type(step) == Delay:
        time.sleep(float(step))
        continue
    
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((PICO_IP, 8080))
    client_sock.send(bytes(step))
    response = client_sock.recv(2048)
    print(response)
    client_sock.close()
