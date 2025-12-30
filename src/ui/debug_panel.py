import pygame
from constants import *
from ui.ui import UI

class DebugPanel:
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

        self.ui = UI(self.screen)

    # ui.py - add zoom parameter to draw_debug_info
    def draw_debug_info(self, sprite_status, all_loaded_files, clock, player, zoom=1.0, show_debug=False):
        """Draw debug information panel (only if show_debug is True)"""
        if not show_debug:
            return
            
        debug_y = SCREEN_H - 180

        # Sprite status header with shadow
        self.ui.draw_text_with_shadow(
            "Sprite Status:", self.font, self.colors['debug'],
            8, debug_y
        )
        debug_y += 25

        # Sprite status lines with shadows
        for i, status in enumerate(sprite_status):
            color = self.colors['success'] if "✓" in status else self.colors['error']
            self.ui.draw_text_with_shadow(
                status, self.small_font, color,
                12, debug_y + i * 18
            )

        debug_y += len(sprite_status) * 18 + 15

        # File info and FPS with shadow - include zoom info
        file_info = f"Total files loaded: {len(all_loaded_files)} | FPS: {int(clock.get_fps())} | Zoom: {zoom:.1f}x"
        self.ui.draw_text_with_shadow(
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
            self.ui.draw_text_with_shadow(
                line, self.small_font, self.colors['text_highlight'],
                8, debug_y + i * 18
            )

    def draw_grid_dots(self, visible_tiles, zoom=1.0, show_debug=False):
        """
        Draw grid dots EXACTLY at tile centers.
        visible_tiles should be a list of dictionaries with 'screen_x', 'screen_y' keys.
        Only draws if show_debug is True.
        """
        if not show_debug:
            return
            
        for tile in visible_tiles:
            sx, sy = tile['screen_x'], tile['screen_y']
            # Scale dot size with zoom
            dot_radius = max(1, int(3 * zoom))
            # Draw a small dot EXACTLY at the tile center (sprite feet position)
            pygame.draw.circle(self.screen, (255, 255, 255, 180), (sx, sy), dot_radius)
            # Draw a subtle border around the dot for better visibility
            pygame.draw.circle(self.screen, (0, 0, 0, 100), (sx, sy), dot_radius, 1)