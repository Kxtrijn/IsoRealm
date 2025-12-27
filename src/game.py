import pygame
import random
from constants import *
from game_map import GameMap
from camera import Camera
from renderer import Renderer
from input import Controls
from player import Player
from monster import Monster
from resource import Resource
from assets_loader import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption('IsoRealm - Static Resources')
        self.clock = pygame.time.Clock()
        
        # Initialize components
        self.controls = Controls()
        self.renderer = Renderer(self.screen)
        self.camera = Camera()
        
        # Load assets
        self.load_assets()
        
        # Create game world
        self.game_map = GameMap()
        self.player = Player(MAP_W // 2, MAP_H // 2, self.player_animations)
        self.monsters = self.create_monsters()
        self.resources = self.create_resources()
        
        # Game state
        self.show_debug = True
        self.show_structure = False
        self.running = True
        self.all_loaded_files = []

        # Initialize components (Renderer now has UI built-in)
        self.controls = Controls()
        self.renderer = Renderer(self.screen)  # This now contains UI
        
    def load_assets(self):
        """Load all game assets"""
        # Only create directories
        ensure_dirs()
        
        # Load tiles
        self.tileset = load_tile_images()
        
        # Get folder structure for display
        self.folder_structure = get_sprite_folder_structure()
        
        # Load animated sprites WITH subfolder search enabled
        self.player_animations, player_files = load_entity_animations('player', search_subfolders=True)
        self.monster_animations, monster_files = load_entity_animations('monster', search_subfolders=True)
        
        # Load STATIC resource sprite
        self.resource_sprite, resource_files = load_static_sprite('resource', search_subfolders=True)
        
        # Track all loaded files
        self.all_loaded_files = []
        self.all_loaded_files.extend(player_files)
        self.all_loaded_files.extend(monster_files)
        self.all_loaded_files.extend(resource_files)
        
        # Check sprite status
        self.sprite_status = []
        if self.player_animations:
            self.sprite_status.append(f"✓ Player: {len(player_files)} files loaded")
        else:
            self.sprite_status.append("✗ Player sprites missing")
            
        if self.monster_animations:
            self.sprite_status.append(f"✓ Monster: {len(monster_files)} files loaded")
        else:
            self.sprite_status.append("✗ Monster sprites missing")
            
        if self.resource_sprite:
            self.sprite_status.append(f"✓ Resource: Static sprite loaded")
        else:
            self.sprite_status.append("✗ Resource sprite missing")
        
        # Create fallback sprites if needed
        if not self.player_animations:
            self.player_animations = {'idle': {'south': [create_fallback_sprite((220, 80, 80), 48)]},
                                    'walk': {'south': [create_fallback_sprite((220, 80, 80), 48)]}}
        
        if not self.monster_animations:
            self.monster_animations = {'idle': {'south': [create_fallback_sprite((120, 40, 160), 48)]},
                                     'walk': {'south': [create_fallback_sprite((120, 40, 160), 48)]}}
        
        if not self.resource_sprite:
            self.resource_sprite = create_fallback_sprite((200, 180, 60), 32)
    
    def create_monsters(self):
        """Create monster entities"""
        monsters = []
        for _ in range(MONSTER_COUNT):
            x = random.randrange(0, MAP_W)
            y = random.randrange(0, MAP_H)
            monster = Monster(x, y, self.monster_animations)
            monsters.append(monster)
        return monsters
    
    def create_resources(self):
        """Create resource entities with unique positions"""
        resources = []
        resource_positions = set()
        
        for _ in range(RESOURCE_COUNT):
            attempts = 0
            while attempts < 100:
                x = random.randrange(0, MAP_W)
                y = random.randrange(0, MAP_H)
                
                # Check if position is occupied
                if (x, y) not in resource_positions:
                    player_here = (x == self.player.x and y == self.player.y)
                    monster_here = any(m.x == x and m.y == y for m in self.monsters)
                    
                    if not player_here and not monster_here:
                        resource = Resource(x, y, self.resource_sprite)
                        resources.append(resource)
                        resource_positions.add((x, y))
                        break
                
                attempts += 1
        
        print(f"Generated {len(resources)} resources in the world")
        return resources
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.show_debug, self.show_structure, should_quit = \
                    self.controls.handle_debug_keys(event, self.show_debug, self.show_structure)
                if should_quit:
                    self.running = False
    
    def update(self, dt):
        """Update game state"""
        # Update controls
        self.controls.update(dt)
        
        # Handle player movement
        keys = pygame.key.get_pressed()
        moved, (dx, dy) = self.controls.handle_player_movement(self.player, self.game_map)
        
        # Handle auto idle
        self.controls.check_auto_idle(self.player)
        
        # Handle player actions
        actions = self.controls.handle_player_actions(keys, self.player, self.monsters, self.resources)
        if actions['gathered']:
            print(f"Collected resource! Total: {self.player.inv['resource']}")
        
        # Update animations
        self.player.update_animation(dt)
        for monster in self.monsters:
            monster.update_animation(dt)
            monster.update_ai(self.game_map)
        
        # Update camera
        self.camera.update(self.player.x, self.player.y)
    
    def render(self):
        """Render the game"""
        self.renderer.clear()
        
        # Prepare draw list for depth sorting
        draw_list = self.prepare_draw_list()
        
        # Sort by depth
        draw_list.sort(key=lambda item: item['depth'])
        
        # Draw everything
        for item in draw_list:
            sx, sy = item['screen_x'], item['screen_y']
            
            if item['type'] == 'tile':
                x, y = item['map_x'], item['map_y']
                tile_type = self.game_map.tiles[x][y]
                img = self.tileset.get(tile_type, list(self.tileset.values())[0])
                self.renderer.draw_tile(img, sx, sy)
            
            elif item['type'] == 'resource':
                resource = item['entity']
                self.renderer.draw_entity(resource, sx, sy, 'resource')
            
            elif item['type'] == 'monster':
                monster = item['entity']
                self.renderer.draw_entity(monster, sx, sy, 'monster')
            
            elif item['type'] == 'player':
                self.renderer.draw_entity(self.player, sx, sy, 'player')
        
        # Draw HUD and UI
        self.renderer.draw_hud(self.player, len(self.resources))
        
        if self.show_debug:
            self.renderer.draw_debug_info(self.sprite_status, self.all_loaded_files, self.clock, self.player)
        
        if self.show_structure:
            self.renderer.draw_folder_structure(self.folder_structure)
        
        pygame.display.flip()
    
    def prepare_draw_list(self):
        """Prepare a list of everything to draw with depth information"""
        draw_list = []
        
        # Add tiles
        for x in range(self.game_map.w):
            for y in range(self.game_map.h):
                sx, sy = self.camera.world_to_screen(x, y)
                draw_list.append({
                    'type': 'tile',
                    'depth': x + y,
                    'screen_x': sx,
                    'screen_y': sy,
                    'map_x': x,
                    'map_y': y
                })
        
        # Add resources
        for resource in self.resources:
            if not resource.collected:
                sx, sy = self.camera.world_to_screen(resource.x, resource.y)
                draw_list.append({
                    'type': 'resource',
                    'depth': resource.x + resource.y,
                    'screen_x': sx,
                    'screen_y': sy,
                    'entity': resource
                })
        
        # Add monsters
        for monster in self.monsters:
            sx, sy = self.camera.world_to_screen(monster.x, monster.y)
            draw_list.append({
                'type': 'monster',
                'depth': monster.x + monster.y,
                'screen_x': sx,
                'screen_y': sy,
                'entity': monster
            })
        
        # Add player
        sx, sy = self.camera.world_to_screen(self.player.x, self.player.y)
        draw_list.append({
            'type': 'player',
            'depth': self.player.x + self.player.y,
            'screen_x': sx,
            'screen_y': sy,
            'entity': self.player
        })
        
        return draw_list
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS)
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()