import socket
from threading import Thread

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 2000
        self.host = socket.gethostbyname(socket.gethostname)
        self.running = False
        
    def run(self):
        self.running = True
        while self.running:
            with self.socket as s:
                s.bind((self.host, self.port))
                s.listen(1)
                while self.running:
                    conn, addr = s.accept()
                    while True:
                        data = conn.recv(1024)
                        if not data: break
                        conn.sendall(data)


    def stop(self):
        self.running = False
