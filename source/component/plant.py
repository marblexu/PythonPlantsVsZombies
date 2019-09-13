__author__ = 'marble_xu'

import pygame as pg
from .. import tool
from .. import constants as c

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, start_y, dest_y, name, damage, ice):
        pg.sprite.Sprite.__init__(self)

        self.name = name
        self.frames = []
        self.frame_index = 0
        self.load_images()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x - 40
        self.rect.y = start_y
        self.dest_y = dest_y
        self.y_vel = 4 if (dest_y > start_y) else -4
        self.x_vel = 4
        self.damage = damage
        self.ice = ice
        self.state = c.FLY
        self.current_time = 0

    def loadFrames(self, frames, name):
        frame_list = tool.GFX[name]
        rect = frame_list[0].get_rect()
        width, height = rect.w, rect.h
        
        for frame in frame_list:
            frames.append(tool.get_image(frame, 0, 0, width, height))
    
    def load_images(self):
        self.fly_frames = []
        self.explode_frames = []
        
        fly_name = self.name
        explode_name = 'PeaNormalExplode'
        
        self.loadFrames(self.fly_frames, fly_name)
        self.loadFrames(self.explode_frames, explode_name)
        
        self.frames = self.fly_frames

    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        if self.state == c.FLY:
            if self.rect.y != self.dest_y:
                self.rect.y += self.y_vel
                if self.y_vel * (self.dest_y - self.rect.y) < 0:
                    self.rect.y = self.dest_y
            self.rect.x += self.x_vel
            if self.rect.x > c.SCREEN_WIDTH:
                self.kill()
        elif self.state == c.EXPLODE:
            if(self.current_time - self.explode_timer) > 500:
                self.kill()

    def setExplode(self):
        self.state = c.EXPLODE
        self.explode_timer = self.current_time
        self.frames = self.explode_frames
        self.image = self.frames[self.frame_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Plant(pg.sprite.Sprite):
    def __init__(self, x, y, name, health, bullet_group, scale=1):
        pg.sprite.Sprite.__init__(self)
        
        self.frames = []
        self.frame_index = 0
        self.loadFrames(self.frames, name, scale)
        self.frame_num = len(self.frames)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        self.name = name
        self.health = health
        self.state = c.IDLE
        self.bullet_group = bullet_group
        self.animate_timer = 0
    
    def loadFrames(self, frames, name, scale):
        frame_list = tool.GFX[name]
        rect = frame_list[0].get_rect()
        width, height = rect.w, rect.h

        for frame in frame_list:
            frames.append(tool.get_image(frame, 0, 0, width, height, c.BLACK, scale))
    
    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        self.handleState()
        self.animation()
    
    def handleState(self):
        if self.state == c.IDLE:
            self.idling()
        elif self.state == c.ATTACK:
            self.attacking()
        elif self.state == c.ATTACKED:
            self.attacked()
    
    def idling(self):
        pass

    def attacking(self):
        pass

    def attacked(self):
        self.attacking()

    def animation(self):
        if (self.current_time - self.animate_timer) > 100:
            self.frame_index += 1
            if self.frame_index >= self.frame_num:
                self.frame_index = 0
            self.animate_timer = self.current_time
        
        self.image = self.frames[self.frame_index]
    
    def setAttack(self):
        pass
    
    def setIdle(self):
        self.state = c.IDLE

    def setAttacked(self):
        self.state = c.ATTACKED
        self.frame_index = 0
    
    def setDamage(self, damage):
        self.health -= damage

class Sun(Plant):
    def __init__(self, x, y, dest_x, dest_y):
        Plant.__init__(self, x, y, c.SUN, 0, None, 0.9)
        self.move_speed = 1
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.die_timer = 0

    def handleState(self):
        if self.rect.centerx != self.dest_x:
            self.rect.centerx += self.move_speed if self.rect.centerx < self.dest_x else -self.move_speed
        if self.rect.bottom != self.dest_y:
            self.rect.bottom += self.move_speed if self.rect.bottom < self.dest_y else -self.move_speed
        
        if self.rect.centerx == self.dest_x and self.rect.bottom == self.dest_y:
            if self.die_timer == 0:
                self.die_timer = self.current_time
            elif(self.current_time - self.die_timer) > c.SUN_LIVE_TIME:
                self.state = c.DIE
                self.kill()

    def checkCollision(self, x, y):
        if self.state == c.DIE:
            return False
        if(x >= self.rect.x and x <= self.rect.right and
           y >= self.rect.y and y <= self.rect.bottom):
            self.state = c.DIE
            self.kill()
            return True
        return False

class SunFlower(Plant):
    def __init__(self, x, y, sun_group):
        Plant.__init__(self, x, y, c.SUNFLOWER, c.PLANT_HEALTH, None)
        self.sun_timer = 0
        self.sun_group = sun_group
    
    def idling(self):
        if self.sun_timer == 0:
            self.sun_timer = self.current_time - (c.FLOWER_SUN_INTERVAL - 6000)
        elif (self.current_time - self.sun_timer) > c.FLOWER_SUN_INTERVAL:
            self.sun_group.add(Sun(self.rect.centerx, self.rect.bottom, self.rect.right, self.rect.bottom + self.rect.h // 2))
            self.sun_timer = self.current_time

class PeaShooter(Plant):
    def __init__(self, x, y, bullet_group):
        Plant.__init__(self, x, y, c.PEASHOOTER, c.PLANT_HEALTH, bullet_group)
        self.shoot_timer = 0
        
    def attacking(self):
        if (self.current_time - self.shoot_timer) > 2000:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.y, self.rect.y,
                                    c.BULLET_PEA, c.BULLET_DAMAGE_NORMAL, False))
            self.shoot_timer = self.current_time

    def setAttack(self):
        self.state = c.ATTACK

class ThreePeaShooter(Plant):
    def __init__(self, x, y, bullet_groups, map_y):
        Plant.__init__(self, x, y, c.THREEPEASHOOTER, c.PLANT_HEALTH, None)
        self.shoot_timer = 0
        self.map_y = map_y
        self.bullet_groups = bullet_groups

    def attacking(self):
        if (self.current_time - self.shoot_timer) > 2000:
            offset_y = 9 # modify bullet in the same y position with bullets of other plants
            for i in range(3):
                tmp_y = self.map_y + (i - 1)
                if tmp_y < 0 or tmp_y >= c.GRID_Y_LEN:
                    continue
                dest_y = self.rect.y + (i - 1) * c.GRID_Y_SIZE + offset_y
                self.bullet_groups[tmp_y].add(Bullet(self.rect.right, self.rect.y, dest_y,
                                        c.BULLET_PEA, c.BULLET_DAMAGE_NORMAL, False))
            self.shoot_timer = self.current_time
    
    def setAttack(self):
        self.state = c.ATTACK

class SnowPeaShooter(Plant):
    def __init__(self, x, y, bullet_group):
        Plant.__init__(self, x, y, c.SNOWPEASHOOTER, c.PLANT_HEALTH, bullet_group)
        self.shoot_timer = 0

    def attacking(self):
        if (self.current_time - self.shoot_timer) > 2000:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.y, self.rect.y,
                                    c.BULLET_PEA_ICE, c.BULLET_DAMAGE_NORMAL, True))
            self.shoot_timer = self.current_time

    def setAttack(self):
        self.state = c.ATTACK

class WallNut(Plant):
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.WALLNUT, c.WALLNUT_HEALTH, None)
        self.load_images()
        self.cracked1 = False
        self.cracked2 = False

    def load_images(self):
        self.cracked1_frames = []
        self.cracked2_frames = []
        
        cracked1_frames_name = self.name + '_cracked1'
        cracked2_frames_name = self.name + '_cracked2'

        self.loadFrames(self.cracked1_frames, cracked1_frames_name, 1)
        self.loadFrames(self.cracked2_frames, cracked2_frames_name, 1)
    
    def attacked(self):
        if not self.cracked1 and self.health <= c.WALLNUT_CRACKED1_HEALTH:
            self.frames = self.cracked1_frames
            self.frame_num = len(self.frames)
            self.frame_index = 0
            self.cracked1 = True
        elif not self.cracked2 and self.health <= c.WALLNUT_CRACKED2_HEALTH:
            self.frames = self.cracked2_frames
            self.frame_num = len(self.frames)
            self.frame_index = 0
            self.cracked2 = True

class CherryBomb(Plant):
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.CHERRYBOMB, c.WALLNUT_HEALTH, None)
        self.state = c.ATTACK
        self.start_boom = False
        self.bomb_timer = 0
    
    def setBoom(self):
        frame = tool.GFX[c.CHERRY_BOOM_IMAGE]
        rect = frame.get_rect()
        width, height = rect.w, rect.h
                
        old_rect = self.rect
        image = tool.get_image(frame, 0, 0, width, height, c.BLACK, 1)
        self.image = image
        self.rect = image.get_rect()
        self.rect.centerx = old_rect.centerx
        self.rect.centery = old_rect.centery
        self.start_boom = True

    def animation(self):
        if self.start_boom:
            if self.bomb_timer == 0:
                self.bomb_timer = self.current_time
            elif(self.current_time - self.bomb_timer) > 500:
                self.health = 0
        else:
            if (self.current_time - self.animate_timer) > 100:
                self.frame_index += 1
                if self.frame_index >= self.frame_num:
                    self.setBoom()
                    return
                self.animate_timer = self.current_time
            
            self.image = self.frames[self.frame_index]

