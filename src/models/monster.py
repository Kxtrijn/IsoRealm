from models.entities import Entity
import random


class Monster(Entity):
    def __init__(self, x, y, img):
        super().__init__(x, y, img, hp=8)
        self.anim_speed = 150
        self.facing = random.choice(['north', 'south', 'east', 'west'])
        self.current_anim = 'idle'
    
    def update_ai(self, game_map):
        """Simple AI for monster movement"""
        if random.random() < 0.015:
            mdx = random.choice([-1, 0, 1])
            mdy = random.choice([-1, 0, 1])
            
            if mdx != 0 or mdy != 0:
                self.set_facing_direction(mdx, mdy)
                new_x = self.x + mdx
                new_y = self.y + mdy
                
                # Check bounds
                if 0 <= new_x < game_map.w and 0 <= new_y < game_map.h:
                    self.x = new_x
                    self.y = new_y
            else:
                self.is_moving = False