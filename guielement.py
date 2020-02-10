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

    def link(self, direction, elem):
        self.links[direction] = elem
        return self

    def goTo(self, dir):
        elem = self.links[dir]
        if elem == None:
            return
        self.deselect()
        elem.select()
        return elem


    def select(self):
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