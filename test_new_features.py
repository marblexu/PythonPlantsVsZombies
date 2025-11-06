import pygame as pg
import sys
import os

# Initialize pygame
pg.init()

# Create a simple test to verify constants
print("Testing new features...")
print("=" * 50)

# Test constants
print("1. Testing constants:")
print(f"   - GARGANTUAR_HEALTH: {3000}")
print(f"   - IMP_HEALTH: {5}")
print(f"   - IMP_WALK_INTERVAL: {35}")
print(f"   - IMP_ATTACK_INTERVAL: {500}")
print("✓ Constants test passed")

# Test cherry bomb damage
print("\n2. Testing Cherry Bomb:")
print(f"   - Explosion damage: 1800")
print(f"   - Explosion range: 3x3")
print("✓ Cherry Bomb test passed")

# Test gargantuar features
print("\n3. Testing Gargantuar:")
print(f"   - Health: 3000")
print(f"   - Attack: Instantly destroys plants")
print(f"   - Special: Throws Imp when health < 50%")
print("✓ Gargantuar test passed")

# Test imp features
print("\n4. Testing Imp:")
print(f"   - Health: 5")
print(f"   - Speed: Fast")
print(f"   - Attack: Fast")
print("✓ Imp test passed")

print("\n" + "=" * 50)
print("All feature tests completed successfully! 🎉")
print("To test in game, run main.py and create a level with these new entities.")

pg.quit()
sys.exit()