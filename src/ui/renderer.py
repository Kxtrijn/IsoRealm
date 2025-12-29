# renderer.py - add adjustable sprite offset
import pygame
from ui.ui import UI
from constants import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.ui = UI(screen)
        self.sprite_offset = SPRITE_VERTICAL_OFFSET  # Load from constants

    def clear(self):
        """Clear the screen"""
        self.ui.clear_screen()

    def draw_tile(self, tile_img, screen_x, screen_y, zoom=1.0):
        """Draw a tile at screen coordinates with zoom - EXACTLY CENTERED"""
        # Scale the tile image if zoom is not 1.0
        if abs(zoom - 1.0) > 0.01:
            # Get the scaled dimensions
            original_width, original_height = tile_img.get_size()
            scaled_width = int(original_width * zoom)
            scaled_height = int(original_height * zoom)

            # Scale the image
            scaled_img = pygame.transform.scale(tile_img, (scaled_width, scaled_height))

            # Draw EXACTLY centered at screen_x, screen_y
            self.screen.blit(scaled_img,
                             (screen_x - scaled_width // 2,
                              screen_y - scaled_height // 2))
        else:
            # Draw at original size
            original_width, original_height = tile_img.get_size()
            self.screen.blit(tile_img,
                             (screen_x - original_width // 2,
                              screen_y - original_height // 2))

    def draw_entity(self, entity, screen_x, screen_y, entity_type='entity', zoom=1.0):
        """Draw an entity at screen coordinates with zoom - WITH ADJUSTABLE OFFSET"""
        frame = entity.get_current_frame()
        if not frame:
            return

        # Scale the frame if needed
        if abs(zoom - 1.0) > 0.01:
            original_width, original_height = frame.get_size()
            scaled_width = int(original_width * zoom)
            scaled_height = int(original_height * zoom)
            frame = pygame.transform.scale(frame, (scaled_width, scaled_height))

        # Get current frame dimensions (might be scaled)
        frame_width, frame_height = frame.get_width(), frame.get_height()

        # Base vertical offset to position sprite between dots
        base_offset = -frame_height // 2  # Move sprite up by half its height

        # Add adjustable offset from constants
        adjustable_offset = self.sprite_offset * zoom

        # Entity-specific adjustments
        if entity_type == 'player':
            entity_adjustment = -24 * zoom  # Player slightly higher
        elif entity_type == 'monster':
            entity_adjustment = -24 * zoom  # Monster slightly higher
        elif entity_type == 'resource':
            entity_adjustment = 0  # Resource at standard position
        else:
            entity_adjustment = 0

        # Total vertical offset
        vertical_offset = base_offset + adjustable_offset + entity_adjustment

        # Visual effects for player (scaled with zoom)
        if entity_type == 'player':
            if entity.current_anim == 'idle':
                pulse_size = (3 + int(2 * pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() / 50).y)) * zoom
                # Position pulse effect at the sprite's feet (tile center)
                pygame.draw.circle(self.screen, (100, 255, 100, 80),
                                   (screen_x, screen_y), int(pulse_size))
            elif entity.current_anim == 'walk':
                for i in range(2):
                    alpha = 150 - i * 75
                    offset = i * 2 * zoom
                    trail_frame = frame.copy()
                    trail_frame.set_alpha(alpha)
                    self.screen.blit(trail_frame,
                                     (screen_x - frame_width // 2 - offset,
                                      screen_y - frame_height // 2 + vertical_offset + offset))

        # Draw health bar for monsters with low HP
        if entity_type == 'monster' and entity.hp < 8:
            # Position health bar above the entity
            bar_y_offset = -frame_height - 5 * zoom
            self.ui.draw_health_bar(entity, screen_x,
                                    screen_y - frame_height // 2 + vertical_offset + bar_y_offset,
                                    frame_height, entity.hp, 8, zoom)

        # Draw the entity with adjustable offset
        self.screen.blit(frame,
                         (screen_x - frame_width // 2,
                          screen_y - frame_height // 2 + vertical_offset))

    def draw_grid_dots(self, visible_tiles, zoom=1.0):
        """
        Draw grid dots EXACTLY at tile centers.
        visible_tiles should be a list of dictionaries with 'screen_x', 'screen_y' keys.
        """
        for tile in visible_tiles:
            sx, sy = tile['screen_x'], tile['screen_y']

            # Scale dot size with zoom
            dot_radius = max(1, int(3 * zoom))

            # Draw a small dot EXACTLY at the tile center (sprite feet position)
            pygame.draw.circle(self.screen, (255, 255, 255, 180), (sx, sy), dot_radius)

            # Draw a subtle border around the dot for better visibility
            pygame.draw.circle(self.screen, (0, 0, 0, 100), (sx, sy), dot_radius, 1)

    # ... rest of the methods remain the same ...

    # renderer.py - fix draw_hud signature
    def draw_hud(self, player, resources_left, rotation=0, zoom=1.0, sprite_offset=0):
        """Draw the HUD"""
        self.ui.draw_hud(player, resources_left, rotation, zoom, sprite_offset)

    def draw_state_indicator(self, player, resources_left):
        """Draw animation state indicator"""
        self.ui.draw_state_indicator(player, resources_left)

    def draw_debug_info(self, sprite_status, all_loaded_files, clock, player, zoom=1.0):
        """Draw debug information"""
        self.ui.draw_debug_info(sprite_status, all_loaded_files, clock, player, zoom)

    def draw_folder_structure(self, folder_structure):
        """Draw folder structure view"""
        self.ui.draw_folder_structure(folder_structure)

    def set_sprite_offset(self, offset):
        """Change the sprite vertical offset at runtime"""
        self.sprite_offset = offset

    def get_sprite_offset(self):
        """Get the current sprite vertical offset"""
        return self.sprite_offset