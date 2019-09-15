__author__ = 'marble_xu'

import pygame as pg
from .. import tool
from .. import constants as c

card_name_list = [c.CARD_SUNFLOWER, c.CARD_PEASHOOTER, c.CARD_SNOWPEASHOOTER, c.CARD_WALLNUT,
                  c.CARD_CHERRYBOMB, c.CARD_THREEPEASHOOTER, c.CARD_REPEATERPEA]
plant_name_list = [c.SUNFLOWER, c.PEASHOOTER, c.SNOWPEASHOOTER, c.WALLNUT,
                   c.CHERRYBOMB, c.THREEPEASHOOTER, c.REPEATERPEA]
plant_sun_list = [50, 100, 175, 50, 150, 325, 200]
card_list = [0, 1, 2, 3, 4, 5, 6]

class Card():
    def __init__(self, x, y, name_index):
        self.loadFrame(card_name_list[name_index])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.name_index = name_index
        self.sun_cost = plant_sun_list[name_index]

    def loadFrame(self, name):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        width, height = rect.w, rect.h

        self.image = tool.get_image(frame, 0, 0, width, height, c.BLACK, 0.8)
    
    def checkMouseClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.rect.x and x <= self.rect.right and
           y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class MenuBar():
    def __init__(self, card_list, sun_value):
        self.loadFrame(c.MENUBAR_BACKGROUND)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 0
        
        self.sun_value = sun_value
        self.card_offset_x = 38
        self.setupCards(card_list)
        self.font = pg.font.SysFont(None, 20)

    def loadFrame(self, name):
        frame_rect = [11, 0, 560, 108]
        frame = tool.GFX[name]
        rect = frame.get_rect()
        width, height = rect.w, rect.h

        self.image = tool.get_image(tool.GFX[name], *frame_rect, c.BLACK, 0.8)

    def createImage(self, x, y, num):
        if num == 1:
            return
        img = self.image
        rect = self.image.get_rect()
        width = rect.w
        height = rect.h
        self.image = pg.Surface((width * num, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        for i in range(num):
            x = i * width
            self.image.blit(img, (x,0))
        self.image.set_colorkey(c.BLACK)
    
    def setupCards(self, card_list):
        self.card_list = []
        x = self.card_offset_x
        y = 7
        for index in card_list:
            x += 51
            self.card_list.append(Card(x, y, index))

    def checkCardClick(self, mouse_pos):
        result = None
        for card in self.card_list:
            if card.checkMouseClick(mouse_pos):
                if card.sun_cost <= self.sun_value:
                    result = (plant_name_list[card.name_index], card.sun_cost)
                break
        return result
    
    def checkMenuBarClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.rect.x and x <= self.rect.right and
           y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False

    def decreaseSunValue(self, value):
        self.sun_value -= value

    def increaseSunValue(self, value):
        self.sun_value += value
    
    def drawSunValue(self):
        width = 30
        msg_image = self.font.render(str(self.sun_value), True, c.NAVYBLUE, c.LIGHTYELLOW)
        msg_rect = msg_image.get_rect()
        msg_w = msg_rect.width
        
        image = pg.Surface([width, 17])
        x = width - msg_w
        
        image.fill(c.LIGHTYELLOW)
        image.blit(msg_image, (x, 0), (0, 0, msg_rect.w, msg_rect.h))
        image.set_colorkey(c.BLACK)

        self.value_image = image
        self.value_rect = self.value_image.get_rect()
        self.value_rect.x = 18
        self.value_rect.y = self.rect.bottom - 20
        
        self.image.blit(self.value_image, self.value_rect)

    def draw(self, surface):
        self.drawSunValue()
        surface.blit(self.image, self.rect)
        for card in self.card_list:
            card.draw(surface)