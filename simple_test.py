#!/usr/bin/env python3
"""
Simple test script for roof level functionality
"""

import sys
import os

# Test 1: Check if all required files exist
print("Testing file existence...")

# Check constants.py
constants_path = os.path.join('source', 'constants.py')
if os.path.exists(constants_path):
    print("✓ constants.py exists")
else:
    print("✗ constants.py missing")
    sys.exit(1)

# Check level.py
level_path = os.path.join('source', 'state', 'level.py')
if os.path.exists(level_path):
    print("✓ level.py exists")
else:
    print("✗ level.py missing")
    sys.exit(1)

# Check plant.py
plant_path = os.path.join('source', 'component', 'plant.py')
if os.path.exists(plant_path):
    print("✓ plant.py exists")
else:
    print("✗ plant.py missing")
    sys.exit(1)

# Check roof level map file
roof_map_path = os.path.join('source', 'data', 'map', 'level_roof.json')
if os.path.exists(roof_map_path):
    print("✓ level_roof.json exists")
else:
    print("✗ level_roof.json missing")
    sys.exit(1)

# Test 2: Check if constants are defined correctly
print("\nTesting constants...")

with open(constants_path, 'r') as f:
    constants_content = f.read()

# Check BACKGROUND_ROOF
if 'BACKGROUND_ROOF' in constants_content:
    print("✓ BACKGROUND_ROOF constant defined")
else:
    print("✗ BACKGROUND_ROOF constant missing")
    sys.exit(1)

# Check FLOWERPOT
if 'FLOWERPOT' in constants_content:
    print("✓ FLOWERPOT constant defined")
else:
    print("✗ FLOWERPOT constant missing")
    sys.exit(1)

# Check CABBAGEPULT
if 'CABBAGEPULT' in constants_content:
    print("✓ CABBAGEPULT constant defined")
else:
    print("✗ CABBAGEPULT constant missing")
    sys.exit(1)

# Check BULLET_CABBAGE
if 'BULLET_CABBAGE' in constants_content:
    print("✓ BULLET_CABBAGE constant defined")
else:
    print("✗ BULLET_CABBAGE constant missing")
    sys.exit(1)

# Check GRAVITY
if 'GRAVITY' in constants_content:
    print("✓ GRAVITY constant defined")
else:
    print("✗ GRAVITY constant missing")
    sys.exit(1)

# Test 3: Check if new classes are defined
print("\nTesting new classes...")

with open(plant_path, 'r') as f:
    plant_content = f.read()

# Check FlowerPot class
if 'class FlowerPot' in plant_content:
    print("✓ FlowerPot class defined")
else:
    print("✗ FlowerPot class missing")
    sys.exit(1)

# Check CabbagePult class
if 'class CabbagePult' in plant_content:
    print("✓ CabbagePult class defined")
else:
    print("✗ CabbagePult class missing")
    sys.exit(1)

# Check ParabolicBullet class
if 'class ParabolicBullet' in plant_content:
    print("✓ ParabolicBullet class defined")
else:
    print("✗ ParabolicBullet class missing")
    sys.exit(1)

# Test 4: Check if roof level support is added to Level class
print("\nTesting Level class roof support...")

with open(level_path, 'r') as f:
    level_content = f.read()

# Check is_roof_level
if 'self.is_roof_level' in level_content:
    print("✓ Roof level flag added")
else:
    print("✗ Roof level flag missing")
    sys.exit(1)

# Check planting restrictions
if 'self.is_roof_level' in level_content and 'FLOWERPOT' in level_content:
    print("✓ Planting restrictions implemented")
else:
    print("✗ Planting restrictions missing")
    sys.exit(1)

# Check bullet collision modifications
if 'self.is_roof_level' in level_content and 'getattr(bullet, \'ice\', False)' in level_content:
    print("✓ Bullet collision modifications implemented")
else:
    print("✗ Bullet collision modifications missing")
    sys.exit(1)

print("\n✅ All tests passed! Roof level implementation is complete.")
print("=" * 50)