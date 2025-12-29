# camera.py - add mouse wheel zoom handling
import pygame
from constants import TILE_W, TILE_H, SCREEN_W, SCREEN_H, ZOOM_MIN, ZOOM_MAX, ZOOM_SPEED, DEFAULT_ZOOM

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.zoom = DEFAULT_ZOOM
        self.target_zoom = DEFAULT_ZOOM

    def update(self, target_world_x, target_world_y, smoothing=0.2, zoom_smoothing=0.1):
        """Update camera position and zoom with smoothing"""
        # Update zoom with smoothing
        self.zoom += (self.target_zoom - self.zoom) * zoom_smoothing

        # Clamp zoom
        self.zoom = max(ZOOM_MIN, min(ZOOM_MAX, self.zoom))

        # Calculate effective tile dimensions based on zoom
        effective_tile_w = int(TILE_W * self.zoom)
        effective_tile_h = int(TILE_H * self.zoom)

        # Calculate target screen position for the target entity
        self.target_x = (target_world_x - target_world_y) * (effective_tile_w // 2)
        self.target_y = (target_world_x + target_world_y) * (effective_tile_h // 2)

        # Smoothly move camera toward target
        self.x += (self.target_x - self.x) * smoothing
        self.y += (self.target_y - self.y) * smoothing

    def world_to_screen(self, world_x, world_y):
        """Convert world (grid) coordinates to screen coordinates with zoom"""
        # Calculate effective tile dimensions based on zoom
        effective_tile_w = int(TILE_W * self.zoom)
        effective_tile_h = int(TILE_H * self.zoom)

        # Convert world coordinates to screen position relative to camera
        screen_x = (world_x - world_y) * (effective_tile_w // 2) - self.x + SCREEN_W // 2
        screen_y = (world_x + world_y) * (effective_tile_h // 2) - self.y + SCREEN_H // 2
        return int(screen_x), int(screen_y)

    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world (grid) coordinates (approximate) with zoom"""
        # Calculate effective tile dimensions based on zoom
        effective_tile_w = int(TILE_W * self.zoom)
        effective_tile_h = int(TILE_H * self.zoom)

        # Convert screen position to world relative to camera
        rel_x = screen_x - SCREEN_W // 2 + self.x
        rel_y = screen_y - SCREEN_H // 2 + self.y

        # Reverse the isometric projection with zoom
        world_x = (rel_x / (effective_tile_w // 2) + rel_y / (effective_tile_h // 2)) // 2
        world_y = (rel_y / (effective_tile_h // 2) - rel_x / (effective_tile_w // 2)) // 2

        return int(world_x), int(world_y)

    def zoom_in(self, amount=ZOOM_SPEED, mouse_pos=None):
        """Zoom in at mouse position or center"""
        old_zoom = self.zoom

        # Store mouse world position before zoom if mouse_pos provided
        if mouse_pos:
            mouse_world_x, mouse_world_y = self.screen_to_world(mouse_pos[0], mouse_pos[1])

        # Update zoom
        self.target_zoom = min(ZOOM_MAX, self.target_zoom + amount)

        # Adjust camera position to zoom at mouse point
        if mouse_pos and old_zoom != self.target_zoom:
            # Adjust camera to keep the same world point under the mouse
            new_mouse_screen_x, new_mouse_screen_y = self.world_to_screen(mouse_world_x, mouse_world_y)
            offset_x = mouse_pos[0] - new_mouse_screen_x
            offset_y = mouse_pos[1] - new_mouse_screen_y
            self.x -= offset_x
            self.y -= offset_y
            self.target_x -= offset_x
            self.target_y -= offset_y

    def zoom_out(self, amount=ZOOM_SPEED, mouse_pos=None):
        """Zoom out at mouse position or center"""
        old_zoom = self.zoom

        # Store mouse world position before zoom if mouse_pos provided
        if mouse_pos:
            mouse_world_x, mouse_world_y = self.screen_to_world(mouse_pos[0], mouse_pos[1])

        # Update zoom
        self.target_zoom = max(ZOOM_MIN, self.target_zoom - amount)

        # Adjust camera position to zoom at mouse point
        if mouse_pos and old_zoom != self.target_zoom:
            # Adjust camera to keep the same world point under the mouse
            new_mouse_screen_x, new_mouse_screen_y = self.world_to_screen(mouse_world_x, mouse_world_y)
            offset_x = mouse_pos[0] - new_mouse_screen_x
            offset_y = mouse_pos[1] - new_mouse_screen_y
            self.x -= offset_x
            self.y -= offset_y
            self.target_x -= offset_x
            self.target_y -= offset_y

    def set_zoom(self, zoom_level, mouse_pos=None):
        """Set zoom to specific level"""
        old_zoom = self.zoom

        # Store mouse world position before zoom if mouse_pos provided
        if mouse_pos:
            mouse_world_x, mouse_world_y = self.screen_to_world(mouse_pos[0], mouse_pos[1])

        # Update zoom
        self.target_zoom = max(ZOOM_MIN, min(ZOOM_MAX, zoom_level))

        # Adjust camera position to zoom at mouse point
        if mouse_pos and abs(old_zoom - self.target_zoom) > 0.01:
            # Adjust camera to keep the same world point under the mouse
            new_mouse_screen_x, new_mouse_screen_y = self.world_to_screen(mouse_world_x, mouse_world_y)
            offset_x = mouse_pos[0] - new_mouse_screen_x
            offset_y = mouse_pos[1] - new_mouse_screen_y
            self.x -= offset_x
            self.y -= offset_y
            self.target_x -= offset_x
            self.target_y -= offset_y

    def reset_zoom(self):
        """Reset zoom to default"""
        self.target_zoom = DEFAULT_ZOOM
        self.zoom = DEFAULT_ZOOM

    def center_on(self, world_x, world_y):
        """Immediately center camera on position"""
        effective_tile_w = int(TILE_W * self.zoom)
        effective_tile_h = int(TILE_H * self.zoom)

        self.x = (world_x - world_y) * (effective_tile_w // 2)
        self.y = (world_x + world_y) * (effective_tile_h // 2)
        self.target_x = self.x
        self.target_y = self.y

    def get_view_center(self):
        """Get the world coordinates at the center of the screen"""
        return self.screen_to_world(SCREEN_W // 2, SCREEN_H // 2)

    def get_tile_center(self, world_x, world_y):
        """Get the exact screen center of a tile at given world coordinates"""
        return self.world_to_screen(world_x, world_y)

    def is_visible(self, world_x, world_y, margin=100):
        """Check if a world position is visible on screen"""
        screen_x, screen_y = self.world_to_screen(world_x, world_y)
        return (-margin <= screen_x <= SCREEN_W + margin and
                -margin <= screen_y <= SCREEN_H + margin)

    def get_effective_tile_size(self):
        """Get the current tile size based on zoom"""
        return int(TILE_W * self.zoom), int(TILE_H * self.zoom)