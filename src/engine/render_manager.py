# engine/render_manager.py
"""
Manages the rendering pipeline and draw list preparation.
"""
class RenderManager:
    def __init__(self, camera):
        self.camera = camera
        
    def prepare_draw_list(self, game_map, player, monsters, resources):
        """Prepare a list of everything to draw with depth information"""
        draw_list = []
        
        # Add tiles first
        for x in range(game_map.w):
            for y in range(game_map.h):
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
        for resource in resources:
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
        for monster in monsters:
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
        sx, sy = self.camera.world_to_screen(player.x, player.y)
        depth = player.x + player.y + 0.3
        draw_list.append({
            'type': 'player',
            'depth': depth,
            'screen_x': sx,
            'screen_y': sy,
            'entity': player,
            'entity_type': 'player'
        })
        
        return draw_list
    
    def sort_draw_list(self, draw_list):
        """Sort draw list by depth"""
        return sorted(draw_list, key=lambda item: (item['depth'], item.get('entity_type', '')))