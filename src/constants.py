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
ZOOM_MIN = 0.5
ZOOM_MAX = 2.0
ZOOM_SPEED = 0.1
DEFAULT_ZOOM = 1.0

# constants.py - Add these lines
ROTATION_SPEED = 0.1  # Slower rotation speed (0.1 seconds between rotations)
ROTATION_COOLDOWN = 200  # milliseconds between rotations

ROTATION_KEY = pygame.K_r  # Add this line

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