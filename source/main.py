__author__ = 'marble_xu'

from . import tool
from . import constants as c
from .state import mainmenu, screen, level

# 처음 시작할 때 호출
def main():
    game = tool.Control()
    state_dict = {c.MAIN_MENU: mainmenu.Menu(),
                  c.GAME_VICTORY: screen.GameVictoryScreen(),
                  c.GAME_LOSE: screen.GameLoseScreen(),
                  c.LEVEL: level.Level()}
    game.setup_states(state_dict, c.MAIN_MENU)
    game.main() # pygame 화면 재생 부분 (루프)