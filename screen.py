import pygame
from threading import Thread
import math
import os
import time
import guielement

class Screen():
    def __init__(self, sources, resolution, joysticks):
        self.texts = []
        self.drawables = []
        self.resolution = resolution
        self.joysticks = joysticks
        self.window = pygame.display.set_mode(self.resolution)
        self.title = "Super Smash Bros No Jutsu | "
        self.quit = False
        
        self.successor = None
        self.sources = sources

    def display(self):
        pass

    def update(self):
        pass

    def handleEvent(self, events):
        pass

    def blitTexts(self):
        for text in self.texts:
            txt, rect = text.getShape()
            self.window.blit(txt, rect)

    def draw(self):
        for d in self.drawables:
            d.draw(self.window)

    def addText(self, text):
        self.texts.append(text)

    def mutate(self, new):
        return new(self.sources, self.resolution, self.joysticks)



class Loading(Screen):
    def __init__(self, sources, resolution, joysticks):
        Screen.__init__(self, sources, resolution, joysticks)
        self.title += "Chargement"
        pygame.display.set_caption(self.title)
        self.advance = 0
        self.font = pygame.font.Font("src/fonts/naruto.ttf", 32)
        self.loader = Loader(sources)
        self.loader.start()

        w, h = pygame.display.get_surface().get_size()

        self.text = guielement.Text()
        self.text.setFont(self.font).setColor((0,0,0)).setText("Chargement 0%").setPosition((w//2, h//2))

        self.texts.append(self.text)

        self.progress = guielement.ProgressBar(0, 100, self.advance)
        self.progress.setPosition((w//2, h//4 * 3)).setSize((w//2, h//8)).setBorder(10, (0,0,0))
        self.drawables.append(self.progress)


    def display(self):
        pygame.display.set_caption("Super Smash Bros No Jutsu | Chargement {}%".format(self.advance))
        self.window.fill((255,255,255))

        self.text.setText("Loading {}%".format(self.advance))

        self.blitTexts()

        self.progress.setValue(self.advance)

        self.draw()

        pygame.display.flip()

    def update(self):
        self.advance = self.loader.getAdvance()
        if self.advance == 100:
            self.loader.join()
            self.successor = self.mutate(Menu)


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
                    if line.endswith(".png"):
                        image = pygame.image.load(line).convert_alpha()
                    else:
                        image = pygame.image.load(line).convert()
                    self.swh.store(path, path[-1].split(".")[0], image)
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
        
class ContollerConnection(Screen):
    def __init__(self, sources, resolution, joysticks):
        Screen.__init__(self, sources, resolution, joysticks)
        
        self.background = pygame.transform.scale(sources.restore()["images"]["bgmenu"], self.window.get_size())
        pygame.display.set_caption("Super Smash Bros No Jutsu | Connexion des manettes | {}".format(pygame.joystick.get_count()))
        self.indicators = []
        
        w, h = pygame.display.get_surface().get_size()
        
        indicatorSize = w//8
        indicatorY = h//2 - indicatorSize // 2
        indicatorPositions = [
            (2.5 * (w//16), indicatorY),
            (0,0),
            (0,0),
            (0,0)
        ]
        for i in range(1,4):
            indicatorPositions[i] = (indicatorPositions[i-1][0] + indicatorSize * 1.5, indicatorPositions[i-1][1])

        self.indicators.append(guielement.ControllerIndicator(1, sources).setPosition(indicatorPositions[0]).setSize((indicatorSize, indicatorSize)))
        self.indicators.append(guielement.ControllerIndicator(2, sources).setPosition(indicatorPositions[1]).setSize((indicatorSize, indicatorSize)))
        self.indicators.append(guielement.ControllerIndicator(3, sources).setPosition(indicatorPositions[2]).setSize((indicatorSize, indicatorSize)))
        self.indicators.append(guielement.ControllerIndicator(4, sources).setPosition(indicatorPositions[3]).setSize((indicatorSize, indicatorSize)))

        for i in self.indicators:
            self.drawables.append(i)
        
        self.reloadJoysticks()

        refreshText = guielement.Text().setText("Espace: rafraichir manettes").setFont(self.sources.restore()["fonts"]["naruto"][26]).setColor((0,0,0)).setPosition((w//2, h - h//8))
        self.addText(refreshText)
        startText = guielement.Text().setText("Entrer: Jouer").setFont(self.sources.restore()["fonts"]["naruto"][26]).setColor((0,0,0)).setPosition((w//2, h - h//16))
        self.addText(startText)

    def display(self):
        self.window.fill((0,0,0))
        self.window.blit(self.background, (0,0))
        self.draw()
        self.blitTexts()
        pygame.display.flip()

    def update(self):
        pass

    def handleEvent(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.quit = True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.successor = self.mutate(Menu)
                elif e.key == pygame.K_DOWN:
                    pass
                elif e.key == pygame.K_UP:
                    pass
                elif e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    pass
                elif e.key == pygame.K_SPACE:
                    self.reloadJoysticks()
            elif e.type == pygame.JOYHATMOTION:
                lr, ud = e.value
                if ud > 0:
                    pass
                elif ud < 0:
                    pass
            elif e.type == pygame.JOYBUTTONDOWN:
                self.indicators[e.joy].giveFeedback()
                if e.button == 0:
                    pass
            elif e.type == pygame.JOYBUTTONUP:
                self.indicators[e.joy].stopFeedback()
                if e.button == 0:
                    pass

    def reloadJoysticks(self):
        pygame.joystick.quit()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for x in range(pygame.joystick.get_count()):
            self.joysticks[x].init()
        for i in range(0,4):
            self.indicators[i].desactivate() 
        for x in range(pygame.joystick.get_count()):
            self.indicators[x].activate()
        pygame.display.set_caption("Super Smash Bros No Jutsu | Connexion des manettes | {}".format(pygame.joystick.get_count()))
        print("Info: {} controllers connected".format(pygame.joystick.get_count()))

class Menu(Screen):
    def __init__(self, sources, resolution, joysticks):
        Screen.__init__(self, sources, resolution, joysticks)
        self.resolution = resolution
        pygame.display.set_caption(self.title + "Menu")
        self.background = pygame.transform.scale(sources.restore()["images"]["bgmenu"], self.window.get_size())
        self.font = sources.restore()["fonts"]["naruto"][32]

        w, h = pygame.display.get_surface().get_size()

        self.texts = []
        
        self.selectionColor = (218, 105, 105)
        self.textColor = (0,0,0)

        self.local = guielement.Text()
        self.local.setFont(self.font).setColor(self.textColor).setSelectionColor(self.selectionColor).setText("Jouer en local").setPosition((w//2, h//8 * 4)).setAction(lambda : self.mutate(ContollerConnection))
        self.texts.append(self.local)

        self.multi = guielement.Text()
        self.multi.setFont(self.font).setColor(self.textColor).setSelectionColor(self.selectionColor).setText("Jouer en multijoueur").setPosition((w//2, h//8 * 5))
        self.texts.append(self.multi)

        self.options = guielement.Text()
        self.options.setFont(self.font).setColor(self.textColor).setSelectionColor(self.selectionColor).setText("Parametres").setPosition((w//2, h//8 * 6)).setAction(lambda : self.mutate(Settings))
        self.texts.append(self.options)

        self.credits = guielement.Text()
        self.credits.setFont(self.font).setColor(self.textColor).setSelectionColor(self.selectionColor).setText("Credits").setPosition((w//2, h//8 * 7))
        self.texts.append(self.credits)

        self.selected = self.local.select()

        self.local.link("down", self.multi).link("up", self.credits)
        self.multi.link("down", self.options).link("up", self.local)
        self.options.link("down", self.credits).link("up", self.multi)
        self.credits.link("down", self.local).link("up", self.options)
        

    def display(self):
        self.window.blit(self.background, (0,0))
        self.blitTexts()
        pygame.display.flip()

    def update(self):
        pass

    def handleEvent(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.quit = True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.quit = True
                elif e.key == pygame.K_DOWN:
                    self.selected = self.selected.goTo("down")
                elif e.key == pygame.K_UP:
                    self.selected = self.selected.goTo("up")
                elif e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER or e.key == pygame.K_SPACE:
                    self.successor = self.selected.trigger()
            elif e.type == pygame.JOYHATMOTION:
                lr, ud = e.value
                if ud > 0:
                    self.selected = self.selected.goTo("up")
                elif ud < 0:
                    self.selected = self.selected.goTo("down")
            elif e.type == pygame.JOYBUTTONDOWN:
                if e.button == 0:
                    self.successor = self.selected.trigger()


class Settings(Screen):
    def __init__(self, sources, resolution, joysticks):
        Screen.__init__(self, sources, resolution, joysticks)
        pygame.display.set_caption(self.title + "Options")
        self.background = pygame.transform.scale(sources.restore()["images"]["battlefield_background"], self.window.get_size())
        self.font = sources.restore()["fonts"]["naruto"][32]

        w, h = pygame.display.get_surface().get_size()

        self.texts = []

        self.optionsText = guielement.Text().setText("Options").setColor((0,0,0)).setSelectionColor((255, 135, 48)).setPosition((w//2, h//8)).setFont(sources.restore()["fonts"]["naruto"][32])
        self.texts.append(self.optionsText)

        self.refreshControllersText = guielement.Text().setText("Connecter manettes").setColor((0,0,0)).setSelectionColor((255, 135, 48)).setPosition((w//2, h//8 * 3)).setFont(sources.restore()["fonts"]["naruto"][26]).setAction(lambda: self.reloadJoysticks()).select()
        self.selected = self.refreshControllersText
        self.texts.append(self.refreshControllersText)

    def display(self):
        self.window.blit(self.background, (0,0))
        self.blitTexts()
        pygame.display.flip()

    def update(self):
        self.refreshControllersText.setText("Connecter manettes ({})".format(pygame.joystick.get_count()))
        pass

    def handleEvent(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.quit = True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.successor = self.mutate(Menu)
                elif e.key == pygame.K_DOWN:
                    self.selected = self.selected.goTo("down")
                elif e.key == pygame.K_UP:
                    self.selected = self.selected.goTo("up")
                elif e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER or e.key == pygame.K_SPACE:
                    self.successor = self.selected.trigger()
            elif e.type == pygame.JOYHATMOTION:
                lr, ud = e.value
                if ud > 0:
                    self.selected = self.selected.goTo("up")
                elif ud < 0:
                    self.selected = self.selected.goTo("down")
            elif e.type == pygame.JOYBUTTONDOWN:
                if e.button == 0:
                    self.successor = self.selected.trigger()

    def reloadJoysticks(self):
        pygame.joystick.quit()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for x in range(pygame.joystick.get_count()):
            self.joysticks[x].init()
        print("Info: {} controllers connected".format(pygame.joystick.get_count()))


class Connect(Screen):
    def __init__(self):
        self.window = pygame.display.set_mode((1280,720))
        self.background = pygame.image.load("src/images/battlefield_background.jpg").convert()
        self.window.blit(self.background, (0,0))

    def display(self):
        print("Display the connection screen for distant game")

class InGame(Screen):
    def __init__(self, sources):
        self.window = pygame.display.set_mode((1280,720))
        self.background = pygame.image.load("/home/mathis/git-repos/magic-jubaston/src/images/battlefield_background.jpg").convert()
        self.window.blit(self.background, (0,0))

    def display(self):
        pygame.display.flip()
