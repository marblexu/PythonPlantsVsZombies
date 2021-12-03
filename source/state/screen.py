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

    def update(self, surface, current_time, mouse_pos, mouse_click):
        # Displaying component when the game ended.
        surface.fill(c.WHITE)
        surface.blit(self.image, self.rect)

class GameVictoryScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
    
    def getImageName(self):
        return c.GAME_VICTORY_IMAGE
    
    def set_next_state(self):
        return c.LEVEL

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
        
    def startup(self, current_time, persist):
        super().startup(current_time, persist)
        #텍스트 추가
        font = pg.font.SysFont("arial",30,True,True)  #폰트 설정
        self.text = font.render("KILL ZOMBIES : " + str(tool.GameManager.getInstance().getKillZombieCount()),True,(0,0,0))  #텍스트가 표시된 Surface 를 만듬
        #self.textForTime = font.render("PLAY TIME : " + str(int(tool.GameManager.getInstance().getTimer())) + "SECOND",True,(0,0,0))
        minuteForRenderStr = 0
        secondForRenderStr = 0
        if int(tool.GameManager.getInstance().getTimer()) >= 60 :
            minuteForRenderStr = int(tool.GameManager.getInstance().getTimer()) / 60
            secondForRenderStr = int(tool.GameManager.getInstance().getTimer()) % 60
            self.textForTime = font.render("PLAY TIME : " + str(int(minuteForRenderStr)) + " MINUTE " + str(secondForRenderStr) + " SECOND",True,(0,0,0))
            self.textPos = [150, 330]
        elif int(tool.GameManager.getInstance().getTimer()) < 60 :
            self.textForTime = font.render("PLAY TIME : " + str(int(tool.GameManager.getInstance().getTimer())) + " SECOND",True,(0,0,0))
            self.textPos = [200, 330]


    def setupImage(self, name):
        super().setupImage(name)
        # Setup For MainMenu Button
        mainMenu_Button = [0, 0, 150, 80]
        self.mainMenuButton_IMG = tool.get_image(tool.GFX[c.GAMEFINISHED_MAINMENU_BUTTON],*mainMenu_Button)
        self.mainMenuButton_IMG_rect = self.mainMenuButton_IMG.get_rect()
        self.mainMenuButton_IMG_rect.x = 235
        self.mainMenuButton_IMG_rect.y = 380
        self.isMainMenuClicked = False

        # Setup For NextStage Button
        nextStage_Button = [0, 0, 150, 80]
        self.nextStageButton_IMG = tool.get_image(tool.GFX[c.GAMEFINISHED_NEXTSTAGE_BUTTON],*nextStage_Button)
        self.nextStageButton_IMG_rect = self.nextStageButton_IMG.get_rect()
        self.nextStageButton_IMG_rect.x = 435
        self.nextStageButton_IMG_rect.y = 380
        self.isNextStageClicked = False

    def update(self, surface, current_time, mouse_pos, mouse_click):
        super().update(surface, current_time, mouse_pos, mouse_click)
        if mouse_pos:
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
                tool.GameManager.getInstance().resetKillZombieCount()
                self.done = True
            elif self.isNextStageClicked :
                tool.GameManager.getInstance().resetKillZombieCount()
                self.done = True

        surface.blit(self.text,(290,280))
        surface.blit(self.textForTime, self.textPos)
        surface.blit(self.mainMenuButton_IMG, self.mainMenuButton_IMG_rect)
        surface.blit(self.nextStageButton_IMG, self.nextStageButton_IMG_rect)

class GameLoseScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
    
    def getImageName(self):
        return c.GAME_LOOSE_IMAGE
    
    def set_next_state(self):
        return c.MAIN_MENU
    
    def checkMainMenuButtonClicked(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.mainMenuButton_IMG_rect.x and x <= self.mainMenuButton_IMG_rect.right and
           y >= self.mainMenuButton_IMG_rect.y and y <= self.mainMenuButton_IMG_rect.bottom):
            self.isMainMenuClicked = True    
    
    def startup(self, current_time, persist):
        super().startup(current_time, persist)
        #텍스트 추가
        font = pg.font.SysFont("arial",30,True,True)  #폰트 설정
        self.text = font.render("KILL ZOMBIES : " + str(tool.GameManager.getInstance().getKillZombieCount()),True,(0,0,0))  #텍스트가 표시된 Surface 를 만듬
    
    def setupImage(self, name):
        super().setupImage(name)
        # Setup For MainMenu Button
        mainMenu_Button = [0, 0, 150, 80]
        self.mainMenuButton_IMG = tool.get_image(tool.GFX[c.GAMEFINISHED_MAINMENU_BUTTON],*mainMenu_Button)
        self.mainMenuButton_IMG_rect = self.mainMenuButton_IMG.get_rect()
        self.mainMenuButton_IMG_rect.x = 310
        self.mainMenuButton_IMG_rect.y = 380
        self.isMainMenuClicked = False
    
    def update(self, surface, current_time, mouse_pos, mouse_click):
        super().update(surface, current_time, mouse_pos, mouse_click)
        if mouse_pos:
            self.checkMainMenuButtonClicked(mouse_pos)   
            if self.isMainMenuClicked :
                tool.GameManager.getInstance().resetKillZombieCount()
                self.done = True

        surface.blit(self.text,(280,300))
        surface.blit(self.mainMenuButton_IMG, self.mainMenuButton_IMG_rect)