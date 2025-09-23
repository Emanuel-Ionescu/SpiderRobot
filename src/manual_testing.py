import network
import socket
import time

# WiFi
ssid = ""
password = ""

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

def load_html():
    with open("./index.html", "r") as f:
        return f.read()

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024).decode()
        #print(request)

        stateis = None

        for i in range(1, 13):
            if f"/slider{i}" in request:
                pos = request.find("value=")
                if pos != -1:
                    val = request[pos+6:pos+9].split(" ")[0]
                    stateis = (i - 1, val)

        print(stateis)

        response = load_html()

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'.encode())
        cl.send(response.encode())
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')
