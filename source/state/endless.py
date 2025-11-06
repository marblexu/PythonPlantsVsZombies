__author__ = 'marble_xu'

import os
import json
import pygame as pg
import math
from .. import tool
from .. import constants as c
from ..component import map, plant, zombie, menubar

class EndlessMode(tool.State):
    def __init__(self):
        tool.State.__init__(self)
    
    def startup(self, current_time, persist):
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.map_y_len = c.GRID_Y_LEN
        self.map = map.Map(c.GRID_X_LEN, self.map_y_len)
        
        # Endless mode specific variables
        self.current_wave = 1
        self.threat_level = 1.0
        self.wave_in_progress = False
        self.interval_timer = 0
        self.interval_duration = 10000  # 10 seconds
        self.zombies_spawned = 0
        self.zombies_killed = 0
        self.zombies_in_wave = 0
        
        self.loadMap()
        self.setupBackground()
        self.initState()
    
    def loadMap(self):
        # For endless mode, we'll use a default map
        self.map_data = {
            c.BACKGROUND_TYPE: c.BACKGROUND_DAY,
            c.CHOOSEBAR_TYPE: c.CHOOSEBAR_STATIC,
            c.INIT_SUN_NAME: 50,
            c.CARD_POOL: ['SunFlower', 'Peashooter', 'SnowPea', 'WallNut', 'CherryBomb'],
            c.ZOMBIE_LIST: []  # We'll generate zombies dynamically
        }
    
    def setupBackground(self):
        img_index = self.map_data[c.BACKGROUND_TYPE]
        self.background_type = img_index
        self.background = tool.GFX[c.BACKGROUND_NAME][img_index]
        self.bg_rect = self.background.get_rect()

        self.level = pg.Surface((self.bg_rect.w, self.bg_rect.h)).convert()
        self.viewport = tool.SCREEN.get_rect(bottom=self.bg_rect.bottom)
        self.viewport.x += c.BACKGROUND_OFFSET_X
    
    def setupGroups(self):
        self.sun_group = pg.sprite.Group()
        self.head_group = pg.sprite.Group()

        self.plant_groups = []
        self.zombie_groups = []
        self.hypno_zombie_groups = [] #zombies who are hypno after eating hypnoshroom
        self.bullet_groups = []
        for i in range(self.map_y_len):
            self.plant_groups.append(pg.sprite.Group())
            self.zombie_groups.append(pg.sprite.Group())
            self.hypno_zombie_groups.append(pg.sprite.Group())
            self.bullet_groups.append(pg.sprite.Group())
    
    def initState(self):
        if c.CHOOSEBAR_TYPE in self.map_data:
            self.bar_type = self.map_data[c.CHOOSEBAR_TYPE]
        else:
            self.bar_type = c.CHOOSEBAR_STATIC

        if self.bar_type == c.CHOOSEBAR_STATIC:
            self.initChoose()
        else:
            card_pool = menubar.getCardPool(self.map_data[c.CARD_POOL])
            self.initPlay(card_pool)
            if self.bar_type == c.CHOSSEBAR_BOWLING:
                self.initBowlingMap()
    
    def initChoose(self):
        self.state = c.CHOOSE
        self.panel = menubar.Panel(menubar.all_card_list, self.map_data[c.INIT_SUN_NAME])
    
    def choose(self, mouse_pos, mouse_click):
        if mouse_pos and mouse_click[0]:
            self.panel.checkCardClick(mouse_pos)
            if self.panel.checkStartButtonClick(mouse_pos):
                self.initPlay(self.panel.getSelectedCards())
    
    def initPlay(self, card_list):
        self.state = c.PLAY
        if self.bar_type == c.CHOOSEBAR_STATIC:
            self.menubar = menubar.MenuBar(card_list, self.map_data[c.INIT_SUN_NAME])
        else:
            self.menubar = menubar.MoveBar(card_list)
        self.drag_plant = False
        self.hint_image = None
        self.hint_plant = False
        if self.background_type == c.BACKGROUND_DAY and self.bar_type == c.CHOOSEBAR_STATIC:
            self.produce_sun = True
        else:
            self.produce_sun = False
        self.sun_timer = self.current_time

        self.removeMouseImage()
        self.setupGroups()
        self.setupCars()
        
        # Start first wave
        self.startNewWave()
    
    def setupCars(self):
        self.cars = []
        for i in range(self.map_y_len):
            _, y = self.map.getMapGridPos(0, i)
            self.cars.append(plant.Car(-25, y+20, i))
    
    def startNewWave(self):
        self.wave_in_progress = True
        self.zombies_spawned = 0
        self.zombies_killed = 0
        
        # Calculate number of zombies in this wave
        self.zombies_in_wave = max(5, int(3 * self.current_wave * self.threat_level))
        
        # Generate zombie list for this wave
        self.generateZombieWave()
        
        print(f"Wave {self.current_wave} started! Threat Level: {self.threat_level:.1f}")
    
    def generateZombieWave(self):
        self.zombie_list = []
        spawn_interval = 1000  # Base spawn interval
        
        for i in range(self.zombies_in_wave):
            # Determine zombie type based on threat level
            zombie_type = self.getZombieType()
            # Random row
            map_y = i % self.map_y_len
            # Calculate spawn time
            spawn_time = i * spawn_interval
            
            self.zombie_list.append((spawn_time, zombie_type, map_y))
    
    def getZombieType(self):
        import random
        
        if self.threat_level < 5:
            # Only normal and conehead zombies
            return random.choice([c.NORMAL_ZOMBIE, c.CONEHEAD_ZOMBIE])
        elif 5 <= self.threat_level < 10:
            # High frequency buckethead zombies
            zombie_types = [c.NORMAL_ZOMBIE, c.CONEHEAD_ZOMBIE, c.BUCKETHEAD_ZOMBIE]
            weights = [0.3, 0.3, 0.4]  # 40% buckethead
            return random.choices(zombie_types, weights=weights)[0]
        else:
            # Squad generation
            return self.generateSquad()
    
    def generateSquad(self):
        import random
        
        # Randomly choose a squad type
        squad_types = [
            [c.BUCKETHEAD_ZOMBIE, c.NORMAL_ZOMBIE, c.NORMAL_ZOMBIE],  # Tank with guards
            [c.CONEHEAD_ZOMBIE, c.CONEHEAD_ZOMBIE, c.NORMAL_ZOMBIE],   # Mixed squad
            [c.BUCKETHEAD_ZOMBIE, c.CONEHEAD_ZOMBIE, c.NORMAL_ZOMBIE]   # Stronger mixed
        ]
        
        return random.choice(random.choice(squad_types))
    
    def createZombie(self, zombie_name, map_y):
        # Calculate enhanced attributes based on threat level
        if zombie_name == c.NORMAL_ZOMBIE:
            base_health = c.NORMAL_HEALTH
        elif zombie_name == c.CONEHEAD_ZOMBIE:
            base_health = c.CONEHEAD_HEALTH
        elif zombie_name == c.BUCKETHEAD_ZOMBIE:
            base_health = c.BUCKETHEAD_HEALTH
        elif zombie_name == c.FLAG_ZOMBIE:
            base_health = c.FLAG_HEALTH
        elif zombie_name == c.NEWSPAPER_ZOMBIE:
            base_health = c.NEWSPAPER_HEALTH
        else:
            base_health = c.NORMAL_HEALTH
        
        # Enhanced health and speed
        enhanced_health = int(base_health * self.threat_level)
        enhanced_speed = 1 * math.sqrt(self.threat_level)
        
        # Create zombie
        x, y = self.map.getMapGridPos(c.GRID_X_LEN, map_y)
        new_zombie = zombie.Zombie(x, y, zombie_name, enhanced_health, self.head_group)
        new_zombie.speed = enhanced_speed
        
        self.zombie_groups[map_y].add(new_zombie)
        self.zombies_spawned += 1
    
    def checkWaveComplete(self):
        # Check if all zombies in wave are killed
        total_zombies = sum(len(group) for group in self.zombie_groups) + sum(len(group) for group in self.hypno_zombie_groups)
        
        if total_zombies == 0 and self.zombies_spawned >= self.zombies_in_wave:
            self.wave_in_progress = False
            self.interval_timer = self.current_time
            
            # Increase threat level
            self.threat_level += 0.1
            self.current_wave += 1
            
            print(f"Wave {self.current_wave - 1} completed! Next wave in 10 seconds...")
    
    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        if self.state == c.CHOOSE:
            self.choose(mouse_pos, mouse_click)
        elif self.state == c.PLAY:
            self.play(mouse_pos, mouse_click)

        self.draw(surface)
    
    def play(self, mouse_pos, mouse_click):
        # Handle sun production
        if self.produce_sun:
            if (self.current_time - self.sun_timer) > c.PRODUCE_SUN_INTERVAL:
                self.sun_timer = self.current_time
                # Create sun
                pass
        
        # Handle zombie spawning
        if self.wave_in_progress and len(self.zombie_list) > 0:
            data = self.zombie_list[0]
            if data[0] <= (self.current_time - self.interval_timer):
                self.createZombie(data[1], data[2])
                self.zombie_list.remove(data)
        
        # Handle interval between waves
        elif not self.wave_in_progress:
            if (self.current_time - self.interval_timer) > self.interval_duration:
                self.startNewWave()
        
        # Update all groups
        for i in range(self.map_y_len):
            self.bullet_groups[i].update(self.game_info)
            self.plant_groups[i].update(self.game_info)
            self.zombie_groups[i].update(self.game_info)
            self.hypno_zombie_groups[i].update(self.game_info)
            for zombie in self.hypno_zombie_groups[i]:
                if zombie.rect.x > c.SCREEN_WIDTH:
                    zombie.kill()

        self.head_group.update(self.game_info)
        self.sun_group.update(self.game_info)
        
        # Check wave completion
        self.checkWaveComplete()
    
    def draw(self, surface):
        surface.blit(self.background, self.bg_rect)
        
        # Draw wave information
        font = pg.font.Font(None, 36)
        wave_text = font.render(f"Wave: {self.current_wave}", True, c.WHITE)
        threat_text = font.render(f"Threat: {self.threat_level:.1f}", True, c.WHITE)
        
        surface.blit(wave_text, (10, 10))
        surface.blit(threat_text, (10, 50))
        
        # Draw map and plants
        self.map.draw(self.level)
        for i in range(self.map_y_len):
            for plant in self.plant_groups[i]:
                plant.draw(self.level)
        
        # Draw zombies
        for i in range(self.map_y_len):
            for zombie in self.zombie_groups[i]:
                zombie.draw(self.level)
            for zombie in self.hypno_zombie_groups[i]:
                zombie.draw(self.level)
        
        # Draw bullets
        for i in range(self.map_y_len):
            for bullet in self.bullet_groups[i]:
                bullet.draw(self.level)
        
        # Draw UI elements
        surface.blit(self.level, self.viewport, self.viewport)
        
        if self.state == c.CHOOSE:
            self.panel.draw(surface)
        else:
            self.menubar.update(self.game_info)
            self.menubar.draw(surface)
            
            # Draw sun
            for sun in self.sun_group:
                sun.draw(surface)
            
            # Draw hint
            if self.hint_image:
                surface.blit(self.hint_image, self.hint_rect)
            
            # Draw mouse image
            if self.mouse_image:
                surface.blit(self.mouse_image, self.mouse_rect)