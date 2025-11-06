__author__ = 'marble_xu'

import pygame as pg
import random
from .. import tool
from .. import constants as c

class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        
        # 加载金币图像
        self.frames = []
        self.frame_index = 0
        self.load_images()
        
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        self.animate_timer = 0
        self.animate_interval = 100  # 动画间隔时间
        self.float_speed = 1  # 向上浮动的速度
        self.float_distance = 50  # 浮动的总距离
        self.start_y = y  # 初始Y坐标
        self.collected = False
        
    def load_images(self):
        """加载金币动画帧"""
        # 尝试从GFX中获取金币图像
        if 'Coin' in tool.GFX:
            self.frames = tool.GFX['Coin']
        else:
            # 如果没有金币图像资源，创建一个临时的黄色圆形
            for i in range(8):
                surface = pg.Surface((30, 30), pg.SRCALPHA)
                pg.draw.circle(surface, c.GOLD, (15, 15), 15)
                self.frames.append(surface)
    
    def update(self, current_time):
        """更新金币状态"""
        # 动画更新
        if (current_time - self.animate_timer) > self.animate_interval:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.animate_timer = current_time
        
        # 向上浮动
        if self.rect.bottom > self.start_y - self.float_distance:
            self.rect.y -= self.float_speed
    
    def draw(self, surface):
        """绘制金币"""
        surface.blit(self.image, self.rect)