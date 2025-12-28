import random
from constants import MAP_W, MAP_H


# Update game_map.py
class GameMap:
    def __init__(self, w=MAP_W, h=MAP_H):
        self.w = w
        self.h = h
        self.rotation = 0  # 0, 1, 2, 3 for 0°, 90°, 180°, 270°
        self.original_tiles = [[self.random_tile(x, y) for y in range(h)] for x in range(w)]
        self.tiles = [row[:] for row in self.original_tiles]
        self.resources = {}

    def rotate_90_clockwise(self):
        """Rotate the map 90 degrees clockwise"""
        self.rotation = (self.rotation + 1) % 4

        # Rotate the tile grid
        self.tiles = self._rotate_grid_90_clockwise(self.tiles)

        # Swap width and height
        self.w, self.h = self.h, self.w

    def _rotate_grid_90_clockwise(self, grid):
        """Helper to rotate a 2D grid 90 degrees clockwise"""
        if not grid:
            return grid

        h = len(grid)
        w = len(grid[0])
        rotated = [[None for _ in range(h)] for _ in range(w)]

        for y in range(h):
            for x in range(w):
                rotated[x][h - 1 - y] = grid[y][x]

        return rotated

    def get_tile_at_world(self, world_x, world_y):
        """Get tile at world coordinates, taking rotation into account"""
        # For now, just return the tile at the grid position
        if self.in_bounds(world_x, world_y):
            return self.tiles[world_x][world_y]
        return 'grass'

    # ... rest of the class remains the same ...

    def random_tile(self, x, y):
        r = random.random()
        if r < 0.06:
            return 'water'
        if r < 0.13:
            return 'stone'
        if r < 0.2:
            return 'sand'
        return 'grass'

    def in_bounds(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h
    
    def get_tile_type(self, x, y):
        if self.in_bounds(x, y):
            return self.tiles[x][y]
        return 'grass'