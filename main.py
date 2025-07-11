import pygame as pg
from source.main import main

if __name__ == '__main__':
   
    pg.init()
    pg.mixer.init()
    
    try:
       
        pg.mixer.music.load(r"D:\Laura Shigihara - Faster.ogg")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)  
        
        
        main()
        
    except pg.error as e:
        print(f"无法加载或播放音乐: {e}")
        
        
    finally:
        
        pg.mixer.music.stop()
        pg.quit()
