__author__ = 'marble_xu'

import pygame as pg
import json
import os
from .. import tool
from .. import constants as c

class Shop(tool.State):
    def __init__(self):
        tool.State.__init__(self)
        self.save_file_path = 'save_data.json'
        self.load_save_data()
        self.setup_shop_items()
        self.setup_background()
        self.setup_buttons()
        self.setup_text()
    
    def load_save_data(self):
        """加载保存数据"""
        if os.path.exists(self.save_file_path):
            with open(self.save_file_path, 'r') as f:
                self.save_data = json.load(f)
        else:
            self.save_data = {
                "gold": 0,
                "upgrades": {
                    "gold_shovel": False,
                    "extra_slot": False,
                    "zombie_encyclopedia": False
                }
            }
            self.save_save_data()
    
    def save_save_data(self):
        """保存数据到文件"""
        with open(self.save_file_path, 'w') as f:
            json.dump(self.save_data, f, indent=2)
    
    def setup_shop_items(self):
        """设置商店商品"""
        self.items = [
            {
                "name": "黄金铲子",
                "description": "铲除植物时返还25%的阳光消耗",
                "price": 1000,
                "upgrade_key": "gold_shovel",
                "rect": pg.Rect(100, 100, 200, 100)
            },
            {
                "name": "额外卡槽",
                "description": "永久解锁第7个植物卡槽",
                "price": 5000,
                "upgrade_key": "extra_slot",
                "rect": pg.Rect(400, 100, 200, 100)
            },
            {
                "name": "僵尸图鉴",
                "description": "解锁僵尸图鉴功能",
                "price": 500,
                "upgrade_key": "zombie_encyclopedia",
                "rect": pg.Rect(100, 250, 200, 100)
            }
        ]
    
    def setup_background(self):
        """设置背景"""
        self.bg_color = c.NAVYBLUE
    
    def setup_buttons(self):
        """设置按钮"""
        self.back_button_rect = pg.Rect(600, 500, 150, 50)
        self.encyclopedia_button_rect = pg.Rect(400, 250, 200, 100)
    
    def setup_text(self):
        """设置文本"""
        self.font = pg.font.Font(None, 36)
        self.small_font = pg.font.Font(None, 24)
    
    def startup(self, current_time, persist):
        """初始化状态"""
        self.next = c.MAIN_MENU
        self.persist = persist
        self.game_info = persist
        self.current_time = current_time
        self.mouse_pos = None
        self.mouse_click = False
    
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
        
        # 处理图鉴按钮（如果已购买）
        if self.save_data['upgrades']['zombie_encyclopedia'] and \
           self.encyclopedia_button_rect.collidepoint(x, y):
            self.next = c.ENCYCLOPEDIA
            self.done = True
            return
        
        # 处理商品购买
        for item in self.items:
            if item['rect'].collidepoint(x, y):
                self.attempt_purchase(item)
                break
    
    def attempt_purchase(self, item):
        """尝试购买商品"""
        upgrade_key = item['upgrade_key']
        if not self.save_data['upgrades'][upgrade_key]:
            if self.save_data['gold'] >= item['price']:
                # 购买成功
                self.save_data['gold'] -= item['price']
                self.save_data['upgrades'][upgrade_key] = True
                self.save_save_data()
    
    def draw(self, surface):
        """绘制商店界面"""
        # 填充背景
        surface.fill(self.bg_color)
        
        # 绘制标题
        title_text = self.font.render("疯狂戴夫的商店", True, c.GOLD)
        title_rect = title_text.get_rect(center=(c.SCREEN_WIDTH // 2, 50))
        surface.blit(title_text, title_rect)
        
        # 绘制金币数量
        gold_text = self.font.render(f"金币: {self.save_data['gold']}", True, c.YELLOW)
        gold_rect = gold_text.get_rect(topleft=(50, 50))
        surface.blit(gold_text, gold_rect)
        
        # 绘制商品
        for item in self.items:
            is_purchased = self.save_data['upgrades'][item['upgrade_key']]
            
            # 绘制商品框
            if is_purchased:
                pg.draw.rect(surface, c.GREEN, item['rect'], 3)
            else:
                pg.draw.rect(surface, c.WHITE, item['rect'], 3)
            
            # 绘制商品名称
            name_text = self.font.render(item['name'], True, c.WHITE)
            name_rect = name_text.get_rect(center=(item['rect'].centerx, item['rect'].y + 30))
            surface.blit(name_text, name_rect)
            
            # 绘制商品价格
            if not is_purchased:
                price_text = self.small_font.render(f"价格: {item['price']} 金币", True, c.YELLOW)
            else:
                price_text = self.small_font.render("已购买", True, c.GREEN)
            price_rect = price_text.get_rect(center=(item['rect'].centerx, item['rect'].y + 60))
            surface.blit(price_text, price_rect)
            
            # 绘制商品描述
            desc_text = self.small_font.render(item['description'], True, c.LIGHTYELLOW)
            desc_rect = desc_text.get_rect(center=(item['rect'].centerx, item['rect'].y + 90))
            surface.blit(desc_text, desc_rect)
        
        # 绘制返回按钮
        pg.draw.rect(surface, c.RED, self.back_button_rect)
        back_text = self.font.render("返回主菜单", True, c.WHITE)
        back_rect = back_text.get_rect(center=self.back_button_rect.center)
        surface.blit(back_text, back_rect)
        
        # 如果已购买图鉴，绘制图鉴按钮
        if self.save_data['upgrades']['zombie_encyclopedia']:
            pg.draw.rect(surface, c.BLUE, self.encyclopedia_button_rect)
            ency_text = self.font.render("僵尸图鉴", True, c.WHITE)
            ency_rect = ency_text.get_rect(center=self.encyclopedia_button_rect.center)
            surface.blit(ency_text, ency_rect)