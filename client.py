import socket
from threading import Thread, RLock
import pickle

class Server(Thread):
    def __init__(self, to):
        Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 2000
        self.host = to
        self.running = False
        self.lock = RLock()
        self.toSend = []
        
    def run(self):
        self.running = True
        while self.running:
            with self.socket as s:
                s.connect((self.host, self.port))
                while self.running:
                    with self.lock:
                        if len(self.toSend) > 0:
                            toSend = self.toSend.pop()
                            s.sendall()



    def stop(self):
        self.running = False
