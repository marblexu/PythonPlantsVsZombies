# main.py
import pygame as pg
from source.main import main as game_main
from menu import main_menu

if __name__ == '__main__':
    # Inicialização do Pygame
    pg.init()
    
    # Exibição do menu inicial
    print("Exibindo menu...")
    main_menu()
    print("Iniciando o jogo após o menu...")
    
    # Inicialização do jogo
    game_main()
    
    # Encerramento do Pygame
    pg.quit()
    print("Jogo encerrado.")
