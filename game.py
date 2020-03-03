import pygame
from threading import Thread
import math
import os
import time
import pickle


class Game():
    def __init__(self):
        self.commands = []
        self.players = []
        self.entities = []

class Entity():
    def __init__(self):
        self.size = (0,0)
        self.position = (0,0)
    
    def setPosition(self, pos):
        self.position = pos

    def setSize(self, size):
        self.size = size


class Command():
    def __init__(self, code):
        self.code = code
        self.attributes = []

    def serialize(self):
        return pickle.dumps([self.code] + self.attributes)

class MoveCommand(Command):
    def __init__(self, id, x, y):
        super().__init__(0)

class CommandUnserializer():
    def __init__(self):
        pass

    def unserialize(self, buffer):
        data = pickle.loads(buffer)
        typ = data[0]
        atttributes = data[1:]
        #typ:
        #   0: MoveCommand
        if typ == 0:
            return MoveCommand(atttributes[0], atttributes[1], atttributes[2])
        
