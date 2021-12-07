__author__ = 'marble_xu'

import os
import pygame as pg
from .. import tool
from .. import constants as c

class Menu(tool.State):
    isClickedSoundBtn = True               #사운드가 켜져있는지
    
    def __init__(self):
        tool.State.__init__(self)
        self.sound_dir = os.path.join('source','sound')  #경로 추가
        self.start_sound = pg.mixer.Sound(os.path.join(self.sound_dir, '게임시작버튼.mp3'))  #버튼을 누르는 소리
        self.start_sound.set_volume(2)                                                      #소리크기 설정
    
    def startup(self, current_time, persist):
        self.next = c.LEVEL
        self.persist = persist
        self.game_info = persist
        
        self.setupBackground()

        self.setupMuteSound()
        self.ClickedMuteSound()
        self.setupSound()
        self.ClickedSound()

        self.setupEasyMode()
        self.ClickedEasyMode()
        self.setupNormalMode()
        self.ClickedNormalMode()
        self.setupHardMode()
        self.ClickedHardMode()

        self.setupOption()
        
    def setupBackground(self):
        frame_rect = [80, 0, 800, 600]
        self.bg_image = tool.get_image(tool.GFX[c.MAIN_MENU_IMAGE], *frame_rect)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0

        gameoff_rect = [0, 0 ,165 , 60]
        self.gameoff_img = tool.get_image(tool.GFX[c.OPTION_GAMEOFF],*gameoff_rect)
        self.gameoff_img_rect = self.gameoff_img.get_rect()
        self.gameoff_img_rect.x = 450
        self.gameoff_img_rect.y = 340
        self.gameOffclicked = False

    def setupMuteSound(self):
        mutesound_rect = [0, 0, 99, 55]
        self.mutesound_img = tool.get_image(tool.GFX[c.SOUND_MUTE_IMAGE],*mutesound_rect)
        self.mutesound_img_rect = self.mutesound_img.get_rect()
        self.mutesound_img_rect.x = 440
        self.mutesound_img_rect.y = 265
        self.muteSoundClicked = False

    def ClickedMuteSound(self):
        clickedMutesound_rect = [0, 0, 99, 55]
        self.clickedMutesound_img = tool.get_image(tool.GFX[c.CLICKED_MUTE_IMAGE],*clickedMutesound_rect)
        self.clickedMutesound_img_rect = self.clickedMutesound_img.get_rect()
        self.clickedMutesound_img_rect.x = 440
        self.clickedMutesound_img_rect.y = 265

    def setupSound(self):
        sound_rect = [0, 0, 99, 55]
        self.sound_img = tool.get_image(tool.GFX[c.SOUND_IMAGE],*sound_rect)
        self.sound_img_rect = self.sound_img.get_rect()
        self.sound_img_rect.x = 550
        self.sound_img_rect.y = 275
        self.soundClicked = False

    def ClickedSound(self):
        clickedsound_rect = [0, 0, 99, 55]
        self.clickedSound_img = tool.get_image(tool.GFX[c.CLICKED_SOUND_IMAGE],*clickedsound_rect)
        self.clickedSound_img_rect = self.clickedSound_img.get_rect()
        self.clickedSound_img_rect.x = 550
        self.clickedSound_img_rect.y = 275
        
    def setupEasyMode(self):
        easyMode_rect = [0, 0, 99, 55]
        self.easyMode_img = tool.get_image(tool.GFX[c.EASY_IMAGE],*easyMode_rect)
        self.easyMode_img_rect = self.easyMode_img.get_rect()
        self.easyMode_img_rect.x = 410
        self.easyMode_img_rect.y = 190
        self.easyClicked = False

    def ClickedEasyMode(self):
        clickedEasy_rect = [0, 0, 99, 55]
        self.clickedEasy_img = tool.get_image(tool.GFX[c.CLICKED_EASY],*clickedEasy_rect)
        self.clickedEasy_img_rect = self.clickedEasy_img.get_rect()
        self.clickedEasy_img_rect.x = 410
        self.clickedEasy_img_rect.y = 190

    def setupNormalMode(self):
        normalMode_rect = [0, 0, 99, 55]
        self.normalMode_img = tool.get_image(tool.GFX[c.NORMAL_IMAGE],*normalMode_rect)
        self.normalMode_img_rect = self.normalMode_img.get_rect()
        self.normalMode_img_rect.x = 510
        self.normalMode_img_rect.y = 200
        self.normalClicked = False

    def ClickedNormalMode(self):
        clickedNormal_rect = [0, 0, 99, 55]
        self.clickedNormal_img = tool.get_image(tool.GFX[c.CLICKED_NORMAL],*clickedNormal_rect)
        self.clickedNormal_img_rect = self.clickedNormal_img.get_rect()
        self.clickedNormal_img_rect.x = 510
        self.clickedNormal_img_rect.y = 200

    def setupHardMode(self):
        hardMode_rect = [0, 0, 99, 55]
        self.hardMode_img = tool.get_image(tool.GFX[c.HARD_IMAGE],*hardMode_rect)
        self.hardMode_img_rect = self.hardMode_img.get_rect()
        self.hardMode_img_rect.x = 610
        self.hardMode_img_rect.y = 210
        self.hardClicked = False

    def ClickedHardMode(self):
        clickedHard_rect = [0, 0, 99, 55]
        self.clickedHard_img = tool.get_image(tool.GFX[c.CLICKED_HARD],*clickedHard_rect)
        self.clickedHard_img_rect = self.clickedHard_img.get_rect()
        self.clickedHard_img_rect.x = 610
        self.clickedHard_img_rect.y = 210

    def setupOption(self):
        self.option_frames = []
        frame_names = [c.OPTION_ADVENTURE + '_0', c.OPTION_ADVENTURE + '_1']
        frame_rect = [0, 0, 165, 70]
        
        for name in frame_names:
            self.option_frames.append(tool.get_image(tool.GFX[name], *frame_rect, c.BLACK, 1.7))
        
        self.option_frame_index = 0
        self.option_image = self.option_frames[self.option_frame_index]
        self.option_rect = self.option_image.get_rect()
        self.option_rect.x = 435
        self.option_rect.y = 75
        
        self.option_start = 0
        self.option_timer = 0
        self.option_clicked = False
    
    def checkOptionClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.option_rect.x and x <= self.option_rect.right and
           y >= self.option_rect.y and y <= self.option_rect.bottom):
            self.option_clicked = True
            if(self.isClickedSoundBtn) :
                self.start_sound.play()                                         #소리재생
            self.option_timer = self.option_start = self.current_time
        return False

    def checkGameOffClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.gameoff_img_rect.x and x <= self.gameoff_img_rect.right and
           y >= self.gameoff_img_rect.y and y <= self.gameoff_img_rect.bottom):
            self.gameOffclicked = True

    def checkMuteSoundClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.mutesound_img_rect.x and x <= self.mutesound_img_rect.right and
           y >= self.mutesound_img_rect.y and y <= self.mutesound_img_rect.bottom):
            self.muteSoundClicked = True
            Menu.isClickedSoundBtn = False

    def checkSoundClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.sound_img_rect.x and x <= self.sound_img_rect.right and
           y >= self.sound_img_rect.y and y <= self.sound_img_rect.bottom):
            self.soundClicked = True
            Menu.isClickedSoundBtn = True

    def checkEasyClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.easyMode_img_rect.x and x <= self.easyMode_img_rect.right and
           y >= self.easyMode_img_rect.y and y <= self.easyMode_img_rect.bottom):
            self.easyClicked = True

    def checkNormalClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.normalMode_img_rect.x and x <= self.normalMode_img_rect.right and
           y >= self.normalMode_img_rect.y and y <= self.normalMode_img_rect.bottom):
            self.normalClicked = True

    def checkHardClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.hardMode_img_rect.x and x <= self.hardMode_img_rect.right and
           y >= self.hardMode_img_rect.y and y <= self.hardMode_img_rect.bottom):
            self.hardClicked = True

    def easyConfig(self):
        c.SUN_VALUE = 30
        c.PLANT_HEALTH = 10

        c.LOSTHEAD_HEALTH = 3
        c.NORMAL_HEALTH = 5
        c.FLAG_HEALTH = 8
        c.CONEHEAD_HEALTH = 10
        c.BUCKETHEAD_HEALTH = 15
        c.NEWSPAPER_HEALTH = 8

    def hardConfig(self):
        c.SUN_VALUE = 20
        c.WALLNUT_HEALTH = 20

        c.LOSTHEAD_HEALTH = 7
        c.NORMAL_HEALTH = 15
        c.FLAG_HEALTH = 22
        c.CONEHEAD_HEALTH = 30
        c.BUCKETHEAD_HEALTH = 45
        c.NEWSPAPER_HEALTH = 22
        c.DELTA_TIME = 2.0

        c.ICE_SLOW_TIME = 5000

    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        if not self.option_clicked:
            if mouse_pos:
                self.checkOptionClick(mouse_pos)
                self.checkGameOffClick(mouse_pos)
                self.checkSoundClick(mouse_pos)
                self.checkMuteSoundClick(mouse_pos)
                self.checkEasyClick(mouse_pos)
                self.checkNormalClick(mouse_pos)
                self.checkHardClick(mouse_pos)
        else:
            if(self.current_time - self.option_timer) > 200:
                self.option_frame_index += 1
                if self.option_frame_index >= 2:
                    self.option_frame_index = 0
                self.option_timer = self.current_time
                self.option_image = self.option_frames[self.option_frame_index]
            #클릭후 1.3초후 self.done = True
            #self.done이 True가 되면? 
            #1. tool.py 의 Update에서 걸림
            #2. flip_state()함수에서 현재 state를 다음 state로 넘겨 다른 state.update()가 호출
            #즉!!! State를 상속받은 클래스는 done을 true해주면 무조건 다음 state로 넘어감!!
            if(self.current_time - self.option_start) > 1300: 
                self.done = True

        surface.blit(self.bg_image, self.bg_rect)
        surface.blit(self.option_image, self.option_rect)
        
        #게임 종료 
        if(self.gameOffclicked == False):
            surface.blit(self.gameoff_img,self.gameoff_img_rect)
        else:
            pg.quit()            
        
        #소리 설정
        if(self.muteSoundClicked == False and self.soundClicked == False):
            surface.blit(self.sound_img, self.sound_img_rect)
            surface.blit(self.mutesound_img, self.mutesound_img_rect)
        elif(self.muteSoundClicked == True and self.soundClicked == False):
            surface.blit(self.clickedMutesound_img, self.clickedMutesound_img_rect)
            surface.blit(self.sound_img, self.sound_img_rect)
            pg.mixer.music.pause()
            self.muteSoundClicked = False

        elif(self.muteSoundClicked == False and self.soundClicked == True):
            surface.blit(self.clickedSound_img, self.clickedSound_img_rect)
            surface.blit(self.mutesound_img, self.mutesound_img_rect)
            pg.mixer.music.unpause()
            self.soundClicked = False

        #난이도 설정
        if(self.easyClicked == False):
            surface.blit(self.easyMode_img, self.easyMode_img_rect)
        else:
            surface.blit(self.clickedEasy_img, self.clickedEasy_img_rect)
            self.easyConfig()

        if(self.normalClicked == False):
            surface.blit(self.normalMode_img, self.normalMode_img_rect)
        else:
            surface.blit(self.clickedNormal_img, self.clickedNormal_img_rect)
            #self.normalConfig()

        if(self.hardClicked == False):
            surface.blit(self.hardMode_img, self.hardMode_img_rect)
        else:
            surface.blit(self.clickedHard_img, self.clickedHard_img_rect)
            self.hardConfig()


    def isClickedSound(self) :
        return Menu.isClickedSoundBtn

