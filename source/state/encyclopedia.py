__author__ = 'marble_xu'

import pygame as pg
from .. import tool
from .. import constants as c

class Encyclopedia(tool.State):
    def __init__(self):
        tool.State.__init__(self)
        self.setup_background()
        self.setup_buttons()
        self.setup_zombie_list()
        self.setup_text()
        self.scroll_offset = 0
    
    def setup_background(self):
        """设置背景"""
        self.bg_color = c.NAVYBLUE
    
    def setup_buttons(self):
        """设置按钮"""
        self.back_button_rect = pg.Rect(600, 500, 150, 50)
    
    def setup_zombie_list(self):
        """设置僵尸列表"""
        # 这里可以根据实际游戏中的僵尸类型进行扩展
        self.zombies = [
            {
                "name": "普通僵尸",
                "description": "最基本的僵尸，移动速度慢，攻击力低",
                "image_key": "Zombie"
            },
            {
                "name": "路障僵尸",
                "description": "头上戴着路障，防御力更高",
                "image_key": "ConeheadZombie"
            },
            {
                "name": "铁桶僵尸",
                "description": "头上戴着铁桶，防御力非常高",
                "image_key": "BucketheadZombie"
            }
        ]
        
        # 计算每个僵尸条目的位置
        self.zombie_entries = []
        for i, zombie in enumerate(self.zombies):
            rect = pg.Rect(50, 100 + i * 150, 300, 120)
            self.zombie_entries.append((zombie, rect))
    
    def setup_text(self):
        """设置文本"""
        self.font = pg.font.Font(None, 36)
        self.small_font = pg.font.Font(None, 24)
    
    def startup(self, current_time, persist):
        """初始化状态"""
        self.next = c.SHOP
        self.persist = persist
        self.game_info = persist
        self.current_time = current_time
        self.mouse_pos = None
        self.mouse_click = False
        self.selected_zombie = None
    
    def update(self, surface, current_time, mouse_pos, mouse_click):
        """更新状态"""
        self.current_time = current_time
        self.mouse_pos = mouse_pos
        self.mouse_click = mouse_click
        
        if self.mouse_click and self.mouse_pos:
            self.handle_click(self.mouse_pos)
        
        self.draw(surface)
    
    def handle_click(self, mouse_pos):
        """处理鼠标点击"""
        x, y = mouse_pos
        
        # 处理返回按钮
        if self.back_button_rect.collidepoint(x, y):
            self.done = True
            return
        
        # 处理僵尸列表点击
        for zombie, rect in self.zombie_entries:
            if rect.collidepoint(x, y):
                self.selected_zombie = zombie
                break
    
    def draw(self, surface):
        """绘制图鉴界面"""
        # 填充背景
        surface.fill(self.bg_color)
        
        # 绘制标题
        title_text = self.font.render("僵尸图鉴", True, c.GOLD)
        title_rect = title_text.get_rect(center=(c.SCREEN_WIDTH // 2, 50))
        surface.blit(title_text, title_rect)
        
        # 绘制僵尸列表
        for zombie, rect in self.zombie_entries:
            # 绘制条目框
            pg.draw.rect(surface, c.WHITE, rect, 2)
            
            # 绘制僵尸名称
            name_text = self.font.render(zombie['name'], True, c.WHITE)
            name_rect = name_text.get_rect(topleft=(rect.x + 10, rect.y + 10))
            surface.blit(name_text, name_rect)
            
            # 绘制僵尸描述
            desc_text = self.small_font.render(zombie['description'], True, c.LIGHTYELLOW)
            desc_rect = desc_text.get_rect(topleft=(rect.x + 10, rect.y + 50))
            surface.blit(desc_text, desc_rect)
        
        # 绘制返回按钮
        pg.draw.rect(surface, c.RED, self.back_button_rect)
        back_text = self.font.render("返回商店", True, c.WHITE)
        back_rect = back_text.get_rect(center=self.back_button_rect.center)
        surface.blit(back_text, back_rect)
        
        # 绘制选中的僵尸详细信息
        if self.selected_zombie:
            self.draw_zombie_detail(surface, self.selected_zombie)
    
    def draw_zombie_detail(self, surface, zombie):
        """绘制选中僵尸的详细信息"""
        # 绘制详细信息面板
        detail_rect = pg.Rect(400, 100, 350, 350)
        pg.draw.rect(surface, c.WHITE, detail_rect, 3)
        
        # 绘制僵尸名称
        name_text = self.font.render(zombie['name'], True, c.GOLD)
        name_rect = name_text.get_rect(center=(detail_rect.centerx, detail_rect.y + 30))
        surface.blit(name_text, name_rect)
        
        # 绘制僵尸图像
        if zombie['image_key'] in tool.GFX:
            zombie_image = tool.GFX[zombie['image_key']][0]  # 取第一张帧
            # 缩放图像
            scaled_image = pg.transform.scale(zombie_image, (150, 150))
            image_rect = scaled_image.get_rect(center=(detail_rect.centerx, detail_rect.y + 150))
            surface.blit(scaled_image, image_rect)
        
        # 绘制僵尸描述
        desc_text = self.small_font.render(zombie['description'], True, c.LIGHTYELLOW)
        desc_rect = desc_text.get_rect(center=(detail_rect.centerx, detail_rect.y + 300))
        surface.blit(desc_text, desc_rect)