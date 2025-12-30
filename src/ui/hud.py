import pygame
from constants import *
from ui.ui import UI


class HUD:
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

    # ui.py - update draw_hud method
    def draw_hud(self, player, resources_left, rotation=0, zoom=1.0, sprite_offset=0):
        """Draw the main HUD with player stats and controls"""
        hud_y = 8

        # Main stats
        anim_state = "IDLE" if player.current_anim == 'idle' else "WALKING"
        state_color = self.colors['idle'] if player.current_anim == 'idle' else self.colors['walk']

        # Add rotation, zoom, and sprite offset to HUD
        rotation_text = f"Rotation: {rotation * 90}°"
        zoom_text = f"Zoom: {zoom:.1f}x"
        offset_text = f"Sprite Offset: {sprite_offset}"

        hud_text = f'HP: {player.hp} | Resources: {player.inv.get("resource", 0)} | Remaining: {resources_left} | State: '
        txt_width, _ = self.ui.draw_text_with_shadow(
            hud_text, self.font, self.colors['text'], 8, hud_y
        )

        # Draw state text
        self.ui.draw_text_with_shadow(
            anim_state, self.font, state_color, 8 + txt_width, hud_y
        )

        hud_y += 25

        # Add rotation, zoom, and offset info
        self.ui.draw_text_with_shadow(
            rotation_text, self.font, (200, 220, 255), 8, hud_y
        )

        rot_txt_width, _ = self.font.size(rotation_text)
        self.ui.draw_text_with_shadow(
            zoom_text, self.font, (220, 255, 200), 8 + rot_txt_width + 20, hud_y
        )

        zoom_txt_width, _ = self.font.size(zoom_text)
        self.ui.draw_text_with_shadow(
            offset_text, self.font, (255, 220, 200), 8 + rot_txt_width + 20 + zoom_txt_width + 20, hud_y
        )

        hud_y += 25

        # Update controls list to include offset controls
        controls = [
            "Arrows/WASD: Move | Space: Attack | G: Gather | R: Rotate world",
            "Mouse Wheel/+/-: Zoom | 0: Reset zoom | Up/Down: Adjust sprite offset | Home: Reset offset",
            "F1: Toggle debug | ESC: Quit"
            "I: Inventory | 1-9: Select hotbar"
        ]

        for i, line in enumerate(controls):
            self.ui.draw_text_with_shadow(
                line, self.small_font, self.colors['text_secondary'],
                8, hud_y + i * 18
            )