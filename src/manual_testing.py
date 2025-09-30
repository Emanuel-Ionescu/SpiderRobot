import socket
import time

try:
    import ujson as json
    RUNNING_ON = "PICO"
except:
    RUNNING_ON = "x86"
    import json

with open("./config.json", 'r') as f:
    PARAMETERS = json.load(f)



def load_html():
    with open("./index.html", "r") as f:
        return f.read()

def main():
    
    # Servo
    if RUNNING_ON == "PICO":
        import servo
        from machine import PWM
        SERVOS = [servo.Servo(PARAMETERS["servo"][i], PWM(i)) for i in range(12)]
    
    # WiFi
    if RUNNING_ON == "PICO":
        import network

        ssid     = PARAMETERS["network"]["SSID"]
        password = PARAMETERS["network"]["password"]
        
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

    # Server socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on', addr)

    while True:
        try:
            cl, addr = s.accept()
            print('client connected from', addr)
            request = cl.recv(1024).decode()
            #print(request)

            stateis = (-1, -1)

            for i in range(0, 13):
                if f"/input{i}" in request:
                    pos = request.find("value=")
                    if pos != -1:
                        val = request[pos+6:pos+9].split(" ")[0]
                        stateis = (i - 1, int(val))

            print(stateis)
            if stateis[0] == -1:
                if stateis[1] == 0:
                    #reset program
                    return 0
            else:
                if RUNNING_ON == "PICO":
                    print("servo=", stateis[0], "deg=", stateis[1])
                    SERVOS[stateis[0]].set_degree(stateis[1])


            response = load_html()

            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'.encode())
            cl.send(response.encode())
            cl.close()

        except OSError as e:
            cl.close()
            print('connection closed')
        except KeyboardInterrupt:
            exit()

if __name__ == "__main__":
    while True:
        main()