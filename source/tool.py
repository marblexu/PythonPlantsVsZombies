from pygame.locals import *
__author__ = 'marble_xu'

import os
import json
from abc import abstractmethod
import pygame as pg
import sys
from . import constants as c
mainClock = pg.time.Clock()

#싱글톤 패턴으로 어디서든 호출할 수 있도록 만듬


class GameManager(object):
    __instance = None

    def __init__(self):
        self.killZombieCount = 0
        self.startTimer = 0.0
        self.timer = 0.0
        self.score = 0
        self.timeBuf = 0.0

        self.current_time = 0.0
        self.current_startTimer = 0.0
        self.current_timeBuf = 0.0
    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = GameManager()
        return cls.__instance

    def getKillZombieCount(self):
        return self.killZombieCount

    def addKillZombieCount(self):
        self.killZombieCount += 1

    def resetKillZombieCount(self):
        self.killZombieCount = 0

    def getTimer(self):
        return self.timer
    def addTimer(self):
        self.timer = ((pg.time.get_ticks()-self.startTimer) / (1000/c.DELTA_TIME)) + self.timeBuf
    def getTimerToTicks(self):
        return self.timer * 1000
    def reSetTimer(self):
        self.startTimer = pg.time.get_ticks()
        self.timeBuf = 0.0
    def reSetStartTimer(self):
        self.startTimer = pg.time.get_ticks()
        self.timeBuf = self.timer

    def getCurrentTimer(self):
        return self.current_time
    def setCurrentTimer(self):
        self.current_time = pg.time.get_ticks()
        self.current_timeBuf = 0.0
    def addCurrentTimer(self):
        self.current_time = ((pg.time.get_ticks()-self.current_startTimer) * c.DELTA_TIME) + self.current_timeBuf
    def reSetCurrentTimer(self):
        self.current_startTimer = pg.time.get_ticks()
        self.current_timeBuf = self.current_time
    
   
class State():
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.next = None
        self.persist = {}

    @abstractmethod
    def startup(self, current_time, persist):
        '''abstract method'''

    def cleanup(self):
        self.done = False
        return self.persist

    @abstractmethod
    def update(self, surface, keys, current_time):
        '''abstract method'''


class Control():
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60
        self.keys = pg.key.get_pressed()
        self.mouse_pos = None
        # value:[left mouse click, right mouse click]
        self.mouse_click = [False, False]
        self.current_time = 0.0
        self.state_dict = {}
        self.state_name = None
        self.state = None
        self.game_info = {c.CURRENT_TIME: 0.0,
                          c.LEVEL_NUM: c.START_LEVEL_NUM}   
        GameManager.getInstance().setCurrentTimer()

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, self.game_info)

    def update(self):
        #self.current_time = pg.time.get_ticks() * c.DELTA_TIME
        GameManager.getInstance().addCurrentTimer()
        self.current_time = GameManager.getInstance().getCurrentTimer()
        print(self.current_time)

        if self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.current_time,
                          self.mouse_pos, self.mouse_click)
        self.mouse_pos = None
        self.mouse_click[0] = False
        self.mouse_click[1] = False

    def flip_state(self):
        #화면 직접적으로 바꾸어 주는 부분
        #현재 state를 state.next로 바꾸어 줌
        #state.next는 State 자식클래스들 startup()에서 지정
        #한 씬에서 여러가지 씬으로 변경할수 있는경우에는 어떻게 처리해야 할지?
        #->level.py에 def checkGameState(self) 함수 참고
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)

    """def event_loop(self):
        #SCREEN = pg.display.set_mode(c.SCREEN_SIZE, pg.RESIZABLE)
        #SCREEN.fill((0, 0, 50))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_pos = pg.mouse.get_pos()
                self.mouse_click[0], _, self.mouse_click[1] = pg.mouse.get_pressed()
                print('pos:', self.mouse_pos, ' mouse:', self.mouse_click)"""

    def event_loop(self):
        fullscreen = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.VIDEORESIZE:
                if not fullscreen:
                    SCREEN = pg.display.set_mode(
                        (event.w, event.h), pg.RESIZABLE)
            if event.type == pg.KEYDOWN:
                #self.keys = pg.key.get_pressed()
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        SCREEN = pg.display.set_mode(
                            monitor_size, pg.FULLSCREEN)
                    else:
                        SCREEN = pg.display.set_mode(
                            (SCREEN.get_width(), SCREEN.get_height()), pg.RESIZABLE)
            if event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_pos = pg.mouse.get_pos()
                self.mouse_click[0], _, self.mouse_click[1] = pg.mouse.get_pressed(
                )
                print('pos:', self.mouse_pos, ' mouse:', self.mouse_click)

    def setBackGroundMusic(self):
        self.sound_dir = os.path.join('source', 'sound')  # 경로 추가
        pg.mixer.music.load(os.path.join(
            self.sound_dir, '배경음악.mp3'))  # 배경음악 로드

    def main(self):

        self.setBackGroundMusic()
        pg.mixer.music.play(-1)  # 게임이 시작하면 노래를 재생합니다

        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)
        pg.mixer.music.fadeout(500)  # 게임이 끝나면 노래를 종료합니다
        print('game over')


def get_image(sheet, x, y, width, height, colorkey=c.BLACK, scale=1):
    image = pg.Surface([width, height])
    rect = image.get_rect()

    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pg.transform.scale(image,
                               (int(rect.width*scale),
                                int(rect.height*scale)))
    return image


def get_image(sheet, x, y, width, height, colorkey=c.BLACK, scale=1):
    image = pg.Surface([width, height])
    rect = image.get_rect()

    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pg.transform.scale(image,
                               (int(rect.width*scale),
                                int(rect.height*scale)))
    return image


def load_image_frames(directory, image_name, colorkey, accept):
    frame_list = []
    tmp = {}
    # image_name is "Peashooter", pic name is 'Peashooter_1', get the index 1
    index_start = len(image_name) + 1
    frame_num = 0
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            index = int(name[index_start:])
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            tmp[index] = img
            frame_num += 1

    for i in range(frame_num):
        frame_list.append(tmp[i])
    return frame_list


def load_all_gfx(directory, colorkey=c.WHITE, accept=('.png', '.jpg', '.bmp', '.gif')):
    graphics = {}
    for name1 in os.listdir(directory):
        # subfolders under the folder resources\graphics
        dir1 = os.path.join(directory, name1)
        if os.path.isdir(dir1):
            for name2 in os.listdir(dir1):
                dir2 = os.path.join(dir1, name2)
                if os.path.isdir(dir2):
                    # e.g. subfolders under the folder resources\graphics\Zombies
                    for name3 in os.listdir(dir2):
                        dir3 = os.path.join(dir2, name3)
                        # e.g. subfolders or pics under the folder resources\graphics\Zombies\ConeheadZombie
                        if os.path.isdir(dir3):
                            # e.g. it's the folder resources\graphics\Zombies\ConeheadZombie\ConeheadZombieAttack
                            image_name, _ = os.path.splitext(name3)
                            graphics[image_name] = load_image_frames(
                                dir3, image_name, colorkey, accept)
                        else:
                            # e.g. pics under the folder resources\graphics\Plants\Peashooter
                            image_name, _ = os.path.splitext(name2)
                            graphics[image_name] = load_image_frames(
                                dir2, image_name, colorkey, accept)
                            break
                else:
                    # e.g. pics under the folder resources\graphics\Screen
                    name, ext = os.path.splitext(name2)
                    if ext.lower() in accept:
                        img = pg.image.load(dir2)
                        if img.get_alpha():
                            img = img.convert_alpha()
                        else:
                            img = img.convert()
                            img.set_colorkey(colorkey)
                        graphics[name] = img
    return graphics


def loadZombieImageRect():
    file_path = os.path.join('source', 'data', 'entity', 'zombie.json')
    f = open(file_path)
    data = json.load(f)
    f.close()
    return data[c.ZOMBIE_IMAGE_RECT]


def loadPlantImageRect():
    file_path = os.path.join('source', 'data', 'entity', 'plant.json')
    f = open(file_path)
    data = json.load(f)
    f.close()
    return data[c.PLANT_IMAGE_RECT]


pg.init()
pg.display.set_caption(c.ORIGINAL_CAPTION)
monitor_size = [pg.display.Info().current_w, pg.display.Info().current_h]
SCREEN = pg.display.set_mode(c.SCREEN_SIZE, pg.RESIZABLE)
GFX = load_all_gfx(os.path.join("resources", "graphics"))
ZOMBIE_RECT = loadZombieImageRect()
PLANT_RECT = loadPlantImageRect()
mainClock.tick(60)
