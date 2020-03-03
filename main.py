import screen
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

    resolution = (1280, 720)
    resolution = (1600, 900)
    
    sources = screen.SourceWH()

    pygame.init()

    for x in range(pygame.joystick.get_count()):
        pygame.joystick.Joystick(x).init()

    state = screen.Loading(sources, resolution, [])

    running = True

    try:
        while running and not state.quit:
            t = time.time()
            if t >= lastFrameTime + frameInterval:
                lastFrameTime = t
                state.display()
            if t >= lastTickTime + tickInterval:
                lastTickTime = t
                
                state.update()
                if state.successor != None:
                    state = state.successor
            state.handleEvent(pygame.event.get())
            #pygame.joystick.quit()
            #pygame.joystick.init()
            
            

    except KeyboardInterrupt:
        running = False
    if state is screen.Loading:
        state.loader.join()
    pygame.quit()
        
if __name__ == "__main__":
    main()