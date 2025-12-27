import random
from constants import MAP_W, MAP_H


class GameMap:
    def __init__(self, w=MAP_W, h=MAP_H):
        self.w = w
        self.h = h
        self.tiles = [[self.random_tile(x, y) for y in range(h)] for x in range(w)]
        self.resources = {}

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