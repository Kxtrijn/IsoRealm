import pygame
from constants import MOVE_COOLDOWN


class Controls:
    def __init__(self):
        self.move_cooldown = 0
        self.game_time = 0
        self.last_move_time = 0
        
    def update(self, dt):
        """Update control timers"""
        self.move_cooldown = max(0, self.move_cooldown - dt)
        self.game_time += dt
        
    def handle_player_movement(self, player, game_map):
        """Handle player movement input"""
        if self.move_cooldown > 0:
            return False, (0, 0)
        
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        else:
            return False, (0, 0)
        
        if player.move(dx, dy, game_map):
            self.move_cooldown = MOVE_COOLDOWN
            self.last_move_time = self.game_time
            return True, (dx, dy)
        
        return False, (0, 0)
    
    def handle_player_actions(self, keys, player, monsters, resources):
        """Handle player action input"""
        actions = {
            'attacked': False,
            'gathered': False
        }
        
        if keys[pygame.K_SPACE]:
            actions['attacked'] = player.attack(monsters)
        
        if keys[pygame.K_e]:
            actions['gathered'] = player.gather_resource(resources)
            
        return actions
    
    def handle_debug_keys(self, event, show_debug, show_structure):
        """Handle debug/show toggles"""
        if event.key == pygame.K_F1:
            show_debug = not show_debug
        elif event.key == pygame.K_F2:
            show_structure = not show_structure
        elif event.key == pygame.K_ESCAPE:
            return show_debug, show_structure, True  # Quit game
        
        return show_debug, show_structure, False
    
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