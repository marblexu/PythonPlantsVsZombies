__author__ = 'marble_xu'

import os
import pygame as pg
from .. import tool
from .. import constants as c

class Menu(tool.State):
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
        self.gameoff_img_rect.x = 460
        self.gameoff_img_rect.y = 350
        self.isclicked = False

    def setupMuteSound(self):
        mutesound_rect = [0, 0, 72, 44]
        self.mutesound_img = tool.get_image(tool.GFX[c.SOUND_MUTE_IMAGE],*mutesound_rect)
        self.mutesound_img_rect = self.mutesound_img.get_rect()
        self.mutesound_img_rect.x = 460
        self.mutesound_img_rect.y = 290
        self.muteSoundClicked = False

    def ClickedMuteSound(self):
        clickedMutesound_rect = [0, 0, 72, 44]
        self.clickedMutesound_img = tool.get_image(tool.GFX[c.CLICKED_MUTE_IMAGE],*clickedMutesound_rect)
        self.clickedMutesound_img_rect = self.clickedMutesound_img.get_rect()
        self.clickedMutesound_img_rect.x = 460
        self.clickedMutesound_img_rect.y = 290

    def setupSound(self):
        sound_rect = [0, 0, 72, 44]
        self.sound_img = tool.get_image(tool.GFX[c.SOUND_IMAGE],*sound_rect)
        self.sound_img_rect = self.sound_img.get_rect()
        self.sound_img_rect.x = 560
        self.sound_img_rect.y = 290
        self.soundClicked = False

    def ClickedSound(self):
        clickedsound_rect = [0, 0, 72, 44]
        self.clickedSound_img = tool.get_image(tool.GFX[c.CLICKED_SOUND_IMAGE],*clickedsound_rect)
        self.clickedSound_img_rect = self.clickedSound_img.get_rect()
        self.clickedSound_img_rect.x = 560
        self.clickedSound_img_rect.y = 290
        
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
            self.start_sound.play()                                         #소리재생
            self.option_timer = self.option_start = self.current_time
        return False

    def checkGameOffClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.gameoff_img_rect.x and x <= self.gameoff_img_rect.right and
           y >= self.gameoff_img_rect.y and y <= self.gameoff_img_rect.bottom):
            self.isclicked = True

    def checkMuteSoundClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.mutesound_img_rect.x and x <= self.mutesound_img_rect.right and
           y >= self.mutesound_img_rect.y and y <= self.mutesound_img_rect.bottom):
            self.muteSoundClicked = True

            #self.start_sound.play()
            #self.option_clicked = True
            #self.option_timer = self.option_start = self.current_time
        #return False

    def checkSoundClick(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.sound_img_rect.x and x <= self.sound_img_rect.right and
           y >= self.sound_img_rect.y and y <= self.sound_img_rect.bottom):
            self.soundClicked = True

    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        if not self.option_clicked:
            if mouse_pos:
                self.checkOptionClick(mouse_pos)
                self.checkGameOffClick(mouse_pos)
                self.checkSoundClick(mouse_pos)
                self.checkMuteSoundClick(mouse_pos)
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

        if(self.isclicked == False):
            surface.blit(self.gameoff_img,self.gameoff_img_rect)
        else:
            pg.quit()


        if(self.muteSoundClicked == False):
            surface.blit(self.mutesound_img, self.mutesound_img_rect)
            if(self.soundClicked == True):
                self.setupSound()         
        else:
            surface.blit(self.clickedMutesound_img, self.clickedMutesound_img_rect)
            pg.mixer.music.pause()

        if(self.soundClicked == False):
            surface.blit(self.sound_img, self.sound_img_rect)
        else:
            surface.blit(self.clickedSound_img, self.clickedSound_img_rect)
            pg.mixer.music.unpause()
            self.setupMuteSound()
            #self.checkMuteSoundClick(mouse_pos)

        
        
       
