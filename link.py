import time 

class Link():
    def __init__(self, ip):
        self.ip = ip
        self.lastOnline = time.time()

class LinkManager():
    def __init__(self):
        self.links = []
    
    def update(self, ip):
        for l in self.links:
            if l.ip == ip:
                l.lastOnline = time.time()
                break

    def clean