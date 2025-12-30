# engine/player_controller.py
"""
Handles player movement and actions.
"""
import pygame
from constants import *

# [file name]: player_manager.py (update)
# Update the handle_actions method to not require keys parameter for certain actions

class PlayerController:
    def __init__(self, controls):
        self.controls = controls
        
    def handle_movement(self, player, game_map, keys):
        """Handle player movement WITHOUT rotation adjustment"""
        
        if self.controls.move_cooldown > 0:
            return False, (0, 0)

        dx, dy = 0, 0
        # Always check keys, even during cooldown
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        
        # If no movement keys pressed
        if dx == 0 and dy == 0:
            return False, (0, 0)
        
        # Only check cooldown if we're actually trying to move
        if self.controls.move_cooldown > 0:
            return False, (0, 0)

        # NO rotation adjustment - movement is always relative to screen
        if player.move(dx, dy, game_map):
            self.controls.move_cooldown = MOVE_COOLDOWN
            self.controls.last_move_time = self.controls.game_time
            return True, (dx, dy)

        return False, (0, 0)
    
    def handle_actions(self, player, monsters, resources, keys=None):
        """Handle player action input"""
        # If keys parameter is provided, check for key presses
        if keys is not None:
            if keys[pygame.K_SPACE]:
                return player.attack(monsters), 'attack'
            
            if keys[pygame.K_g]:
                if player.gather_resource(resources):
                    return True, 'gather'
        
        return False, None