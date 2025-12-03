import socket
import threading
import queue

class ServerThread(threading.Thread):
    def __init__(self, PORT=5005):
        threading.Thread.__init__(self)
        self.PORT = PORT
        self.queue = queue.Queue()
        self.STOP = False

    def run(self):
        while self.STOP is False:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(("0.0.0.0", self.PORT))
            self.socket.listen(1)
            client_socket, addr = self.socket.accept()
            print(f"Client connected from {addr}")
            data = client_socket.recv(1024).decode('utf-8')
            self.queue.put(data)
            print("Client disconnected")
            client_socket.close()

    def stop(self):
        self.STOP = True

    def get_element(self):
        if self.queue.empty():
            return None
        return self.queue.get()