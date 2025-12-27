from entities import Entity


class Resource(Entity):
    """Static resource - doesn't use animation system"""
    def __init__(self, x, y, img):
        super().__init__(x, y, img, hp=1)
        self.collected = False
    
    def update_animation(self, dt):
        """Resources don't animate - override parent method"""
        pass
    
    def get_current_frame(self):
        """Resources just return their static image"""
        return self.img