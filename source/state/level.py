__author__ = 'marble_xu'

import os
import json
import pygame as pg
from .. import tool
from .. import constants as c
from ..component import map, plant, zombie, menubar

#식물 선택, 맵 로드 하는 곳?


class Level(tool.State):
    def __init__(self):
        tool.State.__init__(self)

    def startup(self, current_time, persist):
        self.game_info = persist
        self.persist = self.game_info
        self.game_info[c.CURRENT_TIME] = current_time
        self.map_y_len = c.GRID_Y_LEN
        self.map = map.Map(c.GRID_X_LEN, self.map_y_len)

        self.loadMap()
        self.setupBackground()
        self.initState()
        self.setUpItemImage()

    #배속버튼, 아이템들 초기화
    def setUpItemImage(self):
        speedup = [0, 0, 59, 54]
        if(c.DELTA_TIME == 1):
            self.speedupIMG = tool.get_image(
                tool.GFX[c.SPEED_UP_BUTTON_1], *speedup)
        elif(c.DELTA_TIME == 2):
            self.speedupIMG = tool.get_image(
                tool.GFX[c.SPEED_UP_BUTTON_2], *speedup)
        elif(c.DELTA_TIME == 3):
            self.speedupIMG = tool.get_image(
                tool.GFX[c.SPEED_UP_BUTTON_3], *speedup)
        self.speedupRect = self.speedupIMG.get_rect()
        self.speedupRect.x = 540
        self.speedupRect.y = 10

        #아이템1 초기화 부분
        item_1 = [0, 0, 59, 54]
        self.itemImg_1 = tool.get_image(
            tool.GFX[c.ITEM_1_1], *item_1)
        self.itemRect_1 = self.itemImg_1.get_rect()
        self.itemRect_1.x = 605
        self.itemRect_1.y = 10
        #0안클릭 1클릭이벤트 2클릭x
        self.isItem_1_Clicked = 0
        self.Item_1_Timer = 5000

        #아이템2 초기화 부분
        item_2 = [0, 0, 59, 54]
        self.itemImg_2 = tool.get_image(
            tool.GFX[c.ITEM_2_1], *item_2)
        self.itemRect_2 = self.itemImg_2.get_rect()
        self.itemRect_2.x = 675
        self.itemRect_2.y = 10
        #0안클릭 1클릭이벤트 2클릭x
        self.isItem_2_Clicked = 0
        self.Item_2_Timer = 5000

        #추가로 삽 버튼 관련 속성 여기에 초기화함 - 12/04 홍성민
        shovel = [0, 0, 59, 54]
        self.shovelIMG = tool.get_image(tool.GFX[c.SHOVEL_IMAGE], *shovel)
        self.shovelRect = self.shovelIMG.get_rect()
        self.shovelRect.x = 740
        self.shovelRect.y = 9

    def loadMap(self):
        if(c.LEVEL_DIFFICULTY == 1):
            map_file = 'level_e' + str(self.game_info[c.LEVEL_NUM]) + '.json'
        elif(c.LEVEL_DIFFICULTY == 2):
            map_file = 'level_' + str(self.game_info[c.LEVEL_NUM]) + '.json'
        elif(c.LEVEL_DIFFICULTY == 3):
            map_file = 'level_h' + str(self.game_info[c.LEVEL_NUM]) + '.json'
        file_path = os.path.join('source', 'data', 'map', map_file)
        f = open(file_path)
        self.map_data = json.load(f)
        f.close()

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
        self.hypno_zombie_groups = []  # zombies who are hypno after eating hypnoshroom
        self.bullet_groups = []
        for i in range(self.map_y_len):
            self.plant_groups.append(pg.sprite.Group())
            self.zombie_groups.append(pg.sprite.Group())
            self.hypno_zombie_groups.append(pg.sprite.Group())
            self.bullet_groups.append(pg.sprite.Group())

    def setupZombies(self):
        def takeTime(element):
            return element[0]

        self.zombie_list = []
        for data in self.map_data[c.ZOMBIE_LIST]:
            self.zombie_list.append(
                (data['time'], data['name'], data['map_y']))
        self.zombie_start_time = 0
        self.zombie_list.sort(key=takeTime)

    def setupCars(self):
        self.cars = []
        for i in range(self.map_y_len):
            _, y = self.map.getMapGridPos(0, i)
            self.cars.append(plant.Car(-25, y+20, i))

    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        if self.state == c.CHOOSE:
            self.choose(mouse_pos, mouse_click)
        elif self.state == c.PLAY:
            self.play(mouse_pos, mouse_click)

        self.draw(surface, mouse_pos)

    def initBowlingMap(self):
        print('initBowlingMap')
        for x in range(3, self.map.width):
            for y in range(self.map.height):
                self.map.setMapGridType(x, y, c.MAP_EXIST)

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
        self.panel = menubar.Panel(
            menubar.all_card_list, self.map_data[c.INIT_SUN_NAME])

    def choose(self, mouse_pos, mouse_click):
        if mouse_pos and mouse_click[0]:
            self.panel.checkCardClick(mouse_pos)
            if self.panel.checkStartButtonClick(mouse_pos):
                self.initPlay(self.panel.getSelectedCards())

    def initPlay(self, card_list):
        self.state = c.PLAY
        if self.bar_type == c.CHOOSEBAR_STATIC:
            self.menubar = menubar.MenuBar(
                card_list, self.map_data[c.INIT_SUN_NAME])
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
        self.setupZombies()
        self.setupCars()
        #중화 타이머
        tool.GameManager.getInstance().reSetTimer()
        #마우스 포인터 대신 띄워지는 삽 이미지
        self.shovel_pointer_IMG = None
        self.shovelActivate = False

    def play(self, mouse_pos, mouse_click):

        #중화 타이머
        tool.GameManager.getInstance().addTimer()
        #print(tool.GameManager.getInstance().getTimer())

        if self.zombie_start_time == 0:
            self.zombie_start_time = self.current_time
        elif len(self.zombie_list) > 0:
            data = self.zombie_list[0]
            if data[0] <= (self.current_time - self.zombie_start_time):
                self.createZombie(data[1], data[2])
                self.zombie_list.remove(data)

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

        if not self.drag_plant and mouse_pos and mouse_click[0] and self.shovelActivate == False:
            result = self.menubar.checkCardClick(mouse_pos)
            if result:
                self.setupMouseImage(result[0], result[1])
        elif self.drag_plant:
            if mouse_click[1]:
                self.removeMouseImage()
            elif mouse_click[0]:
                if self.menubar.checkMenuBarClick(mouse_pos):
                    self.removeMouseImage()
                else:
                    self.addPlant()
            elif mouse_pos is None:
                self.setupHintImage()

        if self.produce_sun:
            if(self.current_time - self.sun_timer) > c.PRODUCE_SUN_INTERVAL / c.SUN_TIME_UP:
                self.sun_timer = self.current_time
                map_x, map_y = self.map.getRandomMapIndex()
                x, y = self.map.getMapGridPos(map_x, map_y)
                self.sun_group.add(plant.Sun(x, 0, x, y))
        if not self.drag_plant and mouse_pos and mouse_click[0]:
            for sun in self.sun_group:
                if sun.checkCollision(mouse_pos[0], mouse_pos[1]):
                    self.menubar.increaseSunValue(sun.sun_value)

        for car in self.cars:
            car.update(self.game_info)

        self.menubar.update(self.current_time)

        self.checkBulletCollisions()
        self.checkZombieCollisions()
        self.checkPlants()
        self.checkCarCollisions()
        self.checkGameState()

    def createZombie(self, name, map_y):
        x, y = self.map.getMapGridPos(0, map_y)
        if name == c.NORMAL_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.NormalZombie(
                c.ZOMBIE_START_X, y, self.head_group))
        elif name == c.CONEHEAD_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.ConeHeadZombie(
                c.ZOMBIE_START_X, y, self.head_group))
        elif name == c.BUCKETHEAD_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.BucketHeadZombie(
                c.ZOMBIE_START_X, y, self.head_group))
        elif name == c.FLAG_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.FlagZombie(
                c.ZOMBIE_START_X, y, self.head_group))
        elif name == c.NEWSPAPER_ZOMBIE:
            self.zombie_groups[map_y].add(zombie.NewspaperZombie(
                c.ZOMBIE_START_X, y, self.head_group))

    def canSeedPlant(self):
        x, y = pg.mouse.get_pos()
        return self.map.showPlant(x, y)

    def addPlant(self):
        pos = self.canSeedPlant()
        if pos is None:
            return

        if self.hint_image is None:
            self.setupHintImage()
        x, y = self.hint_rect.centerx, self.hint_rect.bottom
        map_x, map_y = self.map.getMapIndex(x, y)
        if self.plant_name == c.SUNFLOWER:
            new_plant = plant.SunFlower(x, y, self.sun_group)
        elif self.plant_name == c.PEASHOOTER:
            new_plant = plant.PeaShooter(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.SNOWPEASHOOTER:
            new_plant = plant.SnowPeaShooter(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.WALLNUT:
            new_plant = plant.WallNut(x, y)
        elif self.plant_name == c.CHERRYBOMB:
            new_plant = plant.CherryBomb(x, y)
        elif self.plant_name == c.THREEPEASHOOTER:
            new_plant = plant.ThreePeaShooter(x, y, self.bullet_groups, map_y)
        elif self.plant_name == c.REPEATERPEA:
            new_plant = plant.RepeaterPea(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.CHOMPER:
            new_plant = plant.Chomper(x, y)
        elif self.plant_name == c.PUFFSHROOM:
            new_plant = plant.PuffShroom(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.POTATOMINE:
            new_plant = plant.PotatoMine(x, y)
        elif self.plant_name == c.SQUASH:
            new_plant = plant.Squash(x, y)
        elif self.plant_name == c.SPIKEWEED:
            new_plant = plant.Spikeweed(x, y)
        elif self.plant_name == c.JALAPENO:
            new_plant = plant.Jalapeno(x, y)
        elif self.plant_name == c.SCAREDYSHROOM:
            new_plant = plant.ScaredyShroom(x, y, self.bullet_groups[map_y])
        elif self.plant_name == c.SUNSHROOM:
            new_plant = plant.SunShroom(x, y, self.sun_group)
        elif self.plant_name == c.ICESHROOM:
            new_plant = plant.IceShroom(x, y)
        elif self.plant_name == c.HYPNOSHROOM:
            new_plant = plant.HypnoShroom(x, y)
        elif self.plant_name == c.WALLNUTBOWLING:
            new_plant = plant.WallNutBowling(x, y, map_y, self)
        elif self.plant_name == c.REDWALLNUTBOWLING:
            new_plant = plant.RedWallNutBowling(x, y)

        if new_plant.can_sleep and self.background_type == c.BACKGROUND_DAY:
            new_plant.setSleep()
        self.plant_groups[map_y].add(new_plant)
        if self.bar_type == c.CHOOSEBAR_STATIC:
            self.menubar.decreaseSunValue(self.select_plant.sun_cost)
            self.menubar.setCardFrozenTime(self.plant_name)
        else:
            self.menubar.deleateCard(self.select_plant)

        if self.bar_type != c.CHOSSEBAR_BOWLING:
            self.map.setMapGridType(map_x, map_y, c.MAP_EXIST)
        self.removeMouseImage()
        #print('addPlant map[%d,%d], grid pos[%d, %d] pos[%d, %d]' % (map_x, map_y, x, y, pos[0], pos[1]))

    def setupHintImage(self):
        pos = self.canSeedPlant()
        if pos and self.mouse_image:
            if (self.hint_image and pos[0] == self.hint_rect.x and
                    pos[1] == self.hint_rect.y):
                return
            width, height = self.mouse_rect.w, self.mouse_rect.h
            image = pg.Surface([width, height])
            image.blit(self.mouse_image, (0, 0), (0, 0, width, height))
            image.set_colorkey(c.BLACK)
            image.set_alpha(128)
            self.hint_image = image
            self.hint_rect = image.get_rect()
            self.hint_rect.centerx = pos[0]
            self.hint_rect.bottom = pos[1]
            self.hint_plant = True
        else:
            self.hint_plant = False

    def setupMouseImage(self, plant_name, select_plant):
        frame_list = tool.GFX[plant_name]
        if plant_name in tool.PLANT_RECT:
            data = tool.PLANT_RECT[plant_name]
            x, y, width, height = data['x'], data['y'], data['width'], data['height']
        else:
            x, y = 0, 0
            rect = frame_list[0].get_rect()
            width, height = rect.w, rect.h

        if (plant_name == c.POTATOMINE or plant_name == c.SQUASH or
            plant_name == c.SPIKEWEED or plant_name == c.JALAPENO or
            plant_name == c.SCAREDYSHROOM or plant_name == c.SUNSHROOM or
            plant_name == c.ICESHROOM or plant_name == c.HYPNOSHROOM or
                plant_name == c.WALLNUTBOWLING or plant_name == c.REDWALLNUTBOWLING):
            color = c.WHITE
        else:
            color = c.BLACK
        self.mouse_image = tool.get_image(
            frame_list[0], x, y, width, height, color, 1)
        self.mouse_rect = self.mouse_image.get_rect()
        pg.mouse.set_visible(False)
        self.drag_plant = True
        self.plant_name = plant_name
        self.select_plant = select_plant

    def removeMouseImage(self):
        pg.mouse.set_visible(True)
        self.drag_plant = False
        self.mouse_image = None
        self.hint_image = None
        self.hint_plant = False

    def checkBulletCollisions(self):
        collided_func = pg.sprite.collide_circle_ratio(0.7)
        for i in range(self.map_y_len):
            for bullet in self.bullet_groups[i]:
                if bullet.state == c.FLY:
                    zombie = pg.sprite.spritecollideany(
                        bullet, self.zombie_groups[i], collided_func)
                    if zombie and zombie.state != c.DIE:
                        zombie.setDamage(bullet.damage, bullet.ice)
                        bullet.setExplode()

    def checkZombieCollisions(self):
        if self.bar_type == c.CHOSSEBAR_BOWLING:
            ratio = 0.6
        else:
            ratio = 0.7
        collided_func = pg.sprite.collide_circle_ratio(ratio)
        for i in range(self.map_y_len):
            hypo_zombies = []
            for zombie in self.zombie_groups[i]:
                if zombie.state != c.WALK:
                    continue
                plant = pg.sprite.spritecollideany(
                    zombie, self.plant_groups[i], collided_func)
                if plant:
                    if plant.name == c.WALLNUTBOWLING:
                        if plant.canHit(i):
                            zombie.setDamage(c.WALLNUT_BOWLING_DAMAGE)
                            plant.changeDirection(i)
                    elif plant.name == c.REDWALLNUTBOWLING:
                        if plant.state == c.IDLE:
                            plant.setAttack()
                    elif plant.name != c.SPIKEWEED:
                        zombie.setAttack(plant)

            for hypno_zombie in self.hypno_zombie_groups[i]:
                if hypno_zombie.health <= 0:
                    continue
                zombie_list = pg.sprite.spritecollide(hypno_zombie,
                                                      self.zombie_groups[i], False, collided_func)
                for zombie in zombie_list:
                    if zombie.state == c.DIE:
                        continue
                    if zombie.state == c.WALK:
                        zombie.setAttack(hypno_zombie, False)
                    if hypno_zombie.state == c.WALK:
                        hypno_zombie.setAttack(zombie, False)

    def checkCarCollisions(self):
        collided_func = pg.sprite.collide_circle_ratio(0.8)
        for car in self.cars:
            zombies = pg.sprite.spritecollide(
                car, self.zombie_groups[car.map_y], False, collided_func)
            for zombie in zombies:
                if zombie and zombie.state != c.DIE:
                    car.setWalk()
                    zombie.setDie()
            if car.dead:
                self.cars.remove(car)

    def boomZombies(self, x, map_y, y_range, x_range):
        for i in range(self.map_y_len):
            if abs(i - map_y) > y_range:
                continue
            for zombie in self.zombie_groups[i]:
                if abs(zombie.rect.centerx - x) <= x_range:
                    zombie.setBoomDie()

    def freezeZombies(self, plant):
        for i in range(self.map_y_len):
            for zombie in self.zombie_groups[i]:
                if zombie.rect.centerx < c.SCREEN_WIDTH:
                    zombie.setFreeze(plant.trap_frames[0])

    def killPlant(self, plant):
        x, y = plant.getPosition()
        map_x, map_y = self.map.getMapIndex(x, y)
        if self.bar_type != c.CHOSSEBAR_BOWLING:
            self.map.setMapGridType(map_x, map_y, c.MAP_EMPTY)
        if (plant.name == c.CHERRYBOMB or plant.name == c.JALAPENO or
            (plant.name == c.POTATOMINE and not plant.is_init) or
                plant.name == c.REDWALLNUTBOWLING):
            self.boomZombies(plant.rect.centerx, map_y, plant.explode_y_range,
                             plant.explode_x_range)
        elif plant.name == c.ICESHROOM and plant.state != c.SLEEP:
            self.freezeZombies(plant)
        elif plant.name == c.HYPNOSHROOM and plant.state != c.SLEEP:
            zombie = plant.kill_zombie
            zombie.setHypno()
            _, map_y = self.map.getMapIndex(
                zombie.rect.centerx, zombie.rect.bottom)
            self.zombie_groups[map_y].remove(zombie)
            self.hypno_zombie_groups[map_y].add(zombie)
        plant.kill()

    def checkPlant(self, plant, i):
        zombie_len = len(self.zombie_groups[i])
        if plant.name == c.THREEPEASHOOTER:
            if plant.state == c.IDLE:
                if zombie_len > 0:
                    plant.setAttack()
                elif (i-1) >= 0 and len(self.zombie_groups[i-1]) > 0:
                    plant.setAttack()
                elif (i+1) < self.map_y_len and len(self.zombie_groups[i+1]) > 0:
                    plant.setAttack()
            elif plant.state == c.ATTACK:
                if zombie_len > 0:
                    pass
                elif (i-1) >= 0 and len(self.zombie_groups[i-1]) > 0:
                    pass
                elif (i+1) < self.map_y_len and len(self.zombie_groups[i+1]) > 0:
                    pass
                else:
                    plant.setIdle()
        elif plant.name == c.CHOMPER:
            for zombie in self.zombie_groups[i]:
                if plant.canAttack(zombie):
                    plant.setAttack(zombie, self.zombie_groups[i])
                    break
        elif plant.name == c.POTATOMINE:
            for zombie in self.zombie_groups[i]:
                if plant.canAttack(zombie):
                    plant.setAttack()
                    break
        elif plant.name == c.SQUASH:
            for zombie in self.zombie_groups[i]:
                if plant.canAttack(zombie):
                    plant.setAttack(zombie, self.zombie_groups[i])
                    break
        elif plant.name == c.SPIKEWEED:
            can_attack = False
            for zombie in self.zombie_groups[i]:
                if plant.canAttack(zombie):
                    can_attack = True
                    break
            if plant.state == c.IDLE and can_attack:
                plant.setAttack(self.zombie_groups[i])
            elif plant.state == c.ATTACK and not can_attack:
                plant.setIdle()
        elif plant.name == c.SCAREDYSHROOM:
            need_cry = False
            can_attack = False
            for zombie in self.zombie_groups[i]:
                if plant.needCry(zombie):
                    need_cry = True
                    break
                elif plant.canAttack(zombie):
                    can_attack = True
            if need_cry:
                if plant.state != c.CRY:
                    plant.setCry()
            elif can_attack:
                if plant.state != c.ATTACK:
                    plant.setAttack()
            elif plant.state != c.IDLE:
                plant.setIdle()
        elif(plant.name == c.WALLNUTBOWLING or
             plant.name == c.REDWALLNUTBOWLING):
            pass
        else:
            can_attack = False
            if (plant.state == c.IDLE and zombie_len > 0):
                for zombie in self.zombie_groups[i]:
                    if plant.canAttack(zombie):
                        can_attack = True
                        break
            if plant.state == c.IDLE and can_attack:
                plant.setAttack()
            elif (plant.state == c.ATTACK and not can_attack):
                plant.setIdle()

    def checkPlants(self):
        for i in range(self.map_y_len):
            for plant in self.plant_groups[i]:
                if plant.state != c.SLEEP:
                    self.checkPlant(plant, i)
                if plant.health <= 0:
                    self.killPlant(plant)

    def checkVictory(self):
        if len(self.zombie_list) > 0:
            return False
        for i in range(self.map_y_len):
            if len(self.zombie_groups[i]) > 0:
                return False
        return True

    def checkLose(self):
        for i in range(self.map_y_len):
            for zombie in self.zombie_groups[i]:
                if zombie.rect.right < 0:
                    return True
        return False

    def checkGameState(self):
        if self.checkVictory():
            self.game_info[c.LEVEL_NUM] += 1
            self.next = c.GAME_VICTORY
            self.done = True
        elif self.checkLose():
            self.next = c.GAME_LOSE
            self.done = True

    def drawMouseShow(self, surface):
        if self.hint_plant:
            surface.blit(self.hint_image, self.hint_rect)
        x, y = pg.mouse.get_pos()
        self.mouse_rect.centerx = x
        self.mouse_rect.centery = y
        surface.blit(self.mouse_image, self.mouse_rect)

    def drawZombieFreezeTrap(self, i, surface):
        for zombie in self.zombie_groups[i]:
            zombie.drawFreezeTrap(surface)

    #중화 배속 버튼
    def drawSpeedUpButton(self, surface):
        surface.blit(self.speedupIMG, self.speedupRect)

    def CheckSpeedUpButtonClicked(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.speedupRect.x and x <= self.speedupRect.right and
           y >= self.speedupRect.y and y <= self.speedupRect.bottom):
            self.SpeedUpButtonClickEvent()

    def SpeedUpButtonClickEvent(self):
        speedup = [0, 0, 59, 54]
        if(c.DELTA_TIME == 1):
            self.speedupIMG = tool.get_image(
                tool.GFX[c.SPEED_UP_BUTTON_2], *speedup)
            c.DELTA_TIME = 2
        elif(c.DELTA_TIME == 2):
            self.speedupIMG = tool.get_image(
                tool.GFX[c.SPEED_UP_BUTTON_3], *speedup)
            c.DELTA_TIME = 3
        elif(c.DELTA_TIME == 3):
            self.speedupIMG = tool.get_image(
                tool.GFX[c.SPEED_UP_BUTTON_1], *speedup)
            c.DELTA_TIME = 1
        tool.GameManager.getInstance().reSetStartTimer()
        tool.GameManager.getInstance().reSetCurrentTimer()

    def drawItem(self, surface):
        surface.blit(self.itemImg_1, self.itemRect_1)
        surface.blit(self.itemImg_2, self.itemRect_2)

    def CheckItemButtonClicked(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.itemRect_1.x and x <= self.itemRect_1.right and
           y >= self.itemRect_1.y and y <= self.itemRect_1.bottom and self.isItem_1_Clicked == 0):
            self.Item_1_StartEvent()
        if(x >= self.itemRect_2.x and x <= self.itemRect_2.right and
           y >= self.itemRect_2.y and y <= self.itemRect_2.bottom and self.isItem_2_Clicked == 0):
            self.Item_2_StartEvent()

    def Item_1_StartEvent(self):
        self.isItem_1_Clicked = 1
        self.Item_1_Timer += self.current_time
        c.ATK_TIME_UP = 2
        temp = [0, 0, 59, 54]
        self.itemImg_1 = tool.get_image(
            tool.GFX[c.ITEM_1_2], *temp)

    def Item_1_EndEvent(self):
        if(self.Item_1_Timer < self.current_time):
           c.ATK_TIME_UP = 1
           self.isItem_1_Clicked = 2

    def Item_2_StartEvent(self):
        self.isItem_2_Clicked = 1
        self.Item_2_Timer += self.current_time
        c.SUN_TIME_UP = 10
        temp = [0, 0, 59, 54]
        self.itemImg_2 = tool.get_image(
            tool.GFX[c.ITEM_2_2], *temp)

    def Item_2_EndEvent(self):
        if(self.Item_2_Timer < self.current_time):
           c.SUN_TIME_UP = 1
           self.isItem_2_Clicked = 2

    #홍성민 삽 버튼 관련 함수들
    def drawShovelButton(self, surface):
        surface.blit(self.shovelIMG, self.shovelRect)

    def checkShovelButtonClicked(self, mouse_pos):
        x, y = mouse_pos
        shovel_pointer = [0, 0, 59, 54]
        if(x >= self.shovelRect.x - 10 and x <= self.shovelRect.right + 10 and
           y >= self.shovelRect.y - 10 and y <= self.shovelRect.bottom + 10):
            print("shovel clicked")
            # 이곳에 마우스포인터 삽 이미지 및 기능 활성화. 판정은 shovel pointer img가 none인지 아닌지로 한다.
            if (self.shovel_pointer_IMG == None):
                self.shovel_pointer_IMG = tool.get_image(
                    tool.GFX[c.SHOVEL_IMAGE], *shovel_pointer)
                pg.mouse.set_visible(False)
                self.shovelActivate = True
                print(
                    "shovel clicked, and shovelpointer img was none. Now mouse set_visible is False, and IMG got his image")
            # 이미지 및 기능 비활성화, 원래대로
            elif (self.shovel_pointer_IMG != None):
                print(
                    "shovel clicked, and shovelpointer img was had something, Now mouse and IMG get back")
                pg.mouse.set_visible(True)
                self.shovel_pointer_IMG = None
                self.shovelActivate = False
                self.removeMouseImage()
           # If you want to set IMG to member, use this code.
           # self.shovel_pointer_IMG = tool.get_image(tool.GFX[c.SHOVEL_IMAGE], *shovel_pointer)

    #마우스 포인터 위치에 삽 이미지를 띄우게 하는 메소드
    def drawShovelMouseShow(self, surface):
        surface.blit(self.shovel_pointer_IMG, pg.mouse.get_pos())

    # plant를 넘겨받아 삽으로 클릭한 식물을 지우는 메소드
    def removePlantByShovel(self, plant):
        x, y = plant.getPosition()
        map_x, map_y = self.map.getMapIndex(x, y)
        if self.bar_type != c.CHOSSEBAR_BOWLING:
            self.map.setMapGridType(map_x, map_y, c.MAP_EMPTY)
        plant.kill()

    def draw(self, surface, mouse_pos):
        self.level.blit(self.background, self.viewport, self.viewport)
        surface.blit(self.level, (0, 0), self.viewport)
        if self.state == c.CHOOSE:
            self.panel.draw(surface)
        elif self.state == c.PLAY:
            #추가 이미지 그려주는
            self.drawSpeedUpButton(surface)
            self.drawItem(surface)
            self.drawShovelButton(surface)

            self.menubar.draw(surface)
            for i in range(self.map_y_len):
                self.plant_groups[i].draw(surface)
                self.zombie_groups[i].draw(surface)
                self.hypno_zombie_groups[i].draw(surface)
                self.bullet_groups[i].draw(surface)
                self.drawZombieFreezeTrap(i, surface)
            for car in self.cars:
                car.draw(surface)
            self.head_group.draw(surface)
            self.sun_group.draw(surface)

            if(mouse_pos != None):
                #다른 아이템 이미지 클릭 이벤트 여기에
                self.CheckSpeedUpButtonClicked(mouse_pos)
                self.CheckItemButtonClicked(mouse_pos)
                self.checkShovelButtonClicked(mouse_pos)
            if(self.isItem_1_Clicked == 1):
                self.Item_1_EndEvent()
            if(self.isItem_2_Clicked == 1):
                self.Item_2_EndEvent()
            if self.drag_plant:
                self.drawMouseShow(surface)

            # self.shovel_pointer_IMG에 이미지가 추가되어 삽 기능이 작동하는 상태. if문의 조건문은 checkShovelButtonClicekd를 참조
            if (self.shovel_pointer_IMG != None):
                self.drawShovelMouseShow(surface)
                for i in range(self.map_y_len):
                    for plant in self.plant_groups[i]:
                        plant_pos_x, plant_pos_y = plant.getPosition()
                        shovel_clicked_x, shovel_clicked_y = pg.mouse.get_pos()
                        shovel_isClicked = [False, False, False]
                        shovel_isClicked = pg.mouse.get_pressed()
                        plant_pos_y -= 100
                        if(shovel_isClicked[0] == True and plant_pos_x - 35 <= shovel_clicked_x and shovel_clicked_x <= plant_pos_x + 35
                           and plant_pos_y - 20 <= shovel_clicked_y and shovel_clicked_y <= plant_pos_y + 40):
                            print("Plants is Clicked with Shovel")
                            self.removePlantByShovel(plant)
