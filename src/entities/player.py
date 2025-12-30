from entities.base_entity import Entity
import constants


# [file name]: player.py (fix parameter handling)
class Player(Entity):
    def __init__(self, x, y, img):
        super().__init__(x, y, img, hp=constants.PLAYER_HP)
        self.inv = {'resource': 0}  # Keep backward compatibility
        self.anim_speed = constants.ANIM_SPEED_PLAYER

    def move(self, dx, dy, game_map):
        """Move player and update animation state"""
        new_x = self.x + dx
        new_y = self.y + dy

        # Check bounds
        if 0 <= new_x < game_map.w and 0 <= new_y < game_map.h:
            self.x = new_x
            self.y = new_y
            self.set_facing_direction(dx, dy)
            return True
        return False

    def attack(self, monsters):
        """Attack adjacent monsters"""
        attacked = False
        for monster in monsters[:]:
            if abs(monster.x - self.x) + abs(monster.y - self.y) == 1:
                monster.hp -= 6
                monster.anim_timer = 0
                monster.current_anim = 'walk'
                monster.move_timer = 0
                if monster.hp <= 0:
                    monsters.remove(monster)
                attacked = True
        return attacked

    def gather_resource(self, resources, inventory=None):
        """Gather resource at current position"""
        for resource in resources[:]:
            if resource.x == self.x and resource.y == self.y and not resource.collected:
                if inventory:
                    # Use the new inventory system
                    inventory.add_item('resource', 1)
                else:
                    # Fallback to old system
                    self.inv['resource'] = self.inv.get('resource', 0) + 1
                
                resource.collected = True
                resources.remove(resource)
                return True
        return False
    
    # Keep the old method signature for backward compatibility
    def gather_resource_old(self, resources):
        """Old method signature for backward compatibility"""
        return self.gather_resource(resources, None)