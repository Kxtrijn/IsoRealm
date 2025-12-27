# renderer.py (updated)
import pygame
from ui import UI
from constants import *


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.ui = UI(screen)
        
    def clear(self):
        """Clear the screen"""
        self.ui.clear_screen()
    
    def draw_tile(self, tile_img, screen_x, screen_y):
        """Draw a tile at screen coordinates"""
        self.screen.blit(tile_img, (screen_x - TILE_W // 2, screen_y - TILE_H // 2))
    
    def draw_entity(self, entity, screen_x, screen_y, entity_type='entity'):
        """Draw an entity at screen coordinates"""
        frame = entity.get_current_frame()
        if not frame:
            return
            
        # Different vertical offsets for different entity types
        vertical_offset = -10
        frame_width, frame_height = frame.get_width(), frame.get_height()
        
        if entity_type == 'player':
            vertical_offset = -12
            # Visual effects for player
            if entity.current_anim == 'idle':
                pulse_size = 3 + int(2 * pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() / 50).y)
                pygame.draw.circle(self.screen, (100, 255, 100, 80), 
                                 (screen_x, screen_y + 20), pulse_size)
            elif entity.current_anim == 'walk':
                for i in range(2):
                    alpha = 150 - i * 75
                    offset = i * 2
                    trail_frame = frame.copy()
                    trail_frame.set_alpha(alpha)
                    self.screen.blit(trail_frame, 
                                   (screen_x - frame_width // 2 - offset, 
                                    screen_y - frame_height // 2 - 12 + offset))
        
        # Draw health bar for monsters with low HP
        if entity_type == 'monster' and entity.hp < 8:
            self.ui.draw_health_bar(entity, screen_x, screen_y, frame_height, entity.hp, 8)
        
        # Draw the entity
        self.screen.blit(frame, 
                        (screen_x - frame_width // 2, 
                         screen_y - frame_height // 2 + vertical_offset))
    
    def draw_hud(self, player, resources_left):
        """Draw the HUD"""
        self.ui.draw_hud(player, resources_left)
    
    def draw_state_indicator(self, player, resources_left):
        """Draw animation state indicator"""
        self.ui.draw_state_indicator(player, resources_left)
    
    def draw_debug_info(self, sprite_status, all_loaded_files, clock, player):
        """Draw debug information"""
        self.ui.draw_debug_info(sprite_status, all_loaded_files, clock, player)
    
    def draw_folder_structure(self, folder_structure):
        """Draw folder structure view"""
        self.ui.draw_folder_structure(folder_structure)