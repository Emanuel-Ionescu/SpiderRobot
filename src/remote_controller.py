import socket
import time
from sequence import *

PICO_IP = "192.168.1.7"


def send_recv(step : Move | FullMove):
    print("Sending:",  step)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((PICO_IP, 8080))
    client_sock.send(bytes(step)) # type: ignore
    res =  client_sock.recv(2048).decode()
    client_sock.close()
    return res

def main():
    seq = WalkForwardSequence
    for i in range(seq.length):
        time.sleep(0.1)

        step = seq.getStep()

        if type(step) == Delay:
            time.sleep(float(step))
            continue
        
        send_recv(step)

    send_recv(FullMove(STAND_POSITION))


if __name__ == "__main__":
    main()