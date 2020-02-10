import gui.screen
import pygame
from pygame.locals import *
import time

def main():
    frameRate = 60
    frameInterval = 1/frameRate
    lastFrameTime = 0

    tickRate = 100
    tickInterval = 1 / tickRate
    lastTickTime = 0

    
    sources = gui.screen.SourceWH()

    pygame.init()
    screen = gui.screen.Loading(sources)

    running = True

    try:
        while running:
            t = time.time()
            if t >= lastFrameTime + frameInterval:
                lastFrameTime = t
                screen.display()
            if t >= lastTickTime + tickInterval:
                lastTickTime = t
                screen.update()
                if screen.successor != None:
                    screen = screen.successor
            screen.handleEvent(pygame.event.get())
            

    except KeyboardInterrupt:
        running = False
    pygame.quit()
        
if __name__ == "__main__":
    main()