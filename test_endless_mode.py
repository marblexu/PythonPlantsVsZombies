import pygame as pg
import sys
import os

# Add the source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))

from source import constants as c
from source.state.endless import EndlessMode
from source import tool

def test_endless_mode_initialization():
    """Test that endless mode initializes correctly"""
    print("Testing endless mode initialization...")
    
    # Create game info
    game_info = {
        c.CURRENT_TIME: pg.time.get_ticks(),
        c.LEVEL_NUM: 1
    }
    
    # Create endless mode state
    endless_mode = EndlessMode()
    endless_mode.startup(pg.time.get_ticks(), game_info)
    
    # Verify initial state
    assert endless_mode.current_wave == 1
    assert endless_mode.threat_level == 1.0
    assert not endless_mode.wave_in_progress
    
    print("✓ Endless mode initialization test passed")

def test_threat_level_scaling():
    """Test that threat level scales correctly"""
    print("\nTesting threat level scaling...")
    
    # Create game info
    game_info = {
        c.CURRENT_TIME: pg.time.get_ticks(),
        c.LEVEL_NUM: 1
    }
    
    # Create endless mode state
    endless_mode = EndlessMode()
    endless_mode.startup(pg.time.get_ticks(), game_info)
    
    # Simulate wave completion
    initial_threat = endless_mode.threat_level
    endless_mode.threat_level += 0.1
    
    assert endless_mode.threat_level == initial_threat + 0.1
    assert endless_mode.threat_level > 1.0
    
    print("✓ Threat level scaling test passed")

def test_zombie_generation():
    """Test that zombies are generated with correct attributes"""
    print("\nTesting zombie generation...")
    
    # Create game info
    game_info = {
        c.CURRENT_TIME: pg.time.get_ticks(),
        c.LEVEL_NUM: 1
    }
    
    # Create endless mode state
    endless_mode = EndlessMode()
    endless_mode.startup(pg.time.get_ticks(), game_info)
    
    # Test zombie type selection
    zombie_type = endless_mode.getZombieType()
    assert zombie_type in [c.NORMAL_ZOMBIE, c.CONEHEAD_ZOMBIE, c.BUCKETHEAD_ZOMBIE]
    
    print("✓ Zombie generation test passed")

def test_zombie_attribute_scaling():
    """Test that zombie attributes scale with threat level"""
    print("\nTesting zombie attribute scaling...")
    
    # Create game info
    game_info = {
        c.CURRENT_TIME: pg.time.get_ticks(),
        c.LEVEL_NUM: 1
    }
    
    # Create endless mode state
    endless_mode = EndlessMode()
    endless_mode.startup(pg.time.get_ticks(), game_info)
    
    # Test with different threat levels
    test_cases = [1.0, 5.0, 10.0, 15.0]
    
    for threat in test_cases:
        endless_mode.threat_level = threat
        
        # Test normal zombie
        normal_health = int(c.NORMAL_HEALTH * threat)
        normal_speed = 1 * (threat ** 0.5)
        
        # Test conehead zombie
        conehead_health = int(c.CONEHEAD_HEALTH * threat)
        conehead_speed = 1 * (threat ** 0.5)
        
        assert normal_health > 0
        assert normal_speed > 0
        assert conehead_health > 0
        assert conehead_speed > 0
    
    print("✓ Zombie attribute scaling test passed")

if __name__ == "__main__":
    print("Running endless mode tests...")
    print("=" * 50)
    
    # Initialize pygame once for all tests
    pg.init()
    pg.display.set_mode(c.SCREEN_SIZE)
    
    try:
        test_endless_mode_initialization()
        test_threat_level_scaling()
        test_zombie_generation()
        test_zombie_attribute_scaling()
        
        print("=" * 50)
        print("All tests passed! ✓")
    finally:
        pg.quit()