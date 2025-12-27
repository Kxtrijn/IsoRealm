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
            'text_shadow': (0, 0, 0, 180),  # Semi-transparent black for shadows
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
    
    def draw_hud(self, player, resources_left):
        """Draw the main HUD with player stats and controls"""
        hud_y = 8
        
        # Main stats - drawn with shadow
        anim_state = "IDLE" if player.current_anim == 'idle' else "WALKING"
        state_color = self.colors['idle'] if player.current_anim == 'idle' else self.colors['walk']
        
        # Render HUD text with shadow
        hud_text = f'HP: {player.hp} | Resources: {player.inv.get("resource", 0)} | Remaining: {resources_left} | State: '
        txt_width, _ = self.draw_text_with_shadow(
            hud_text, self.font, self.colors['text'], 8, hud_y
        )
        
        # Draw state text with shadow
        self.draw_text_with_shadow(
            anim_state, self.font, state_color, 8 + txt_width, hud_y
        )
        
        hud_y += 25
        
        # Controls with shadows
        controls = [
            "Arrows/WASD: Move (auto idle when stopped)",
            "Space: Attack adjacent | E: Gather resource",
            "F1: Toggle debug | F2: Toggle folder view",
            "ESC: Quit"
        ]
        
        for i, line in enumerate(controls):
            self.draw_text_with_shadow(
                line, self.small_font, self.colors['text_secondary'], 
                8, hud_y + i * 18
            )
    
    def draw_debug_info(self, sprite_status, all_loaded_files, clock, player):
        """Draw debug information panel"""
        debug_y = SCREEN_H - 180
        
        # Sprite status header with shadow
        self.draw_text_with_shadow(
            "Sprite Status:", self.font, self.colors['debug'], 
            8, debug_y
        )
        debug_y += 25
        
        # Sprite status lines with shadows
        for i, status in enumerate(sprite_status):
            color = self.colors['success'] if "✓" in status else self.colors['error']
            self.draw_text_with_shadow(
                status, self.small_font, color, 
                12, debug_y + i * 18
            )
        
        debug_y += len(sprite_status) * 18 + 15
        
        # File info and FPS with shadow
        file_info = f"Total files loaded: {len(all_loaded_files)} | FPS: {int(clock.get_fps())}"
        self.draw_text_with_shadow(
            file_info, self.small_font, self.colors['debug'], 
            8, debug_y
        )
        debug_y += 20
        
        # Player info with shadows
        player_info = [
            f"Position: ({player.x}, {player.y})",
            f"Facing: {player.facing} | Frame: {player.anim_frame}"
        ]
        
        for i, line in enumerate(player_info):
            self.draw_text_with_shadow(
                line, self.small_font, self.colors['text_highlight'], 
                8, debug_y + i * 18
            )
    
    def draw_folder_structure(self, folder_structure):
        """Draw folder structure view panel"""
        struct_x = SCREEN_W - 350
        struct_y = 100
        struct_width = 340
        struct_height = 400
        
        # Draw background
        struct_bg = pygame.Rect(struct_x, struct_y, struct_width, struct_height)
        pygame.draw.rect(self.screen, (30, 30, 40, 220), struct_bg)
        pygame.draw.rect(self.screen, (70, 70, 90), struct_bg, 2)
        
        # Header with shadow
        header_x = struct_x + 10
        header_y = struct_y + 10
        header_surf = self.font.render("SPRITE FOLDER STRUCTURE", True, self.colors['folder_header'])
        shadow_surf = self.font.render("SPRITE FOLDER STRUCTURE", True, (0, 0, 0, 180))
        
        # Draw shadow then main text
        self.screen.blit(shadow_surf, (header_x + 2, header_y + 2))
        self.screen.blit(header_surf, (header_x, header_y))
        
        # Structure content with shadows
        content_y = struct_y + 40
        max_lines = 18
        
        for i, line in enumerate(folder_structure[:max_lines]):
            # Different color for folder names vs file names
            color = (220, 220, 255) if '/' in line else (180, 200, 180)
            shadow_color = (0, 0, 0, 180)
            
            # Create shadow surface
            shadow_surf = self.tiny_font.render(line, True, shadow_color)
            shadow_surf.set_alpha(180)
            
            # Draw shadow
            self.screen.blit(shadow_surf, (struct_x + 17, content_y + i * 16 + 2))
            
            # Draw main text
            main_surf = self.tiny_font.render(line, True, color)
            self.screen.blit(main_surf, (struct_x + 15, content_y + i * 16))
        
        # Show "more" indicator with shadow
        if len(folder_structure) > max_lines:
            more_text = f"... {len(folder_structure) - max_lines} more lines"
            more_x = struct_x + 15
            more_y = content_y + max_lines * 16
            
            # Shadow
            shadow_surf = self.tiny_font.render(more_text, True, (0, 0, 0, 180))
            shadow_surf.set_alpha(180)
            self.screen.blit(shadow_surf, (more_x + 2, more_y + 2))
            
            # Main text
            main_surf = self.tiny_font.render(more_text, True, (180, 180, 200))
            self.screen.blit(main_surf, (more_x, more_y))
        
        # Footer with shadow
        footer_text = "Press F2 to hide"
        footer_x = struct_x + 10
        footer_y = struct_y + struct_height - 25
        
        # Shadow
        shadow_surf = self.small_font.render(footer_text, True, (0, 0, 0, 180))
        shadow_surf.set_alpha(180)
        self.screen.blit(shadow_surf, (footer_x + 2, footer_y + 2))
        
        # Main text
        main_surf = self.small_font.render(footer_text, True, self.colors['text_secondary'])
        self.screen.blit(main_surf, (footer_x, footer_y))
    
    def draw_health_bar(self, entity, screen_x, screen_y, frame_height, current_hp, max_hp):
        """Draw a health bar above an entity"""
        if current_hp >= max_hp:  # Don't draw full health bars
            return
        
        bar_width = 30
        bar_height = 4
        bar_x = screen_x - bar_width // 2
        bar_y = screen_y - frame_height // 2 - 15
        
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