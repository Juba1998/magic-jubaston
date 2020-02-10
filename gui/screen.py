from abc import ABC, abstractmethod
import pygame
from threading import Thread
import math
import os
import time

class Screen(ABC):
    def display(self, sources):
        pass

    def update(self):
        pass

    def handleEvent(self, event):
        pass

class Loading(Screen):
    def __init__(self, sources):
        self.window = pygame.display.set_mode((1280,720))
        pygame.display.set_caption("Magic Jubaston | Loading")

        self.text = "Starting..."
        self.advance = 0
        self.font = pygame.font.Font("src/fonts/bbo.ttf", 32)
        self.loader = Loader(sources)
        self.loader.start()
        self.sources = sources
        self.successor = None

    def display(self):
        pygame.display.set_caption("Magic Jubaston | Loading {}%".format(self.advance))
        self.window.fill((0,0,0))
        txt = self.font.render("Loading {}%".format(self.advance), True, (255,0,0), None)
        rect = txt.get_rect()
        w, h = pygame.display.get_surface().get_size()
        rect.center = (w // 2, h // 2)
        self.window.blit(txt, rect)

        width = w // 2
        propWidth = (int)(width * (self.advance / 100))
        pygame.draw.rect(self.window, (255,0,0), (w//4, (h//2) + (h // 8), propWidth, h // 8))
        pygame.display.flip()

    def update(self):
        self.advance = self.loader.getAdvance()
        if self.advance == 100:
            self.loader.join()
            self.successor = Menu(self.sources)


class Loader(Thread):
    def __init__(self, sources):
        Thread.__init__(self)
        self.swh = sources
        self.advance = 0

    def run(self):
        src = open("src/sources.txt","r")
        content = src.readlines()
        toLoad = len(content)
        loaded = 0
        self.advance = 0
        """dirname = os.path.dirname(__file__)
        splittedDirname = dirname.split("/")
        splittedDirname.pop()
        dirname = "/".join(splittedDirname)
        print(dirname)"""
        for line in content:
            if line[-1] == '\n':
                line = line[:-1]
            path = line.split("/")
            line = "src/{}".format(line)
            if path[0] == "images":
                try:
                    self.swh.store(path, path[-1].split(".")[0], pygame.image.load(line).convert())
                except pygame.error as message:
                    print("[Error][Loading]: " + line)
            if path[0] == "fonts":
                size = (int)(path[-1].split(".")[-1])
                path[-1] = ".".join(path[-1].split('.')[:-1])
                line = "/".join(path)
                line = "src/{}".format(line)
                path[-1] = path[-1].split(".")[0]
                path.append((str)(size))
                try:
                    self.swh.store(path, size, pygame.font.Font(line, size))
                except pygame.error as message:
                    print("[Error][Loading]: " + line)
                except FileNotFoundError:
                    print("[Error][Loading]: " + line)
            loaded = loaded + 1
            self.advance = math.floor((loaded / toLoad) * 100)
        self.advance = 100
        #print(self.swh.restore())

    def getAdvance(self):
        return self.advance

class SourceWH():
    def __init__(self):
        self.storage = {}

    def store(self, path, name, ressource):
        dictio = self.storage
        for x in path:
            if x == path[-1]:
                dictio[name] = ressource
            else:
                if not x in dictio:
                    dictio[x] = {}
                dictio = dictio[x]
        
    def restore(self):
        return self.storage
        
class LocalConnection(Screen):
    def __init__(self):
        self.window = pygame.display.set_mode((1280,720))
        self.background = pygame.image.load("src/images/battlefield_background.jpg").convert()
        self.window.blit(self.background, (0,0))

    def display(self):
        print("Display the connection of the different players and their controllers")

class Menu(Screen):
    def __init__(self, sources):
        self.successor = None
        self.window = pygame.display.set_mode((1280,720))
        self.sources = sources
        pygame.display.set_caption("Magic Jubaston | Menu")
        self.background = sources.restore()["images"]["battlefield_background"]
        self.font = sources.restore()["fonts"]["bbo"][32]
        self.window.blit(self.background, (0,0))
        self.lines = ["Local", "Online", "Options", "Credits"]
        self.selected = 0

    def display(self):
        self.window.blit(self.background, (0,0))
        w, h = pygame.display.get_surface().get_size()
        listY = h//(len(self.lines))
        lineIndex = 0
        for line in self.lines:
            if lineIndex == self.selected:
                color = (0,0,255)
            else:
                color = (255,0,0)
            txt = self.font.render(line, True, color, None)
            rect = txt.get_rect()
            rect.center = (w//2, listY)
            listY = listY + (1.5 * rect.height)
            self.window.blit(txt, rect)
            lineIndex = lineIndex + 1
        pygame.display.flip()

    def update(self):
        pass

class Connect(Screen):
    def __init__(self):
        self.window = pygame.display.set_mode((1280,720))
        self.background = pygame.image.load("src/images/battlefield_background.jpg").convert()
        self.window.blit(self.background, (0,0))

    def display(self):
        print("Display the connection screen for distant game")

class Game(Screen):
    def __init__(self, sources):
        self.window = pygame.display.set_mode((1280,720))
        self.background = pygame.image.load("/home/mathis/git-repos/magic-jubaston/src/images/battlefield_background.jpg").convert()
        self.window.blit(self.background, (0,0))

    def display(self):
        pygame.display.flip()
