import os
import pygame

# Directory paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
TILES_DIR = os.path.join(ASSETS_DIR, 'tiles')
SPRITES_DIR = os.path.join(ASSETS_DIR, 'sprites')

# Game dimensions
TILE_W, TILE_H = 128, 64
MAP_W, MAP_H = 40, 40
SCREEN_W, SCREEN_H = 1600, 900

# Zoom settings
ZOOM_MIN = 0.3  # Allow zooming out more
ZOOM_MAX = 3.0  # Allow zooming in more
ZOOM_SPEED = 0.1  # Larger step size for instant zoom feel
DEFAULT_ZOOM = 1.0

# constants.py - Add these lines
ROTATION_SPEED = 0.1  # Slower rotation speed (0.1 seconds between rotations)
ROTATION_COOLDOWN = 200  # milliseconds between rotations

ROTATION_KEY = pygame.K_r  # Add this line

# Sprite positioning
SPRITE_VERTICAL_OFFSET = -6  # Adjust this to move sprites up (negative) or down (positive)

# Animation speeds in milliseconds
ANIM_SPEED_PLAYER = 120
ANIM_SPEED_MONSTER = 150
ANIM_SPEED_RESOURCE = 200
ANIM_SPEED_IDLE = 500
ANIM_SPEED_MOVING = 120

# Colors
COLOR_GRASS = (100, 200, 100)
COLOR_WATER = (80, 140, 220)
COLOR_STONE = (160, 160, 160)
COLOR_SAND = (220, 200, 140)
COLOR_BACKGROUND = (40, 40, 50)
COLOR_UI_BG = (40, 40, 60)
COLOR_UI_BORDER = (80, 80, 100)

# Game settings
FPS = 60
MOVE_COOLDOWN = 140
MONSTER_COUNT = 60
RESOURCE_COUNT = 120
PLAYER_HP = 30
MONSTER_HP = 8
RESOURCE_HP = 1

# Animation states
ANIM_IDLE = 'idle'
ANIM_WALK = 'walk'

# Directions
DIRECTIONS = ['north', 'south', 'east', 'west']


# UI Dimensions
INVENTORY_WIDTH = 400
INVENTORY_HEIGHT = 500
HOTBAR_WIDTH = 600
HOTBAR_HEIGHT = 80
UI_MARGIN = 10

# Colors for UI
COLOR_UI_BACKGROUND = (50, 50, 70, 200)      # RGBA format
COLOR_UI_BORDER = (100, 100, 150, 255)       # RGBA format
COLOR_SLOT_EMPTY = (70, 70, 90, 150)         # RGBA format
COLOR_SLOT_FILLED = (90, 120, 150, 180)      # RGBA format
COLOR_SLOT_HOVER = (120, 150, 180, 200)      # RGBA format
COLOR_SLOT_SELECTED = (150, 180, 210, 200)   # RGBA format
COLOR_TEXT_UI = (240, 240, 240, 255)         # RGBA format

# Inventory settings
INVENTORY_ROWS = 5
INVENTORY_COLS = 9
HOTBAR_SLOTS = 9
TOTAL_SLOTS = INVENTORY_ROWS * INVENTORY_COLS
SLOT_SIZE = 48
SLOT_MARGIN = 4

# Item types
ITEM_TYPES = {
    'resource': 'Resource',
}

RESOURCE_IMAGE = 'resource.png'  # Name of resource sprite file