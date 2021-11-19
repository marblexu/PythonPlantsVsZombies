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

        #여기서 결과창에 추가할것들 넣어주기
        #죽인 좀비수, 스코어, 클리어 시간, 다음 스테이지, 메인 메뉴로 버튼, 스코어에 따라 별 갯수 띄워주기도 OK
        
    def update(self, surface, current_time, mouse_pos, mouse_click):
        #startup()에서 end_time을 3000으로 초기화해서 
        #이기든 지든 3초 지나면 자동으로 next state로 넘어감
        if(current_time - self.start_time) < self.end_time:
            #뒷 배경을 WHITE로
            surface.fill(c.WHITE)
            surface.blit(self.image, self.rect)
        else:
            self.done = True

        #텍스트 출력
        surface.blit(self.text,(300,300))

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