__author__ = 'marble_xu'

from . import tool
from . import constants as c
from .state import mainmenu, screen, level, shop, encyclopedia

def main():
    game = tool.Control()
    state_dict = {c.MAIN_MENU: mainmenu.Menu(),
                  c.GAME_VICTORY: screen.GameVictoryScreen(),
                  c.GAME_LOSE: screen.GameLoseScreen(),
                  c.LEVEL: level.Level(),
                  c.SHOP: shop.Shop(),
                  c.ENCYCLOPEDIA: encyclopedia.Encyclopedia()}
    game.setup_states(state_dict, c.MAIN_MENU)
    game.main()