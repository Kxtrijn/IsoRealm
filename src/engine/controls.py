import pygame
from constants import *
from ui.debug_panel import DebugPanel
from ui.ui import UI

class Controls:
    def __init__(self, screen):
        self.screen = screen
        self.move_cooldown = 0
        self.game_time = 0
        self.last_move_time = 0
        self.debug_panel = DebugPanel(self.screen)

    def update(self, dt):
        """Update control timers"""
        self.move_cooldown = max(0, self.move_cooldown - dt)
        self.game_time += dt

    def check_auto_idle(self, player):
        """Check if player should automatically go idle"""
        if not player.is_moving:
            return False

        time_since_last_move = self.game_time - self.last_move_time
        if time_since_last_move > 200:
            player.is_moving = False
            player.move_timer = 0
            player.current_anim = 'idle'
            return True
        return False

    def handle_debug_keys(self, event, show_debug):
        """Handle debug/show toggles"""
        if event.key == pygame.K_F1:
            show_debug = not show_debug
        elif event.key == pygame.K_TAB:  # Add Tab for inventory toggle
            # Note: This is handled in ui_manager now
            pass
        elif event.key == pygame.K_ESCAPE:
            return show_debug, True  # Quit game
                
        return show_debug, False