__author__ = 'marble_xu'

import pygame as pg
from .. import tool
from .. import constants as c

class Screen(tool.State):
    def __init__(self):
        tool.State.__init__(self)
        self.end_time = 3000

    def startup(self, current_time, persist):
        self.start_time = current_time
        self.next = c.LEVEL
        self.persist = persist
        self.game_info = persist
        name = self.getImageName()
        self.setupImage(name)
        self.next = self.set_next_state()

        #텍스트 추가
        font = pg.font.SysFont("arial",30,True,True)  #폰트 설정
        self.text = font.render("KILL ZOMBIES : " + str(tool.GameManager.getInstance().getKillZombieCount()),True,(0,0,0))  #텍스트가 표시된 Surface 를 만듬

    def getImageName(self):
        pass

    def set_next_state(self):
        pass

    def setupImage(self, name):
        frame_rect = [0, 0, 800, 600]
        self.image = tool.get_image(tool.GFX[name], *frame_rect)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        # Setup For MainMenu Button
        mainMenu_Button = [0, 0, 150, 80]
        self.mainMenuButton_IMG = tool.get_image(tool.GFX[c.GAMEFINISHED_MAINMENU_BUTTON],*mainMenu_Button)
        self.mainMenuButton_IMG_rect = self.mainMenuButton_IMG.get_rect()
        self.mainMenuButton_IMG_rect.x = 250
        self.mainMenuButton_IMG_rect.y = 380

        # Setup For NextStage Button
        nextStage_Button = [0, 0, 150, 80]
        self.nextStageButton_IMG = tool.get_image(tool.GFX[c.GAMEFINISHED_NEXTSTAGE_BUTTON],*nextStage_Button)
        self.nextStageButton_IMG_rect = self.nextStageButton_IMG.get_rect()
        self.nextStageButton_IMG_rect.x = 450
        self.nextStageButton_IMG_rect.y = 380

        self.isMainMenuClicked = False
        self.isNextStageClicked = False

    # Mouse Position checking method
    def checkNextStageButtonClicked(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.nextStageButton_IMG_rect.x and x <= self.nextStageButton_IMG_rect.right and
           y >= self.nextStageButton_IMG_rect.y and y <= self.nextStageButton_IMG_rect.bottom):
            self.isNextStageClicked = True

    def checkMainMenuButtonClicked(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.mainMenuButton_IMG_rect.x and x <= self.mainMenuButton_IMG_rect.right and
           y >= self.mainMenuButton_IMG_rect.y and y <= self.mainMenuButton_IMG_rect.bottom):
            self.isMainMenuClicked = True    

    def update(self, surface, current_time, mouse_pos, mouse_click):
        """#startup()에서 end_time을 3000으로 초기화해서 
        #이기든 지든 3초 지나면 자동으로 next state로 넘어감
        if(current_time - self.start_time) < self.end_time:
            #뒷 배경을 WHITE로
            surface.fill(c.WHITE)
            surface.blit(self.image, self.rect)
        else:
            tool.GameManager.getInstance().resetKillZombieCount()
            self.done = True

        #텍스트 출력
        surface.blit(self.text,(300,300))"""
        if mouse_pos :
            self.checkMainMenuButtonClicked(mouse_pos)
            self.checkNextStageButtonClicked(mouse_pos)   

            if self.isMainMenuClicked :
                if self.game_info[c.LEVEL_NUM] == 1 :
                    self.game_info[c.LEVEL_NUM] -= 1
                elif self.game_info[c.LEVEL_NUM] == 2:
                    self.game_info[c.LEVEL_NUM] -= 2
                elif self.game_info[c.LEVEL_NUM] == 3:
                    self.game_info[c.LEVEL_NUM] -= 3
                elif self.game_info[c.LEVEL_NUM] == 4:
                    self.game_info[c.LEVEL_NUM] -= 4
                elif self.game_info[c.LEVEL_NUM] == 5:
                    self.game_info[c.LEVEL_NUM] -= 5
                self.next = c.MAIN_MENU
                self.done = True

            elif self.isNextStageClicked :
                tool.GameManager.getInstance().resetKillZombieCount()
                self.done = True

        # Displaying component when the game ended.
        surface.fill(c.WHITE)
        surface.blit(self.image, self.rect)
        surface.blit(self.text,(300,300))
        surface.blit(self.mainMenuButton_IMG, self.mainMenuButton_IMG_rect)
        surface.blit(self.nextStageButton_IMG, self.nextStageButton_IMG_rect)

    def update(self, surface, current_time, mouse_pos, mouse_click):
        if(current_time - self.start_time) < self.end_time:
            surface.fill(c.WHITE)
            surface.blit(self.image, self.rect)
        else:
            self.done = True

class GameVictoryScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
    
    def getImageName(self):
        return c.GAME_VICTORY_IMAGE
    
    def set_next_state(self):
        return c.LEVEL

class GameLoseScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
    
    def getImageName(self):
        return c.GAME_LOOSE_IMAGE
    
    def set_next_state(self):
        return c.MAIN_MENU