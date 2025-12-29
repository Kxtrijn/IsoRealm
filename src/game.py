# game.py - update handle_events and HUD
import pygame
import random
from constants import *
from world.game_map import GameMap
from view.camera import Camera
from ui.renderer import Renderer
from input import Controls
from models.player import Player
from models.monster import Monster
from resource import Resource
from loaders.assets_loader import *

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

        self.rotation = 0  # 0 = 0°, 1 = 90°, 2 = 180°, 3 = 270°
        self.rotation_timer = 0  # Timer for smooth rotation
        self.target_rotation = 0  # Target rotation for animation
        self.is_rotating = False  # Whether rotation animation is active

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

        self.sprite_offset = 0  # Current sprite offset

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

                # Handle R key for instant rotation
                if event.key == pygame.K_r:
                    self.rotate_world_90()  # This is now instant

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
        moved, (dx, dy) = self.handle_player_movement(keys)

        # Handle auto idle
        self.controls.check_auto_idle(self.player)

        # Handle player actions (attack on space, gathering on 'g')
        self.handle_player_actions(keys)

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
        self.renderer.draw_grid_dots(tile_list, self.camera.zoom)
    
        # Draw HUD and UI with sprite offset info
        resources_left = len([r for r in self.resources if not r.collected])
        self.renderer.draw_hud(self.player, resources_left, self.rotation, self.camera.zoom, self.sprite_offset)
    
        if self.show_debug:
            self.renderer.draw_debug_info(self.sprite_status, self.all_loaded_files, self.clock, self.player, self.camera.zoom)
    
        if self.show_structure:
            self.renderer.draw_folder_structure(self.folder_structure)
    
        pygame.display.flip()

    def rotate_world_90(self):
        """Rotate the entire world 90 degrees clockwise INSTANTLY"""
        # Rotate the map
        self.game_map.rotate_90_clockwise()

        # Update rotation counter
        self.rotation = (self.rotation + 1) % 4

        print(f"World rotated 90° clockwise (rotation: {self.rotation})")

        # Adjust all entity positions for rotation
        self.adjust_entities_for_rotation()

        # Force immediate camera update for instant rotation feel
        self.camera.center_on(self.player.x, self.player.y)

    def adjust_entities_for_rotation(self):
        """Adjust all entity positions for the current rotation"""
        map_w, map_h = self.game_map.w, self.game_map.h

        # Adjust player position
        self.player.x, self.player.y = self.rotate_point_90_cw(
            self.player.x, self.player.y, map_w, map_h
        )

        # Adjust monster positions
        for monster in self.monsters:
            monster.x, monster.y = self.rotate_point_90_cw(
                monster.x, monster.y, map_w, map_h
            )

        # Adjust resource positions
        for resource in self.resources:
            resource.x, resource.y = self.rotate_point_90_cw(
                resource.x, resource.y, map_w, map_h
            )

    def rotate_point_90_cw(self, x, y, map_w, map_h):
        """Rotate a point 90 degrees clockwise around map center"""
        # Map center
        center_x = map_w / 2 - 0.5
        center_y = map_h / 2 - 0.5

        # Translate to origin
        rel_x = x - center_x
        rel_y = y - center_y

        # Rotate 90 degrees clockwise: (x, y) -> (y, -x)
        new_x = rel_y
        new_y = -rel_x

        # Translate back and clamp to bounds
        new_x = max(0, min(map_w - 1, new_x + center_x))
        new_y = max(0, min(map_h - 1, new_y + center_y))

        return int(round(new_x)), int(round(new_y))

    def handle_player_actions(self, keys):
        """Handle player action input"""
        if keys[pygame.K_SPACE]:
            self.player.attack(self.monsters)

        # Gathering on 'g' key
        if keys[pygame.K_g]:
            if self.player.gather_resource(self.resources):
                print(f"Collected resource! Total: {self.player.inv['resource']}")

    def handle_player_movement(self, keys):
        """Handle player movement WITHOUT rotation adjustment"""
        if self.controls.move_cooldown > 0:
            return False, (0, 0)

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

        # NO rotation adjustment - movement is always relative to screen
        if self.player.move(dx, dy, self.game_map):
            self.controls.move_cooldown = MOVE_COOLDOWN
            self.controls.last_move_time = self.controls.game_time
            return True, (dx, dy)

        return False, (0, 0)

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
            dt = self.clock.tick(FPS)  # Keep FPS consistent
    
            # Cap dt to prevent large jumps
            dt = min(dt, 100)  # Cap at 100ms to prevent huge jumps
    
            self.handle_events()
            self.update(dt)
            self.render()
    
        pygame.quit()