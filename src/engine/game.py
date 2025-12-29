# game.py - update handle_events and HUD
import pygame
import random
from constants import *
from world.game_map import GameMap
from engine.camera import Camera
from engine.renderer import Renderer
from engine.controls import Controls
from entities.player import Player
from utils.loader import *
from utils.fallbacks import *
from entities.entity_manager import EntityManager
from engine.player_manager import PlayerController
from world.world_manager import WorldRotator
from engine.render_manager import RenderManager
from ui.hud import HUD
from ui.ui import UI
from ui.debug_panel import DebugPanel

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

        # Initialize managers
        self.player_controller = PlayerController(self.controls)  # <-- ADD THIS LINE
        self.world_rotator = WorldRotator()                       # If you created this
        self.render_manager = RenderManager(self.camera)          # If you created this

        self.rotation = 0  # 0 = 0°, 1 = 90°, 2 = 180°, 3 = 270°
        self.rotation_timer = 0  # Timer for smooth rotation
        self.target_rotation = 0  # Target rotation for animation
        self.is_rotating = False  # Whether rotation animation is active

        # Load assets
        self.load_assets()

        # Create game world
        self.game_map = GameMap()  # <-- CREATE MAP HERE

        self.entity_manager = EntityManager(
        self.game_map, 
        self.player_animations, 
        self.monster_animations, 
        self.resource_sprite
        )

        self.entity_manager.initialize(MAP_W // 2, MAP_H // 2)
        self.player = self.entity_manager.player
        self.monsters = self.entity_manager.monsters
        self.resources = self.entity_manager.resources

        # Game state
        self.show_debug = True
        self.show_structure = False
        self.running = True
        self.all_loaded_files = []

        # Initialize components (Renderer now has UI built-in)
        self.debug_panel = DebugPanel(self.screen)
        self.hud = HUD(self.screen)

        self.sprite_offset = 0  # Current sprite offset

    def load_assets(self): # kat
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

                # Handle R key for instant rotation
                if event.key == pygame.K_r:
                    self.rotation = self.world_rotator.rotate_world_90(
                        self.game_map, 
                        self.camera, 
                        self.player, 
                        self.monsters, 
                        self.resources
                    )

                # Handle plus/minus keys for zoom - instant zoom
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.camera.zoom_in(ZOOM_SPEED * 0.5, pygame.mouse.get_pos())  # Instant zoom
                elif event.key == pygame.K_MINUS:
                    self.camera.zoom_out(ZOOM_SPEED * 0.5, pygame.mouse.get_pos())  # Instant zoom
                elif event.key == pygame.K_0:
                    self.camera.reset_zoom()  # Instant zoom reset

                # Handle sprite offset adjustment keys
                elif event.key == pygame.K_UP:
                    self.sprite_offset -= 5  # Move sprites up
                    self.renderer.set_sprite_offset(self.sprite_offset)
                    print(f"Sprite offset: {self.sprite_offset}")
                elif event.key == pygame.K_DOWN:
                    self.sprite_offset += 5  # Move sprites down
                    self.renderer.set_sprite_offset(self.sprite_offset)
                    print(f"Sprite offset: {self.sprite_offset}")
                elif event.key == pygame.K_HOME:
                    self.sprite_offset = 0  # Reset offset
                    self.renderer.set_sprite_offset(self.sprite_offset)
                    print(f"Sprite offset reset to: {self.sprite_offset}")

            elif event.type == pygame.MOUSEWHEEL:
                # Mouse wheel zoom with mouse position as center point - instant zoom
                mouse_pos = pygame.mouse.get_pos()
                if event.y > 0:  # Scroll up - zoom in
                    self.camera.zoom_in(ZOOM_SPEED, mouse_pos)  # Instant zoom
                elif event.y < 0:  # Scroll down - zoom out
                    self.camera.zoom_out(ZOOM_SPEED, mouse_pos)  # Instant zoom

    def update(self, dt):
        """Update game state"""
        # Update controls
        self.controls.update(dt)

        # Handle player movement
        keys = pygame.key.get_pressed()
        moved, (dx, dy) = self.player_controller.handle_movement(
        self.player, self.game_map, keys
        )

        # Handle auto idle
        self.controls.check_auto_idle(self.player)

        # Handle player actions (attack on space, gathering on 'g')
        action_result, action_type = self.player_controller.handle_actions(
            self.player, self.monsters, self.resources, keys
        )

        # Update animations
        self.entity_manager.update(dt)

        # Update camera
        self.camera.update(self.player.x, self.player.y)

    def render(self):
        """Render the game"""
        self.renderer.clear()
    
        # Get the draw list
        draw_list = self.prepare_draw_list()
    
        # Sort by depth (y then x for isometric)
        draw_list.sort(key=lambda item: (item['depth'], item.get('entity_type', '')))
    
        # Draw everything in sorted order
        for item in draw_list:
            sx, sy = item['screen_x'], item['screen_y']
    
            if item['type'] == 'tile':
                x, y = item['map_x'], item['map_y']
                tile_type = self.game_map.tiles[x][y]
                img = self.tileset.get(tile_type, list(self.tileset.values())[0])
    
                # Draw tile EXACTLY centered
                self.renderer.draw_tile(img, sx, sy, self.camera.zoom)
    
            elif item['type'] == 'resource':
                resource = item['entity']
                self.renderer.draw_entity(resource, sx, sy, 'resource', self.camera.zoom)
    
            elif item['type'] == 'monster':
                monster = item['entity']
                self.renderer.draw_entity(monster, sx, sy, 'monster', self.camera.zoom)
    
            elif item['type'] == 'player':
                self.renderer.draw_entity(self.player, sx, sy, 'player', self.camera.zoom)
    
        # Draw grid dots EXACTLY at tile centers
        tile_list = [item for item in draw_list if item['type'] == 'tile']
        self.debug_panel.draw_grid_dots(tile_list, self.camera.zoom)
    
        # Draw HUD and UI with sprite offset info
        resources_left = len([r for r in self.resources if not r.collected])
        self.hud.draw_hud(self.player, resources_left, self.rotation, self.camera.zoom, self.sprite_offset)
    
        if self.show_debug:
            self.debug_panel.draw_debug_info(self.sprite_status, self.all_loaded_files, self.clock, self.player, self.camera.zoom)
    
        if self.show_structure:
            self.debug_panel.draw_folder_structure(self.folder_structure)
    
        pygame.display.flip()

    def prepare_draw_list(self):
        """Prepare a list of everything to draw with depth information"""
        draw_list = []
    
        # Add tiles first
        for x in range(self.game_map.w):
            for y in range(self.game_map.h):
                sx, sy = self.camera.world_to_screen(x, y)
                # Calculate depth based on isometric position
                depth = x + y  # Basic isometric depth
                draw_list.append({
                    'type': 'tile',
                    'depth': depth,
                    'screen_x': sx,
                    'screen_y': sy,
                    'map_x': x,
                    'map_y': y
                })
    
        # Add resources
        for resource in self.resources:
            if not resource.collected:
                sx, sy = self.camera.world_to_screen(resource.x, resource.y)
                # Resources should appear on top, so add a small offset to depth
                depth = resource.x + resource.y + 0.1
                draw_list.append({
                    'type': 'resource',
                    'depth': depth,
                    'screen_x': sx,
                    'screen_y': sy,
                    'entity': resource,
                    'entity_type': 'resource'
                })
    
        # Add monsters
        for monster in self.monsters:
            sx, sy = self.camera.world_to_screen(monster.x, monster.y)
            # Monsters should appear on top of resources
            depth = monster.x + monster.y + 0.2
            draw_list.append({
                'type': 'monster',
                'depth': depth,
                'screen_x': sx,
                'screen_y': sy,
                'entity': monster,
                'entity_type': 'monster'
            })
    
        # Add player (always on top)
        sx, sy = self.camera.world_to_screen(self.player.x, self.player.y)
        depth = self.player.x + self.player.y + 0.3
        draw_list.append({
            'type': 'player',
            'depth': depth,
            'screen_x': sx,
            'screen_y': sy,
            'entity': self.player,
            'entity_type': 'player'
        })
    
        return draw_list

    # game.py - in the run() method
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS)  # dt is in milliseconds      
            # Cap dt to prevent large jumps
            dt = min(dt, 100)  # Cap at 100ms to prevent huge jumps
            
            self.handle_events()
            self.update(dt)
            self.render()
    
        pygame.quit()