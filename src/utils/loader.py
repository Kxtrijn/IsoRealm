import os
import pygame
from constants import *


def ensure_dirs():
    """Create necessary directories if they don't exist"""
    os.makedirs(TILES_DIR, exist_ok=True)
    os.makedirs(SPRITES_DIR, exist_ok=True)


def make_iso_tile_surface(color, w=TILE_W, h=TILE_H):
    """Create fallback tile surface"""
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pts = [(w//2, 0), (w-1, h//2), (w//2, h-1), (0, h//2)]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.polygon(surf, (0, 0, 0, 120), pts, 2)
    return surf


def find_sprite_file(filename, search_subfolders=True):
    """Find a sprite file, searching in subfolders if enabled"""
    # Check directly in sprites folder first
    direct_path = os.path.join(SPRITES_DIR, filename)
    if os.path.exists(direct_path):
        return direct_path
    
    # Search in subfolders if enabled
    if search_subfolders:
        for root, dirs, files in os.walk(SPRITES_DIR):
            if root == SPRITES_DIR:
                continue
            for file in files:
                if file == filename:
                    return os.path.join(root, file)
    
    return None


def load_tile_images():
    """Load tile images - uses fallback if missing"""
    from constants import COLOR_GRASS, COLOR_WATER, COLOR_STONE, COLOR_SAND
    
    types = ['grass', 'water', 'stone', 'sand']
    tiles = {}
    color_map = {
        'grass': COLOR_GRASS,
        'water': COLOR_WATER,
        'stone': COLOR_STONE,
        'sand': COLOR_SAND
    }
    
    for t in types:
        p = os.path.join(TILES_DIR, f'{t}.png')
        if os.path.exists(p):
            tiles[t] = pygame.image.load(p).convert_alpha()
        else:
            tiles[t] = make_iso_tile_surface(color_map.get(t, (200, 0, 200)))
    return tiles


def load_entity_animations(entity_name, search_subfolders=True):
    """Load both idle and walk animations for an entity"""
    from constants import DIRECTIONS
    
    animations = {'idle': {}, 'walk': {}}
    loaded_files = []
    
    # Try to load static image first
    static_path = find_sprite_file(f'{entity_name}.png', search_subfolders)
    static_img = None
    if static_path:
        try:
            static_img = pygame.image.load(static_path).convert_alpha()
            loaded_files.append(f'Static: {os.path.basename(static_path)}')
        except Exception as e:
            print(f"Error loading {static_path}: {e}")
    
    for anim_type in ['idle', 'walk']:
        for direction in DIRECTIONS:
            frames = []
            frame_idx = 0
            
            # Load all frames for this animation type and direction
            while True:
                filename = f'{entity_name}_{anim_type}_{direction}_{frame_idx}.png'
                frame_path = find_sprite_file(filename, search_subfolders)
                
                if frame_path:
                    try:
                        img = pygame.image.load(frame_path).convert_alpha()
                        frames.append(img)
                        loaded_files.append(f'{anim_type}_{direction}_{frame_idx}: {os.path.basename(frame_path)}')
                        frame_idx += 1
                    except Exception as e:
                        print(f"Error loading {frame_path}: {e}")
                        break
                else:
                    break
            
            if frames:
                animations[anim_type][direction] = frames
    
    # If no animations loaded at all, return static image or None
    has_animations = any(animations['idle']) or any(animations['walk'])
    
    if not has_animations:
        if static_img:
            simple_dict = {}
            for direction in DIRECTIONS:
                simple_dict[direction] = [static_img]
            return {'idle': simple_dict, 'walk': simple_dict}, loaded_files
        return None, loaded_files
    
    return animations, loaded_files


def load_static_sprite(sprite_name, search_subfolders=True):
    """Load a static sprite (for resources)"""
    loaded_files = []
    sprite = None
    
    sprite_path = find_sprite_file(f'{sprite_name}.png', search_subfolders)
    
    if sprite_path:
        try:
            sprite = pygame.image.load(sprite_path).convert_alpha()
            loaded_files.append(f'Static: {os.path.basename(sprite_path)}')
        except Exception as e:
            print(f"Error loading {sprite_path}: {e}")
    
    return sprite, loaded_files


def get_sprite_folder_structure():
    """Scan and return the sprite folder structure"""
    structure = []
    
    if not os.path.exists(SPRITES_DIR):
        return ["Sprites folder does not exist"]
    
    for root, dirs, files in os.walk(SPRITES_DIR):
        rel_path = os.path.relpath(root, SPRITES_DIR)
        if rel_path == '.':
            folder_display = 'sprites/'
        else:
            folder_display = f'sprites/{rel_path}/'
        
        png_files = [f for f in files if f.lower().endswith('.png')]
        if png_files:
            structure.append(f"{folder_display} ({len(png_files)} files)")
            for file in png_files[:3]:
                structure.append(f"  - {file}")
            if len(png_files) > 3:
                structure.append(f"  ... and {len(png_files) - 3} more")
    
    if not structure:
        structure.append("No sprite files found in sprites folder")
    
    return structure


def iso_to_screen(x, y, cam_x, cam_y):
    from constants import TILE_W, TILE_H, SCREEN_W, SCREEN_H
    sx = (x - y) * (TILE_W // 2) - cam_x + SCREEN_W // 2
    sy = (x + y) * (TILE_H // 2) - cam_y + SCREEN_H // 2
    return int(sx), int(sy)

# Add these functions to utils.py
def rotate_world_coords_90_cw(x, y, map_width, map_height, current_rotation):
    """Rotate world coordinates 90 degrees clockwise"""
    if current_rotation % 4 == 0:
        return x, y
    elif current_rotation % 4 == 1:  # 90° clockwise
        return y, map_width - 1 - x
    elif current_rotation % 4 == 2:  # 180°
        return map_width - 1 - x, map_height - 1 - y
    else:  # 270° clockwise (or 90° counter-clockwise)
        return map_height - 1 - y, x

def rotate_direction_90_cw(direction, rotations):
    """Rotate a facing direction by 90-degree increments"""
    directions = ['north', 'east', 'south', 'west']
    if direction not in directions:
        return direction

    idx = directions.index(direction)
    return directions[(idx + rotations) % 4]

def rotate_movement_90_cw(dx, dy, rotations):
    """Rotate movement vector by 90-degree increments clockwise"""
    # 0 rotations: (dx, dy)
    # 1 rotation: (dy, -dx)
    # 2 rotations: (-dx, -dy)
    # 3 rotations: (-dy, dx)

    for _ in range(rotations % 4):
        dx, dy = dy, -dx

    return dx, dy