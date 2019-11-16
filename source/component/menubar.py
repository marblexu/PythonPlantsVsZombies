__author__ = 'marble_xu'

import pygame as pg
from .. import tool
from .. import constants as c

card_name_list = [c.CARD_SUNFLOWER, c.CARD_PEASHOOTER, c.CARD_SNOWPEASHOOTER, c.CARD_WALLNUT,
                  c.CARD_CHERRYBOMB, c.CARD_THREEPEASHOOTER, c.CARD_REPEATERPEA, c.CARD_CHOMPER,
                  c.CARD_PUFFMUSHROOM, c.CARD_POTATOMINE, c.CARD_SQUASH]
plant_name_list = [c.SUNFLOWER, c.PEASHOOTER, c.SNOWPEASHOOTER, c.WALLNUT,
                   c.CHERRYBOMB, c.THREEPEASHOOTER, c.REPEATERPEA, c.CHOMPER,
                   c.PUFFMUSHROOM, c.POTATOMINE, c.SQUASH]
plant_sun_list = [50, 100, 175, 50, 150, 325, 200, 150, 0, 25, 50]
plant_frozen_time_list = [0, 5000, 5000, 10000, 5000, 5000, 5000, 5000, 8000, 8000, 8000]
card_list = [0, 1, 3, 4, 7, 8, 9, 10]

class Card():
    def __init__(self, x, y, name_index):
        self.loadFrame(card_name_list[name_index])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.name_index = name_index
        self.sun_cost = plant_sun_list[name_index]
        self.frozen_time = plant_frozen_time_list[name_index]
        self.frozen_timer = -self.frozen_time

    def loadFrame(self, name):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        width, height = rect.w, rect.h

        self.image = tool.get_image(frame, 0, 0, width, height, c.BLACK, 0.78)
    
    def checkMouseClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.rect.x and x <= self.rect.right and
           y >= self.rect.y and y <= self.rect.bottom):
            return True
        return False

    def canClick(self, sun_value, current_time):
        if self.sun_cost <= sun_value and (current_time - self.frozen_timer) > self.frozen_time:
            return True
        return False

    def setFrozenTime(self, current_time):
        self.frozen_timer = current_time

    def update(self, sun_value, current_time):
        if (self.sun_cost > sun_value or
            (current_time - self.frozen_timer) <= self.frozen_time):
            self.image.set_alpha(128)
        else:
            self.image.set_alpha(255)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class MenuBar():
    def __init__(self, card_list, sun_value):
        self.loadFrame(c.MENUBAR_BACKGROUND)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 0
        
        self.sun_value = sun_value
        self.card_offset_x = 32
        self.setupCards(card_list)
        self.font = pg.font.SysFont(None, 20)

    def loadFrame(self, name):
        frame = tool.GFX[name]
        rect = frame.get_rect()
        frame_rect = (rect.x, rect.y, rect.w, rect.h)

        self.image = tool.get_image(tool.GFX[name], *frame_rect, c.WHITE, 1)

    def update(self, current_time):
        self.current_time = current_time
        for card in self.card_list:
            card.update(self.sun_value, self.current_time)

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
        y = 8
        for index in card_list:
            x += 55
            self.card_list.append(Card(x, y, index))

    def checkCardClick(self, mouse_pos):
        result = None
        for card in self.card_list:
            if card.checkMouseClick(mouse_pos):
                if card.canClick(self.sun_value, self.current_time):
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

    def setCardFrozenTime(self, plant_name):
        for card in self.card_list:
            if plant_name_list[card.name_index] == plant_name:
                card.setFrozenTime(self.current_time)
                break

    def drawSunValue(self):
        width = 32
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
        self.value_rect.y = self.rect.bottom - 21
        
        self.image.blit(self.value_image, self.value_rect)

    def draw(self, surface):
        self.drawSunValue()
        surface.blit(self.image, self.rect)
        for card in self.card_list:
            card.draw(surface)