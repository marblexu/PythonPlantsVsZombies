import pygame as pg
import sys
import os

# 添加source目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'source'))

from source import tool
from source import constants as c
from source.state import level

def test_night_level():
    """测试黑夜关卡功能"""
    print("=== 测试黑夜关卡功能 ===")
    
    # 初始化pygame
    pg.init()
    screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
    clock = pg.time.Clock()
    
    # 创建游戏控制
    game = tool.Control()
    
    # 创建黑夜关卡
    level_state = level.Level()
    
    # 模拟加载黑夜关卡
    level_state.setupLevel(3)  # level_3.json是黑夜关卡
    
    print("1. 测试背景类型是否为黑夜:")
    print(f"   background_type = {level_state.background_type}")
    print(f"   预期: {c.BACKGROUND_NIGHT}")
    print(f"   结果: {'通过' if level_state.background_type == c.BACKGROUND_NIGHT else '失败'}")
    
    print("\n2. 测试是否不生成阳光:")
    print(f"   produce_sun = {level_state.produce_sun}")
    print(f"   预期: False")
    print(f"   结果: {'通过' if not level_state.produce_sun else '失败'}")
    
    print("\n3. 测试墓碑生成:")
    print(f"   墓碑数量: {len(level_state.grave_group)}")
    print(f"   预期: 5-8个墓碑")
    print(f"   结果: {'通过' if 5 <= len(level_state.grave_group) <= 8 else '失败'}")
    
    # 显示墓碑位置
    for i, grave in enumerate(level_state.grave_group):
        print(f"   墓碑{i+1}: 位置 ({grave.map_x}, {grave.map_y})")
    
    print("\n4. 测试黑夜滤镜是否创建:")
    print(f"   night_filter存在: {hasattr(level_state, 'night_filter')}")
    print(f"   结果: {'通过' if hasattr(level_state, 'night_filter') else '失败'}")
    
    if hasattr(level_state, 'night_filter'):
        print(f"   night_filter alpha: {level_state.night_filter.get_alpha()}")
        print(f"   预期: 80")
        print(f"   结果: {'通过' if level_state.night_filter.get_alpha() == 80 else '失败'}")
    
    print("\n=== 测试完成 ===")
    
    # 清理
    pg.quit()

if __name__ == "__main__":
    test_night_level()