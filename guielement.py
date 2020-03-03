import pygame

class Element():
    def __init__(self):
        self.links = {
            "left" : None,
            "right" : None,
            "up" : None,
            "down" : None 
        }   
        self.selected = False
        self.position = (0,0)
        self.size = (0,0)
        self.action = lambda : None
        self.locked = False

    def link(self, direction, elem):
        self.links[direction] = elem
        return self

    def goTo(self, dir):
        elem = self.links[dir]
        if elem == None or elem.locked:
            return self
        self.deselect()
        elem.select()
        return elem


    def select(self):
        if self.locked:
            return None
        self.selected = True
        return self

    def deselect(self):
        self.selected = False
        return self

    def setPosition(self, xy):
        self.position = xy
        return self

    def setSize(self, wh):
        self.size = wh
        return self

    def getShape(self):
        pass

    def setAction(self, action):
        self.action = action
        return self

    def trigger(self):
        return self.action()

    def lock(self):
        self.locked = True
        #0.1
        return self

    def unlock(self):
        self.locked = False
        return self

class Shape(Element):
    def __init__(self):
        Element.__init__(self)

    def getShape(self):
        pass

class Drawable(Element):
    def __init__(self):
        Element.__init__(self)

    def draw(self):
        pass
    
class Text(Shape):
    def __init__(self):
        Element.__init__(self)
        self.font = None
        self.color = (0,0,0)
        self.selectionColor = (0,0,0)
        self.text = ""

    def getShape(self):
        if self.font == None:
            raise Exception("Undefined", "font")
        txt = self.font.render(self.text, True, self.color if not self.selected else self.selectionColor, None)
        rect = txt.get_rect()
        x, y = self.position

        rect.center = (x, y)
        return (txt, rect)

    def setText(self, txt):
        self.text = txt
        return self

    def setFont(self, font):
        self.font = font
        return self
    
    def setColor(self, color):
        self.color = color
        return self

    def setSelectionColor(self, selecolor):
        self.selectionColor = selecolor
        return self


class ProgressBar(Drawable):
    def __init__(self, mini, maxi, value):
        Element.__init__(self)
        self.color = (0,0,0)
        self.borderColor = (0,0,0)
        self.borderThickness = 0
        self.min = mini
        self.max = maxi
        self.value = value

    def draw(self, window):
        w, h = self.size
        x, y = self.position

        baseX = x - (w//2)
        baseY = y - (h//2)

        subX = baseX + self.borderThickness
        subY = baseY + self.borderThickness
        subWidth = w - (self.borderThickness * 2)

        ratio = self.value / (self.max - self.min)

        subWidth = subWidth * ratio
        subHeight = h - (self.borderThickness * 2)

        if self.borderThickness > 0:
            pygame.draw.rect(window, self.borderColor, (baseX, baseY, w, h), self.borderThickness)
        pygame.draw.rect(window, self.color, (subX, subY, subWidth, subHeight), 0)
        

    def setBorderThickness(self, thickness):
        self.borderThickness = thickness
        return self

    def setBorderColor(self, color):
        self.borderColor = color
        return self

    def setBorder(self, thickness, color):
        return self.setBorderThickness(thickness).setBorderColor(color)

    def setColor(self, color):
        self.color = color
        return self

    def setValue(self, value):
        self.value = value
        return self

    def setMin(self, mini):
        self.min = mini
        return self

    def setMax(self, maxi):
        self.max = maxi
        return self

    def setRange(self, mini, maxi):
        return self.setMin(mini).setMax(maxi)

class ControllerIndicator(Drawable):
    def __init__(self, number, sources):
        Element.__init__(self)
        if number < 1 or number > 4:
            raise Exception("Controller number must be between 1 and 4")
        self.activatedImage = sources.restore()["images"]["ico"]["controller"]["on"]["{}".format(number)]
        self.desactivatedImage = sources.restore()["images"]["ico"]["controller"]["off"]["{}".format(number)]
        self.feedbackImage = sources.restore()["images"]["ico"]["controller"]["feedback"]["{}".format(number)]
        self.activated = False
        self.feedback = False

    def draw(self, window):
        x,y = self.position
        w,h = self.size
        if self.feedback:
            image = self.feedbackImage
        elif self.activated:
            image = self.activatedImage
        else:
            image = self.desactivatedImage
        image = pygame.transform.scale(image, (w, h))
        window.blit(image, (x, y))

    def activate(self):
        self.activated = True

    def desactivate(self):
        self.activated = False

    def giveFeedback(self):
        self.feedback = True

    def stopFeedback(self):
        self.feedback = False
