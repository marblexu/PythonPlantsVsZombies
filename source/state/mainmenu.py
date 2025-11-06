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
        
    def setupOption(self):
        # Adventure mode option
        self.adventure_option_frames = []
        adventure_frame_names = [c.OPTION_ADVENTURE + '_0', c.OPTION_ADVENTURE + '_1']
        frame_rect = [0, 0, 165, 77]
        
        for name in adventure_frame_names:
            self.adventure_option_frames.append(tool.get_image(tool.GFX[name], *frame_rect, c.BLACK, 1.7))
        
        self.adventure_option_frame_index = 0
        self.adventure_option_image = self.adventure_option_frames[self.adventure_option_frame_index]
        self.adventure_option_rect = self.adventure_option_image.get_rect()
        self.adventure_option_rect.x = 435
        self.adventure_option_rect.y = 75
        
        # Endless mode option
        self.endless_option_frames = []
        endless_frame_names = [c.OPTION_ENDLESS + '_0', c.OPTION_ENDLESS + '_1']
        
        for name in endless_frame_names:
            self.endless_option_frames.append(tool.get_image(tool.GFX[name], *frame_rect, c.BLACK, 1.7))
        
        self.endless_option_frame_index = 0
        self.endless_option_image = self.endless_option_frames[self.endless_option_frame_index]
        self.endless_option_rect = self.endless_option_image.get_rect()
        self.endless_option_rect.x = 435
        self.endless_option_rect.y = 180
        
        self.option_start = 0
        self.option_timer = 0
        self.adventure_option_clicked = False
        self.endless_option_clicked = False
    
    def checkOptionClick(self, mouse_pos):
        x, y = mouse_pos
        # Check adventure mode click
        if(x >= self.adventure_option_rect.x and x <= self.adventure_option_rect.right and
           y >= self.adventure_option_rect.y and y <= self.adventure_option_rect.bottom):
            self.adventure_option_clicked = True
            self.option_timer = self.option_start = self.current_time
            self.next = c.LEVEL
            return True
        # Check endless mode click
        elif(x >= self.endless_option_rect.x and x <= self.endless_option_rect.right and
           y >= self.endless_option_rect.y and y <= self.endless_option_rect.bottom):
            self.endless_option_clicked = True
            self.option_timer = self.option_start = self.current_time
            self.next = c.ENDLESS_MODE
            return True
        return False
        
    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        # Handle adventure mode button
        if not self.adventure_option_clicked and not self.endless_option_clicked:
            if mouse_pos:
                self.checkOptionClick(mouse_pos)
        else:
            # Animate clicked button
            if self.adventure_option_clicked:
                if(self.current_time - self.option_timer) > 200:
                    self.adventure_option_frame_index += 1
                    if self.adventure_option_frame_index >= 2:
                        self.adventure_option_frame_index = 0
                    self.option_timer = self.current_time
                    self.adventure_option_image = self.adventure_option_frames[self.adventure_option_frame_index]
            elif self.endless_option_clicked:
                if(self.current_time - self.option_timer) > 200:
                    self.endless_option_frame_index += 1
                    if self.endless_option_frame_index >= 2:
                        self.endless_option_frame_index = 0
                    self.option_timer = self.current_time
                    self.endless_option_image = self.endless_option_frames[self.endless_option_frame_index]
            
            if(self.current_time - self.option_start) > 1300:
                self.done = True

        surface.blit(self.bg_image, self.bg_rect)
        surface.blit(self.adventure_option_image, self.adventure_option_rect)
        surface.blit(self.endless_option_image, self.endless_option_rect)