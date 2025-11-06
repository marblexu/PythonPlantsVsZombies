__author__ = 'marble_xu'

import pygame as pg
from .. import tool
from .. import constants as c

class Grave(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        
        self.name = c.GRAVE
        self.frames = []
        self.frame_index = 0
        self.loadImages()
        self.frame_num = len(self.frames)
        
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        self.health = 10  # Grave health
        self.dead = False
        
        self.animate_timer = 0
        self.animate_interval = 150
        
    def loadImages(self):
        # Load grave images
        grave_name = self.name
        self.loadFrames(self.frames, grave_name, 1)
        
    def loadFrames(self, frame_list, name, scale):
        # Load frames from sprite sheet
        frame_rect = tool.GRAVE_RECT[name]
        for i in range(frame_rect['frame_num']):
            x = frame_rect['x'] + i * frame_rect['width']
            y = frame_rect['y']
            width = frame_rect['width']
            height = frame_rect['height']
            image = tool.get_image(tool.GFX[name], x, y, width, height, c.BLACK, scale)
            frame_list.append(image)
            
    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        self.animation()
        
    def animation(self):
        if (self.current_time - self.animate_timer) > self.animate_interval:
            self.frame_index += 1
            if self.frame_index >= self.frame_num:
                self.frame_index = 0
            self.animate_timer = self.current_time
            self.image = self.frames[self.frame_index]
            
    def setDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.dead = True
            self.kill()
            
class GraveBuster(pg.sprite.Sprite):
    def __init__(self, x, y, grave):
        pg.sprite.Sprite.__init__(self)
        
        self.name = c.GRAVE_BUSTER
        self.frames = []
        self.frame_index = 0
        self.loadImages()
        self.frame_num = len(self.frames)
        
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        self.grave = grave
        self.eat_timer = 0
        self.eat_duration = c.GRAVE_BUSTER_EAT_TIME
        self.state = c.IDLE
        
        self.animate_timer = 0
        self.animate_interval = 150
        
    def loadImages(self):
        # Load grave buster images
        buster_name = self.name
        self.loadFrames(self.frames, buster_name, 1)
        
    def loadFrames(self, frame_list, name, scale):
        # Load frames from sprite sheet
        frame_rect = tool.PLANT_RECT[name]
        for i in range(frame_rect['frame_num']):
            x = frame_rect['x'] + i * frame_rect['width']
            y = frame_rect['y']
            width = frame_rect['width']
            height = frame_rect['height']
            image = tool.get_image(tool.GFX[name], x, y, width, height, c.BLACK, scale)
            frame_list.append(image)
            
    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        self.handleState()
        self.animation()
        
    def handleState(self):
        if self.state == c.IDLE:
            self.idling()
        elif self.state == c.ATTACK:
            self.attacking()
            
    def idling(self):
        # Start eating grave
        self.state = c.ATTACK
        self.eat_timer = self.current_time
        
    def attacking(self):
        # Check if done eating
        if (self.current_time - self.eat_timer) > self.eat_duration:
            # Destroy both grave and grave buster
            self.grave.setDamage(10)  # Enough damage to destroy grave
            self.kill()
            
    def animation(self):
        if (self.current_time - self.animate_timer) > self.animate_interval:
            self.frame_index += 1
            if self.frame_index >= self.frame_num:
                self.frame_index = self.frame_num - 1  # Stay on last frame
            self.animate_timer = self.current_time
            self.image = self.frames[self.frame_index]
            
    def canAttack(self, zombie):
        # Grave buster doesn't attack zombies
        return False