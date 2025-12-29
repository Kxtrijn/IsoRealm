# ui.py
import pygame
from constants import *


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 22)
        self.small_font = pygame.font.SysFont(None, 18)
        self.tiny_font = pygame.font.SysFont(None, 16)
        self.large_font = pygame.font.SysFont(None, 32)
        
        # Colors
        self.colors = {
            'ui_bg': COLOR_UI_BG,
            'ui_border': COLOR_UI_BORDER,
            'text': (255, 255, 255),
            'text_shadow': (0, 0, 0, 255),  # Semi-transparent black for shadows
            'text_secondary': (255, 255, 255),
            'text_highlight': (200, 220, 255),
            'health': (200, 0, 0),
            'health_bg': (50, 0, 0),
            'idle': (100, 255, 100),
            'walk': (255, 200, 100),
            'success': (150, 255, 150),
            'error': (255, 150, 150),
            'debug': (255, 255, 255),
            'folder_header': (255, 255, 200)
        }
    
    def draw_text_with_shadow(self, text, font, color, x, y, shadow_color=None, shadow_offset=(1, 1)):
        """Draw text with a shadow behind it for better readability"""
        if shadow_color is None:
            shadow_color = self.colors['text_shadow']
        
        # Create shadow surface
        shadow_surf = font.render(text, True, shadow_color)
        shadow_surf.set_alpha(shadow_color[3] if len(shadow_color) > 3 else 255)
        
        # Draw shadow
        self.screen.blit(shadow_surf, (x + shadow_offset[0], y + shadow_offset[1]))
        
        # Draw main text
        main_surf = font.render(text, True, color)
        self.screen.blit(main_surf, (x, y))
        
        return main_surf.get_size()

    def draw_health_bar(self, entity, screen_x, screen_y, frame_height, current_hp, max_hp, zoom=1.0):
        """Draw a health bar above an entity"""
        if current_hp >= max_hp:  # Don't draw full health bars
            return
    
        # Scale bar dimensions with zoom
        bar_width = int(30 * zoom)
        bar_height = max(2, int(4 * zoom))
        bar_x = screen_x - bar_width // 2
        # Position above the entity (screen_y is where to position the health bar)
        bar_y = screen_y
    
        # Draw shadow for health bar
        pygame.draw.rect(self.screen, (0, 0, 0, 100),
                         (bar_x + 1, bar_y + 1, bar_width, bar_height))
    
        # Draw background
        pygame.draw.rect(self.screen, self.colors['health_bg'],
                         (bar_x, bar_y, bar_width, bar_height))
    
        # Draw health fill
        health_width = int(bar_width * (current_hp / max_hp))
        pygame.draw.rect(self.screen, self.colors['health'],
                         (bar_x, bar_y, health_width, bar_height))
    
        # Draw border
        pygame.draw.rect(self.screen, (0, 0, 0, 120),
                         (bar_x, bar_y, bar_width, bar_height), 1)
    
    def draw_notification(self, message, color, duration, current_time):
        """Draw a temporary notification message (optional feature)"""
        # This is a placeholder for notification system
        pass
    
    def draw_entity_tooltip(self, entity, screen_x, screen_y, entity_type):
        """Draw a tooltip for an entity when hovered (optional feature)"""
        # This is a placeholder for tooltip system
        pass
    
    def draw_minimap(self, game_map, player, monsters, resources):
        """Draw a minimap in the corner (optional feature)"""
        # This is a placeholder for minimap system
        pass
    
    def clear_screen(self):
        """Clear the entire screen with background color"""
        self.screen.fill(COLOR_BACKGROUND)