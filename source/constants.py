__author__ = 'marble_xu'

START_LEVEL_NUM = 1

ORIGINAL_CAPTION = 'Plant VS Zombies Game'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

GRID_X_LEN = 9
GRID_Y_LEN = 5
GRID_X_SIZE = 80
GRID_Y_SIZE = 100


WHITE        = (255, 255, 255)
NAVYBLUE     = ( 60,  60, 100)
SKY_BLUE     = ( 39, 145, 251)
BLACK        = (  0,   0,   0)
LIGHTYELLOW  = (234, 233, 171)
RED          = (255,   0,   0)
PURPLE       = (255,   0, 255)
GOLD         = (255, 215,   0)
GREEN        = (  0, 255,   0)

SIZE_MULTIPLIER = 1.3

#GAME INFO DICTIONARY KEYS
CURRENT_TIME = 'current time'
LEVEL_NUM = 'level num'

#STATES FOR ENTIRE GAME
MAIN_MENU = 'main menu'
LOAD_SCREEN = 'load screen'
GAME_LOSE = 'game los'
GAME_VICTORY = 'game victory'
LEVEL = 'level'

MAIN_MENU_IMAGE = 'MainMenu'
OPTION_ADVENTURE = 'Adventure'
GAME_LOOSE_IMAGE = 'GameLoose'
GAME_VICTORY_IMAGE = 'GameVictory'

#MAP COMPONENTS
BACKGROUND_NAME = 'Background'
BACKGROUND_TYPE = 'background_type'
INIT_SUN_NAME = 'init_sun_value'
ZOMBIE_LIST = 'zombie_list'

MAP_EMPTY = 0
MAP_EXIST = 1

BACKGROUND_OFFSET_X = 220
MAP_OFFSET_X = 35
MAP_OFFSET_Y = 100

#MENUBAR
CHOOSEBAR_TYPE = 'choosebar_type'
CHOOSEBAR_STATIC = 0
CHOOSEBAR_MOVE = 1
CHOSSEBAR_BOWLING = 2
MENUBAR_BACKGROUND = 'ChooserBackground'
MOVEBAR_BACKGROUND = 'MoveBackground'
PANEL_BACKGROUND = 'PanelBackground'
START_BUTTON = 'StartButton'
CARD_POOL = 'card_pool'

MOVEBAR_CARD_FRESH_TIME = 6000
CARD_MOVE_TIME = 60

#PLANT INFO
PLANT_IMAGE_RECT = 'plant_image_rect'
CAR = 'car'
SUN = 'Sun'
SUNFLOWER = 'SunFlower'
PEASHOOTER = 'Peashooter'
SNOWPEASHOOTER = 'SnowPea'
WALLNUT = 'WallNut'
CHERRYBOMB = 'CherryBomb'
THREEPEASHOOTER = 'Threepeater'
REPEATERPEA = 'RepeaterPea'
CHOMPER = 'Chomper'
CHERRY_BOOM_IMAGE = 'Boom'
PUFFSHROOM = 'PuffShroom'
POTATOMINE = 'PotatoMine'
SQUASH = 'Squash'
SPIKEWEED = 'Spikeweed'
JALAPENO = 'Jalapeno'
SCAREDYSHROOM = 'ScaredyShroom'
SUNSHROOM = 'SunShroom'
ICESHROOM = 'IceShroom'
HYPNOSHROOM = 'HypnoShroom'
WALLNUTBOWLING = 'WallNutBowling'
REDWALLNUTBOWLING = 'RedWallNutBowling'
# Chinese Red Theme Plants
RED_PEONY = 'RedPeony'  # 红牡丹
FIRECRACKER_PLANT = 'FirecrackerPlant'  # 鞭炮花
LION_DANCE_PEA = 'LionDancePea'  # 舞狮豌豆

PLANT_HEALTH = 5
WALLNUT_HEALTH = 30
WALLNUT_CRACKED1_HEALTH = 20
WALLNUT_CRACKED2_HEALTH = 10
WALLNUT_BOWLING_DAMAGE = 10

# Chinese Red Theme Plant Properties
RED_PEONY_HEALTH = 15  # 红牡丹生命值
RED_PEONY_POLLEN_DAMAGE = 3  # 红牡丹花粉伤害
FIRECRACKER_PLANT_HEALTH = 10  # 鞭炮花生命值
FIRECRACKER_DAMAGE = 2  # 鞭炮伤害
LION_DANCE_PEA_HEALTH = 5  # 舞狮豌豆生命值
LION_DANCE_PEA_DAMAGE = 4  # 舞狮豌豆伤害
LION_DANCE_PEA_KNOCKBACK = 50  # 舞狮豌豆击退效果

PRODUCE_SUN_INTERVAL = 7000
FLOWER_SUN_INTERVAL = 22000
SUN_LIVE_TIME = 7000
SUN_VALUE = 25

ICE_SLOW_TIME = 2000

FREEZE_TIME = 7500
ICETRAP = 'IceTrap'

#PLANT CARD INFO
CARD_SUNFLOWER = 'card_sunflower'
CARD_PEASHOOTER = 'card_peashooter'
CARD_SNOWPEASHOOTER = 'card_snowpea'
CARD_WALLNUT = 'card_wallnut'
CARD_CHERRYBOMB = 'card_cherrybomb'
CARD_THREEPEASHOOTER = 'card_threepeashooter'
CARD_REPEATERPEA = 'card_repeaterpea'
CARD_CHOMPER = 'card_chomper'
CARD_PUFFSHROOM = 'card_puffshroom'
CARD_POTATOMINE = 'card_potatomine'
CARD_SQUASH = 'card_squash'
CARD_SPIKEWEED = 'card_spikeweed'
CARD_JALAPENO = 'card_jalapeno'
CARD_SCAREDYSHROOM = 'card_scaredyshroom'
CARD_SUNSHROOM = 'card_sunshroom'
CARD_ICESHROOM = 'card_iceshroom'
CARD_HYPNOSHROOM = 'card_hypnoshroom'
CARD_REDWALLNUT = 'card_redwallnut'
# Chinese Red Theme Plant Cards
CARD_RED_PEONY = 'card_redpeony'
CARD_FIRECRACKER_PLANT = 'card_firecrackerplant'
CARD_LION_DANCE_PEA = 'card_liondancepea'

#BULLET INFO
BULLET_PEA = 'PeaNormal'
BULLET_PEA_ICE = 'PeaIce'
BULLET_MUSHROOM = 'BulletMushRoom'
BULLET_DAMAGE_NORMAL = 1

#ZOMBIE INFO
ZOMBIE_IMAGE_RECT = 'zombie_image_rect'
ZOMBIE_HEAD = 'ZombieHead'
NORMAL_ZOMBIE = 'Zombie'
CONEHEAD_ZOMBIE = 'ConeheadZombie'
BUCKETHEAD_ZOMBIE = 'BucketheadZombie'
FLAG_ZOMBIE = 'FlagZombie'
NEWSPAPER_ZOMBIE = 'NewspaperZombie'
BOOMDIE = 'BoomDie'
# Chinese Red Theme Zombies
LANTERN_ZOMBIE = 'LanternZombie'  # 灯笼僵尸
LION_DANCE_ZOMBIE = 'LionDanceZombie'  # 舞狮僵尸
CHINESE_NEW_YEAR_ZOMBIE = 'ChineseNewYearZombie'  # 春节僵尸

LOSTHEAD_HEALTH = 5
NORMAL_HEALTH = 10
FLAG_HEALTH = 15
CONEHEAD_HEALTH = 20
BUCKETHEAD_HEALTH = 30
NEWSPAPER_HEALTH = 15

# Chinese Red Theme Zombie Properties
LANTERN_ZOMBIE_HEALTH = 15  # 灯笼僵尸生命值
LANTERN_ZOMBIE_SPEED = 1.2  # 灯笼僵尸移动速度
LANTERN_LIGHT_RANGE = 3  # 灯笼照亮范围
LION_DANCE_ZOMBIE_HEALTH = 30  # 舞狮僵尸生命值
LION_DANCE_ZOMBIE_SPEED = 0.8  # 舞狮僵尸移动速度
LION_DANCE_ATTACK_DAMAGE = 2  # 舞狮僵尸攻击伤害
CHINESE_NEW_YEAR_ZOMBIE_HEALTH = 25  # 春节僵尸生命值
CHINESE_NEW_YEAR_ZOMBIE_SPEED = 1.0  # 春节僵尸移动速度
CHINESE_NEW_YEAR_GOLD_DROP = 5  # 春节僵尸掉落金币数量

ATTACK_INTERVAL = 1000
ZOMBIE_WALK_INTERVAL = 70

ZOMBIE_START_X = SCREEN_WIDTH + 50

#STATE
IDLE = 'idle'
FLY = 'fly'
EXPLODE = 'explode'
ATTACK = 'attack'
ATTACKED = 'attacked'
DIGEST = 'digest'
WALK = 'walk'
DIE = 'die'
CRY = 'cry'
FREEZE = 'freeze'
SLEEP = 'sleep'

#LEVEL STATE
CHOOSE = 'choose'
PLAY = 'play'

#BACKGROUND
BACKGROUND_DAY = 0
BACKGROUND_NIGHT = 1