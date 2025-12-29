# engine/world_rotator.py
"""
Handles world rotation and coordinate transformations.
"""
import pygame
import math
from constants import *


class WorldRotator:
    def __init__(self):
        self.rotation = 0  # 0, 1, 2, 3 for 0°, 90°, 180°, 270°
        
    def rotate_world_90(self, game_map, camera, player, monsters, resources):
        """Rotate the entire world 90 degrees clockwise INSTANTLY"""
        # Rotate the map
        game_map.rotate_90_clockwise()
        
        # Update rotation counter
        self.rotation = (self.rotation + 1) % 4
        
        # Adjust all entity positions for rotation
        self.adjust_entities_for_rotation(game_map, player, monsters, resources)
        
        # Force immediate camera update for instant rotation feel
        camera.center_on(player.x, player.y)
        
        return self.rotation
    
    def adjust_entities_for_rotation(self, game_map, player, monsters, resources):
        """Adjust all entity positions for the current rotation"""
        map_w, map_h = game_map.w, game_map.h
        
        # Adjust player position
        player.x, player.y = self.rotate_point_90_cw(
            player.x, player.y, map_w, map_h
        )
        
        # Adjust monster positions
        for monster in monsters:
            monster.x, monster.y = self.rotate_point_90_cw(
                monster.x, monster.y, map_w, map_h
            )
        
        # Adjust resource positions
        for resource in resources:
            resource.x, resource.y = self.rotate_point_90_cw(
                resource.x, resource.y, map_w, map_h
            )
    
    def rotate_point_90_cw(self, x, y, map_w, map_h):
        """Rotate a point 90 degrees clockwise around map center"""
        # Map center
        center_x = map_w / 2 - 0.5
        center_y = map_h / 2 - 0.5
        
        # Translate to origin
        rel_x = x - center_x
        rel_y = y - center_y
        
        # Rotate 90 degrees clockwise: (x, y) -> (y, -x)
        new_x = rel_y
        new_y = -rel_x
        
        # Translate back and clamp to bounds
        new_x = max(0, min(map_w - 1, new_x + center_x))
        new_y = max(0, min(map_h - 1, new_y + center_y))
        
        return int(round(new_x)), int(round(new_y))
    
    def rotate_direction(self, dx, dy, rotations):
        """Rotate a movement vector by given number of 90° rotations"""
        for _ in range(rotations % 4):
            dx, dy = dy, -dx
        return dx, dy