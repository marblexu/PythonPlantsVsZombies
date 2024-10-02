# menu.py
import pygame as pg
import sys

def main_menu():
    # Inicialização do Pygame
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption('Python Plants vs Zombies - Menu')
    clock = pg.time.Clock()

    # Configuração da fonte e do texto do menu
    font = pg.font.SysFont(None, 55)
    start_text = font.render('Pressione SPACE para começar', True, (255, 255, 255))

    show_menu = True

    while show_menu:
        screen.fill((0, 0, 0))
        screen.blit(start_text, (100, 250))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    show_menu = False  # Sai do loop do menu

        pg.display.flip()
        clock.tick(60)
