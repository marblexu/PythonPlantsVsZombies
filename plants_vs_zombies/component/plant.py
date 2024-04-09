__author__ = 'marble_xu'

import random
import pygame as pg
from .. import tool
from .. import constants as c

class Car(pg.sprite.Sprite):
    def __init__(self, x, y, map_y):
        pg.sprite.Sprite.__init__(self)

        rect = tool.GFX[c.CAR].get_rect()
        width, height = rect.w, rect.h
        self.image = tool.get_image(tool.GFX[c.CAR], 0, 0, width, height)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.map_y = map_y
        self.state = c.IDLE
        self.dead = False

    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        if self.state == c.IDLE:
            pass
        elif self.state == c.WALK:
            self.rect.x += 4
        if self.rect.x > c.SCREEN_WIDTH:
            self.dead = True

    def setWalk(self):
        if self.state == c.IDLE:
            self.state = c.WALK

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, start_y, dest_y, name, damage, ice):
        pg.sprite.Sprite.__init__(self)

        self.name = name
        self.frames = []
        self.frame_index = 0
        self.load_images()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
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
        if name in tool.PLANT_RECT:
            data = tool.PLANT_RECT[name]
            x, y, width, height = data['x'], data['y'], data['width'], data['height']
        else:
            x, y = 0, 0
            rect = frame_list[0].get_rect()
            width, height = rect.w, rect.h
        
        for frame in frame_list:
            frames.append(tool.get_image(frame, x, y, width, height))
    
    def load_images(self):
        self.fly_frames = []
        self.explode_frames = []
        
        fly_name = self.name
        if self.name == c.BULLET_MUSHROOM:
            explode_name = 'BulletMushRoomExplode'
        else:
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
        self.loadImages(name, scale)
        self.frame_num = len(self.frames)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        self.name = name
        self.health = health
        self.state = c.IDLE
        self.bullet_group = bullet_group
        self.can_sleep = False
        self.animate_timer = 0
        self.animate_interval = 100
        self.hit_timer = 0

    def loadFrames(self, frames, name, scale, color=c.BLACK):
        frame_list = tool.GFX[name]
        if name in tool.PLANT_RECT:
            data = tool.PLANT_RECT[name]
            x, y, width, height = data['x'], data['y'], data['width'], data['height']
        else:
            x, y = 0, 0
            rect = frame_list[0].get_rect()
            width, height = rect.w, rect.h

        for frame in frame_list:
            frames.append(tool.get_image(frame, x, y, width, height, color, scale))

    def loadImages(self, name, scale):
        self.loadFrames(self.frames, name, scale)

    def changeFrames(self, frames):
        '''change image frames and modify rect position'''
        self.frames = frames
        self.frame_num = len(self.frames)
        self.frame_index = 0
        
        bottom = self.rect.bottom
        x = self.rect.x
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.x = x

    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        self.handleState()
        self.animation()
    
    def handleState(self):
        if self.state == c.IDLE:
            self.idling()
        elif self.state == c.ATTACK:
            self.attacking()
        elif self.state == c.DIGEST:
            self.digest()

    def idling(self):
        pass

    def attacking(self):
        pass

    def digest(self):
        pass

    def animation(self):
        if (self.current_time - self.animate_timer) > self.animate_interval:
            self.frame_index += 1
            if self.frame_index >= self.frame_num:
                self.frame_index = 0
            self.animate_timer = self.current_time
        
        self.image = self.frames[self.frame_index]
        if(self.current_time - self.hit_timer) >= 200:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(192)

    def canAttack(self, zombie):
        if (self.state != c.SLEEP and zombie.state != c.DIE and
            self.rect.x <= zombie.rect.right):
            return True
        return False

    def setAttack(self):
        self.state = c.ATTACK

    def setIdle(self):
        self.state = c.IDLE
        self.is_attacked = False

    def setSleep(self):
        self.state = c.SLEEP
        self.changeFrames(self.sleep_frames)

    def setDamage(self, damage, zombie):
        self.health -= damage
        self.hit_timer = self.current_time
        if self.health == 0:
            self.kill_zombie = zombie

    def getPosition(self):
        return self.rect.centerx, self.rect.bottom

class Sun(Plant):
    def __init__(self, x, y, dest_x, dest_y, is_big=True):
        if is_big:
            scale = 0.9
            self.sun_value = c.SUN_VALUE
        else:
            scale = 0.6
            self.sun_value = 12
        Plant.__init__(self, x, y, c.SUN, 0, None, scale)
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

class RepeaterPea(Plant):
    def __init__(self, x, y, bullet_group):
        Plant.__init__(self, x, y, c.REPEATERPEA, c.PLANT_HEALTH, bullet_group)
        self.shoot_timer = 0

    def attacking(self):
        if (self.current_time - self.shoot_timer) > 2000:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.y, self.rect.y,
                                    c.BULLET_PEA, c.BULLET_DAMAGE_NORMAL, False))
            self.bullet_group.add(Bullet(self.rect.right + 40, self.rect.y, self.rect.y,
                                    c.BULLET_PEA, c.BULLET_DAMAGE_NORMAL, False))
            self.shoot_timer = self.current_time

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

class SnowPeaShooter(Plant):
    def __init__(self, x, y, bullet_group):
        Plant.__init__(self, x, y, c.SNOWPEASHOOTER, c.PLANT_HEALTH, bullet_group)
        self.shoot_timer = 0

    def attacking(self):
        if (self.current_time - self.shoot_timer) > 2000:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.y, self.rect.y,
                                    c.BULLET_PEA_ICE, c.BULLET_DAMAGE_NORMAL, True))
            self.shoot_timer = self.current_time

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
    
    def idling(self):
        if not self.cracked1 and self.health <= c.WALLNUT_CRACKED1_HEALTH:
            self.changeFrames(self.cracked1_frames)
            self.cracked1 = True
        elif not self.cracked2 and self.health <= c.WALLNUT_CRACKED2_HEALTH:
            self.changeFrames(self.cracked2_frames)
            self.cracked2 = True

class CherryBomb(Plant):
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.CHERRYBOMB, c.WALLNUT_HEALTH, None)
        self.state = c.ATTACK
        self.start_boom = False
        self.bomb_timer = 0
        self.explode_y_range = 1
        self.explode_x_range = c.GRID_X_SIZE
    
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

class Chomper(Plant):
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.CHOMPER, c.PLANT_HEALTH, None)
        self.animate_interval = 250
        self.digest_timer = 0
        self.digest_interval = 15000
        self.attack_zombie = None
        self.zombie_group = None

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.attack_frames = []
        self.digest_frames = []

        idle_name = name
        attack_name = name + 'Attack'
        digest_name = name + 'Digest'

        frame_list = [self.idle_frames, self.attack_frames, self.digest_frames]
        name_list = [idle_name, attack_name, digest_name]
        scale_list = [1, 1, 1]
        rect_list = [(0, 0, 100, 114), None, None]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, scale_list[i])

        self.frames = self.idle_frames

    def canAttack(self, zombie):
        if (self.state == c.IDLE and zombie.state != c.DIGEST and
            self.rect.x <= zombie.rect.right and
            (self.rect.right + c.GRID_X_SIZE//3 >= zombie.rect.x)):
            return True
        return False

    def setIdle(self):
        self.state = c.IDLE
        self.changeFrames(self.idle_frames)

    def setAttack(self, zombie, zombie_group):
        self.attack_zombie = zombie
        self.zombie_group = zombie_group
        self.state = c.ATTACK
        self.changeFrames(self.attack_frames)

    def setDigest(self):
        self.state = c.DIGEST
        self.changeFrames(self.digest_frames)

    def attacking(self):
        if self.frame_index == (self.frame_num - 3):
            self.zombie_group.remove(self.attack_zombie)
        if (self.frame_index + 1) == self.frame_num:
            self.setDigest()

    def digest(self):
        if self.digest_timer == 0:
            self.digest_timer = self.current_time
        elif (self.current_time - self.digest_timer) > self.digest_interval:
            self.digest_timer = 0
            self.attack_zombie.kill()
            self.setIdle()

class PuffShroom(Plant):
    def __init__(self, x, y, bullet_group):
        Plant.__init__(self, x, y, c.PUFFSHROOM, c.PLANT_HEALTH, bullet_group)
        self.can_sleep = True
        self.shoot_timer = 0

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.sleep_frames = []

        idle_name = name
        sleep_name = name + 'Sleep'
        
        frame_list = [self.idle_frames, self.sleep_frames]
        name_list = [idle_name, sleep_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1)

        self.frames = self.idle_frames

    def attacking(self):
        if (self.current_time - self.shoot_timer) > 3000:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.y + 10, self.rect.y + 10,
                                    c.BULLET_MUSHROOM, c.BULLET_DAMAGE_NORMAL, True))
            self.shoot_timer = self.current_time

    def canAttack(self, zombie):
        if (self.rect.x <= zombie.rect.right and
            (self.rect.right + c.GRID_X_SIZE * 4 >= zombie.rect.x)):
            return True
        return False

class PotatoMine(Plant):
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.POTATOMINE, c.PLANT_HEALTH, None)
        self.animate_interval = 300
        self.is_init = True
        self.init_timer = 0
        self.bomb_timer = 0
        self.explode_y_range = 0
        self.explode_x_range = c.GRID_X_SIZE//3 * 2

    def loadImages(self, name, scale):
        self.init_frames = []
        self.idle_frames = []
        self.explode_frames = []
        
        init_name = name + 'Init'
        idle_name = name
        explode_name = name + 'Explode'
        
        frame_list = [self.init_frames, self.idle_frames, self.explode_frames]
        name_list = [init_name, idle_name, explode_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1, c.WHITE)

        self.frames = self.init_frames

    def idling(self):
        if self.is_init:
            if self.init_timer == 0:
                self.init_timer = self.current_time
            elif (self.current_time - self.init_timer) > 15000:
                self.changeFrames(self.idle_frames)
                self.is_init = False

    def canAttack(self, zombie):
        if (not self.is_init and zombie.rect.right >= self.rect.x and
            (zombie.rect.x - self.rect.x) <= self.explode_x_range):
            return True
        return False

    def attacking(self):
        if self.bomb_timer == 0:
            self.bomb_timer = self.current_time
            self.changeFrames(self.explode_frames)
        elif (self.current_time - self.bomb_timer) > 500:
            self.health = 0

class Squash(Plant):
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.SQUASH, c.PLANT_HEALTH, None)
        self.orig_pos = (x, y)
        self.aim_timer = 0
        self.squashing = False

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.aim_frames = []
        self.attack_frames = []
        
        idle_name = name
        aim_name = name + 'Aim'
        attack_name = name + 'Attack'
        
        frame_list = [self.idle_frames, self.aim_frames, self.attack_frames]
        name_list = [idle_name, aim_name, attack_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1, c.WHITE)

        self.frames = self.idle_frames

    def canAttack(self, zombie):
        if (self.state == c.IDLE and self.rect.x <= zombie.rect.right and
            (self.rect.right + c.GRID_X_SIZE >= zombie.rect.x)):
            return True
        return False

    def setAttack(self, zombie, zombie_group):
        self.attack_zombie = zombie
        self.zombie_group = zombie_group
        self.state = c.ATTACK

    def attacking(self):
        if self.squashing:
            if self.frame_index == 2:
                self.zombie_group.remove(self.attack_zombie)
            if (self.frame_index + 1) == self.frame_num:
                self.attack_zombie.kill()
                self.health = 0
        elif self.aim_timer == 0:
            self.aim_timer = self.current_time
            self.changeFrames(self.aim_frames)
        elif (self.current_time - self.aim_timer) > 1000:
            self.changeFrames(self.attack_frames)
            self.rect.centerx = self.attack_zombie.rect.centerx
            self.squashing = True
            self.animate_interval = 300

    def getPosition(self):
        return self.orig_pos

class Spikeweed(Plant):
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.SPIKEWEED, c.PLANT_HEALTH, None)
        self.animate_interval = 200
        self.attack_timer = 0

    def loadImages(self, name, scale):
        self.loadFrames(self.frames, name, 0.9, c.WHITE)

    def setIdle(self):
        print('spikeweed idle')
        self.animate_interval = 200
        self.state = c.IDLE

    def canAttack(self, zombie):
        if (self.rect.x <= zombie.rect.right and
            (self.rect.right >= zombie.rect.x)):
            return True
        return False

    def setAttack(self, zombie_group):
        self.zombie_group = zombie_group
        self.animate_interval = 50
        self.state = c.ATTACK

    def attacking(self):
        if (self.current_time - self.attack_timer) > 2000:
            self.attack_timer = self.current_time
            for zombie in self.zombie_group:
                if self.canAttack(zombie):
                    zombie.setDamage(1, False)

class Jalapeno(Plant):
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.JALAPENO, c.PLANT_HEALTH, None)
        self.orig_pos = (x, y)
        self.state = c.ATTACK
        self.start_explode = False
        self.explode_y_range = 0
        self.explode_x_range = 377
        
    def loadImages(self, name, scale):
        self.explode_frames = []
        explode_name = name + 'Explode'
        self.loadFrames(self.explode_frames, explode_name, 1, c.WHITE)
        
        self.loadFrames(self.frames, name, 1, c.WHITE)

    def setExplode(self):
        self.changeFrames(self.explode_frames)
        self.animate_timer = self.current_time
        self.rect.x = c.MAP_OFFSET_X
        self.start_explode = True

    def animation(self):
        if self.start_explode:
            if(self.current_time - self.animate_timer) > 100:
                self.frame_index += 1
                if self.frame_index >= self.frame_num:
                    self.health = 0
                    return
                self.animate_timer = self.current_time
        else:
            if (self.current_time - self.animate_timer) > 100:
                self.frame_index += 1
                if self.frame_index >= self.frame_num:
                    self.setExplode()
                    return
                self.animate_timer = self.current_time
        self.image = self.frames[self.frame_index]

    def getPosition(self):
        return self.orig_pos

class ScaredyShroom(Plant):
    def __init__(self, x, y, bullet_group):
        Plant.__init__(self, x, y, c.SCAREDYSHROOM, c.PLANT_HEALTH, bullet_group)
        self.can_sleep = True
        self.shoot_timer = 0
        self.cry_x_range = c.GRID_X_SIZE * 2

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.cry_frames = []
        self.sleep_frames = []

        idle_name = name
        cry_name = name + 'Cry'
        sleep_name = name + 'Sleep'
        
        frame_list = [self.idle_frames, self.cry_frames, self.sleep_frames]
        name_list = [idle_name, cry_name, sleep_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1, c.WHITE)

        self.frames = self.idle_frames

    def needCry(self, zombie):
        if (zombie.state != c.DIE and self.rect.x <= zombie.rect.right and 
            self.rect.x + self.cry_x_range > zombie.rect.x):
            return True
        return False

    def setCry(self):
        self.state = c.CRY
        self.changeFrames(self.cry_frames)

    def setAttack(self):
        self.state = c.ATTACK
        self.changeFrames(self.idle_frames)

    def setIdle(self):
        self.state = c.IDLE
        self.changeFrames(self.idle_frames)

    def attacking(self):
        if (self.current_time - self.shoot_timer) > 2000:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.y + 40, self.rect.y + 40,
                                    c.BULLET_MUSHROOM, c.BULLET_DAMAGE_NORMAL, True))
            self.shoot_timer = self.current_time

class SunShroom(Plant):
    def __init__(self, x, y, sun_group):
        Plant.__init__(self, x, y, c.SUNSHROOM, c.PLANT_HEALTH, None)
        self.can_sleep = True
        self.animate_interval = 200
        self.sun_timer = 0
        self.sun_group = sun_group
        self.is_big = False
        self.change_timer = 0

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.big_frames = []
        self.sleep_frames = []

        idle_name = name
        big_name = name + 'Big'
        sleep_name = name + 'Sleep'
        
        frame_list = [self.idle_frames, self.big_frames, self.sleep_frames]
        name_list = [idle_name, big_name, sleep_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1, c.WHITE)

        self.frames = self.idle_frames

    def idling(self):
        if not self.is_big:
            if self.change_timer == 0:
                self.change_timer = self.current_time
            elif (self.current_time - self.change_timer) > 25000:
                self.changeFrames(self.big_frames)
                self.is_big = True
        
        if self.sun_timer == 0:
            self.sun_timer = self.current_time - (c.FLOWER_SUN_INTERVAL - 6000)
        elif (self.current_time - self.sun_timer) > c.FLOWER_SUN_INTERVAL:
            self.sun_group.add(Sun(self.rect.centerx, self.rect.bottom, self.rect.right,
                                   self.rect.bottom + self.rect.h // 2, self.is_big))
            self.sun_timer = self.current_time

class IceShroom(Plant):
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.ICESHROOM, c.PLANT_HEALTH, None)
        self.can_sleep = True
        self.orig_pos = (x, y)
        self.start_freeze = False

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.snow_frames = []
        self.sleep_frames = []
        self.trap_frames = []

        idle_name = name
        snow_name = name + 'Snow'
        sleep_name = name + 'Sleep'
        trap_name = name + 'Trap'
        
        frame_list = [self.idle_frames, self.snow_frames, self.sleep_frames, self.trap_frames]
        name_list = [idle_name, snow_name, sleep_name, trap_name]
        scale_list = [1, 1.5, 1, 1]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, scale_list[i], c.WHITE)

        self.frames = self.idle_frames

    def setFreeze(self):
        self.changeFrames(self.snow_frames)
        self.animate_timer = self.current_time
        self.rect.x = c.MAP_OFFSET_X
        self.rect.y = c.MAP_OFFSET_Y
        self.start_freeze = True

    def animation(self):
        if self.start_freeze:
            if(self.current_time - self.animate_timer) > 500:
                self.frame_index += 1
                if self.frame_index >= self.frame_num:
                    self.health = 0
                    return
                self.animate_timer = self.current_time
        else:
            if (self.current_time - self.animate_timer) > 100:
                self.frame_index += 1
                if self.frame_index >= self.frame_num:
                    if self.state == c.SLEEP:
                        self.frame_index = 0
                    else:
                        self.setFreeze()
                        return
                self.animate_timer = self.current_time
        self.image = self.frames[self.frame_index]

    def getPosition(self):
        return self.orig_pos

class HypnoShroom(Plant):
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.HYPNOSHROOM, 1, None)
        self.can_sleep = True
        self.animate_interval = 200

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.sleep_frames = []

        idle_name = name
        sleep_name = name + 'Sleep'

        frame_list = [self.idle_frames, self.sleep_frames]
        name_list = [idle_name, sleep_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1, c.WHITE)

        self.frames = self.idle_frames

class WallNutBowling(Plant):
    def __init__(self, x, y, map_y, level):
        Plant.__init__(self, x, y, c.WALLNUTBOWLING, 1, None)
        self.map_y = map_y
        self.level = level
        self.init_rect = self.rect.copy()
        self.rotate_degree = 0
        self.animate_interval = 200
        self.move_timer = 0
        self.move_interval = 70
        self.vel_x = random.randint(12, 15)
        self.vel_y = 0
        self.disable_hit_y = -1

    def loadImages(self, name, scale):
        self.loadFrames(self.frames, name, 1, c.WHITE)

    def idling(self):
        if self.move_timer == 0:
            self.move_timer = self.current_time
        elif (self.current_time - self.move_timer) >= self.move_interval:
            self.rotate_degree = (self.rotate_degree - 30) % 360
            self.init_rect.x += self.vel_x
            self.init_rect.y += self.vel_y
            self.handleMapYPosition()
            if self.shouldChangeDirection():
                self.changeDirection(-1)
            if self.init_rect.x > c.SCREEN_WIDTH:
                self.health = 0
            self.move_timer += self.move_interval

    def canHit(self, map_y):
        if self.disable_hit_y == map_y:
            return False
        return True

    def handleMapYPosition(self):
        _, map_y1 = self.level.map.getMapIndex(self.init_rect.x, self.init_rect.centery)
        _, map_y2 = self.level.map.getMapIndex(self.init_rect.x, self.init_rect.bottom)
        if self.map_y != map_y1 and map_y1 == map_y2:
            # wallnut bowls to another row, should modify which plant group it belongs to
            self.level.plant_groups[self.map_y].remove(self)
            self.level.plant_groups[map_y1].add(self)
            self.map_y = map_y1

    def shouldChangeDirection(self):
        if self.init_rect.centery <= c.MAP_OFFSET_Y:
            return True
        elif self.init_rect.bottom + 20 >= c.SCREEN_HEIGHT:
            return True
        return False

    def changeDirection(self, map_y):
        if self.vel_y == 0:
            if self.map_y == 0:
                direc = 1
            elif self.map_y == (c.GRID_Y_LEN-1):
                direc = -1
            else:
                if random.randint(0, 1) == 0:
                    direc = 1
                else:
                    direc = -1
            self.vel_y = self.vel_x * direc
        else:
            self.vel_y = - self.vel_y

        self.disable_hit_y = map_y

    def animation(self):
        if (self.current_time - self.animate_timer) > self.animate_interval:
            self.frame_index += 1
            if self.frame_index >= self.frame_num:
                self.frame_index = 0
            self.animate_timer = self.current_time
            
        image = self.frames[self.frame_index]
        self.image = pg.transform.rotate(image, self.rotate_degree)
        # must keep the center postion of image when rotate
        self.rect = self.image.get_rect(center=self.init_rect.center)

class RedWallNutBowling(Plant):
    def __init__(self, x, y):
        Plant.__init__(self, x, y, c.REDWALLNUTBOWLING, 1, None)
        self.orig_y = y
        self.explode_timer = 0
        self.explode_y_range = 1
        self.explode_x_range = c.GRID_X_SIZE
        self.init_rect = self.rect.copy()
        self.rotate_degree = 0
        self.animate_interval = 200
        self.move_timer = 0
        self.move_interval = 70
        self.vel_x = random.randint(12, 15)

    def loadImages(self, name, scale):
        self.idle_frames = []
        self.explode_frames = []

        idle_name = name
        explode_name = name + 'Explode'
        
        frame_list = [self.idle_frames, self.explode_frames]
        name_list = [idle_name, explode_name]

        for i, name in enumerate(name_list):
            self.loadFrames(frame_list[i], name, 1, c.WHITE)

        self.frames = self.idle_frames

    def idling(self):
        if self.move_timer == 0:
            self.move_timer = self.current_time
        elif (self.current_time - self.move_timer) >= self.move_interval:
            self.rotate_degree = (self.rotate_degree - 30) % 360
            self.init_rect.x += self.vel_x
            if self.init_rect.x > c.SCREEN_WIDTH:
                self.health = 0
            self.move_timer += self.move_interval

    def attacking(self):
        if self.explode_timer == 0:
            self.explode_timer = self.current_time
            self.changeFrames(self.explode_frames)
        elif (self.current_time - self.explode_timer) > 500:
            self.health = 0

    def animation(self):
        if (self.current_time - self.animate_timer) > self.animate_interval:
            self.frame_index += 1
            if self.frame_index >= self.frame_num:
                self.frame_index = 0
            self.animate_timer = self.current_time

        image = self.frames[self.frame_index]
        if self.state == c.IDLE:
            self.image = pg.transform.rotate(image, self.rotate_degree)
        else:
            self.image = image
        # must keep the center postion of image when rotate
        self.rect = self.image.get_rect(center=self.init_rect.center)

    def getPosition(self):
        return (self.rect.centerx, self.orig_y)