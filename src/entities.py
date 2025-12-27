class Entity:
    def __init__(self, x, y, img, hp=10):
        self.x = x
        self.y = y
        self.img = img
        self.hp = hp
        
        # Animation properties
        self.anim_frame = 0
        self.anim_timer = 0
        self.anim_speed = 200
        
        # Animation state
        self.facing = 'south'
        self.is_moving = False
        self.move_timer = 0
        self.idle_timer = 0
        self.current_anim = 'idle'
        self.was_moving = False  # Track previous movement state
        
    def update_animation(self, dt):
        """Update animation based on time passed"""
        # Only animate if we have animation frames
        if isinstance(self.img, dict) or (isinstance(self.img, list) and len(self.img) > 1):
            self.anim_timer += dt
            
            # Track if we just stopped moving
            just_stopped = False
            if self.was_moving and not self.is_moving:
                just_stopped = True
            self.was_moving = self.is_moving
            
            # Update timers based on movement state
            if not self.is_moving:
                self.idle_timer += dt
                
                # Switch to idle animation immediately when stopping
                if self.current_anim != 'idle' and (just_stopped or self.move_timer > 150):
                    self.current_anim = 'idle'
                    self.anim_frame = 0
                    self.anim_timer = 0
            else:
                self.idle_timer = 0
                if self.current_anim != 'walk':
                    self.current_anim = 'walk'
                    self.anim_frame = 0
                    self.anim_timer = 0
            
            # Get current animation frames
            frames = self.get_current_frames()
            if frames and len(frames) > 1:
                # Adjust animation speed based on state
                current_speed = self.anim_speed
                if self.current_anim == 'idle':
                    current_speed = self.anim_speed * 3  # Slower for idle
                elif self.current_anim == 'walk':
                    current_speed = self.anim_speed  # Normal for walking
                
                # Advance frame
                if self.anim_timer >= current_speed:
                    self.anim_timer = 0
                    self.anim_frame = (self.anim_frame + 1) % len(frames)
            
            # Handle movement timer decay
            if self.is_moving:
                self.move_timer += dt
                if self.move_timer > 180:  # Slightly longer to prevent flickering
                    self.is_moving = False
                    self.move_timer = 0
            else:
                # Gradually reduce move_timer when not moving
                self.move_timer = max(0, self.move_timer - dt * 2)
    
    def get_current_frames(self):
        """Get the current animation frames based on state"""
        if isinstance(self.img, dict):
            if 'idle' in self.img and 'walk' in self.img:
                anim_dict = self.img.get(self.current_anim, {})
                if anim_dict:
                    return anim_dict.get(self.facing, [])
            elif self.facing in self.img:
                return self.img.get(self.facing, [])
        return []
    
    def get_current_frame(self):
        """Get the current frame to display"""
        if isinstance(self.img, dict):
            frames = self.get_current_frames()
            if frames:
                return frames[self.anim_frame % len(frames)]
            return None
        elif isinstance(self.img, list):
            # For simple frame lists (like resources)
            if self.img:
                return self.img[self.anim_frame % len(self.img)]
            return None
        else:
            # Static image
            return self.img
    
    def set_facing_direction(self, dx, dy):
        """Set facing direction based on movement"""
        if dx > 0:
            self.facing = 'east'
        elif dx < 0:
            self.facing = 'west'
        elif dy > 0:
            self.facing = 'south'
        elif dy < 0:
            self.facing = 'north'
        self.is_moving = True
        self.move_timer = 0
        self.current_anim = 'walk'
        self.was_moving = True