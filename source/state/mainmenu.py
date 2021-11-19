__author__ = 'marble_xu'

import pygame as pg
from .. import tool
from .. import constants as c

class Menu(tool.State):
    def __init__(self):
        tool.State.__init__(self)
    
    def startup(self, current_time, persist):
        self.next = c.LEVEL
        self.persist = persist
        self.game_info = persist
        
        self.setupBackground()
        self.setupOption()
        
        

    def setupBackground(self):
        frame_rect = [80, 0, 800, 600]
        self.bg_image = tool.get_image(tool.GFX[c.MAIN_MENU_IMAGE], *frame_rect)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0

        #left top right bottom
        frame_rect2 = [0,0,73,71]
        self.test_img = tool.get_image(tool.GFX[c.TEST_IMAGE],*frame_rect2)
        self.test_img_rect = self.test_img.get_rect()
        self.test_img_rect.x = 450
        self.test_img_rect.y = 300

        self.isclicked = False
        
    def setupOption(self):
        self.option_frames = []
        frame_names = [c.OPTION_ADVENTURE + '_0', c.OPTION_ADVENTURE + '_1']
        frame_rect = [0, 0, 165, 77]
        
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
            self.option_timer = self.option_start = self.current_time
        return False

    def checkOptionClick2(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.test_img_rect.x and x <= self.test_img_rect.right and
           y >= self.test_img_rect.y and y <= self.test_img_rect.bottom):
            self.isclicked = True
           
        
    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        if not self.option_clicked:
            if mouse_pos:
                self.checkOptionClick(mouse_pos)
                self.checkOptionClick2(mouse_pos)
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
         surface.blit(self.test_img,self.test_img_rect)
        else:
          pg.quit()
       
       
       