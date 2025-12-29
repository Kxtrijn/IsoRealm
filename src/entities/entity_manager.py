# engine/entity_manager.py
"""
Manages all game entities (player, monsters, resources).
"""
import pygame
from constants import *
import random
from constants import MONSTER_COUNT, RESOURCE_COUNT
from entities.player import Player
from entities.monster import Monster
from entities.resource import Resource


class EntityManager:
    def __init__(self, game_map, player_animations, monster_animations, resource_sprite):
        self.game_map = game_map
        self.player_animations = player_animations
        self.monster_animations = monster_animations
        self.resource_sprite = resource_sprite
        
        # Create entities
        self.player = None
        self.monsters = []
        self.resources = []

    def update(self, dt):
        """Update all entities"""
        self.player.update_animation(dt)
        for monster in self.monsters:
            monster.update_animation(dt)
            monster.update_ai(self.game_map)
        
    def initialize(self, player_start_x, player_start_y):
        """Initialize all entities"""
        # Create player
        self.player = Player(player_start_x, player_start_y, self.player_animations)
        
        # Create monsters
        self.monsters = self.create_monsters()
        
        # Create resources
        self.resources = self.create_resources()
            
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