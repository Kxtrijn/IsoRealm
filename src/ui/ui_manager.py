# [file name]: ui_manager.py (add item dragging and resource sprites)
import pygame
import os
from constants import *

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.inventory_visible = False
        self.hotbar_always_visible = True
        
        # Load UI textures
        self.inventory_bg = self.load_texture('inventory.png', INVENTORY_WIDTH, INVENTORY_HEIGHT)
        self.chest_bg = self.load_texture('chest.png', INVENTORY_WIDTH, INVENTORY_HEIGHT)
        self.hotbar_bg = self.load_texture('hotbar.png', HOTBAR_WIDTH, HOTBAR_HEIGHT)
        
        # Load item sprites
        self.item_sprites = self.load_item_sprites()
        
        # Calculate positions
        self.inventory_pos = (SCREEN_W // 2 - INVENTORY_WIDTH // 2, 
                             SCREEN_H // 2 - INVENTORY_HEIGHT // 2)
        self.hotbar_pos = (SCREEN_W // 2 - HOTBAR_WIDTH // 2, 
                          SCREEN_H - HOTBAR_HEIGHT - UI_MARGIN)
        
        # Mouse hover tracking
        self.hovered_slot = None
        self.selected_hotbar_slot = 0
        
        # Item dragging
        self.dragging_item = None
        self.dragging_from_slot = None
        self.drag_offset = (0, 0)
        
        # Font for UI
        self.font = pygame.font.SysFont(None, 24)
        self.small_font = pygame.font.SysFont(None, 20)
    
    def load_texture(self, filename, width, height):
        """Load a texture file - returns None if not found"""
        try:
            texture_path = os.path.join(BASE_DIR, 'assets', 'ui', filename)
            
            if os.path.exists(texture_path):
                texture = pygame.image.load(texture_path).convert_alpha()
                return pygame.transform.scale(texture, (width, height))
            else:
                return None
        
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None
    
    def load_item_sprites(self):
        """Load sprites for different item types"""
        sprites = {}
        
        # Try to load resource sprite
        try:
            resource_path = os.path.join(SPRITES_DIR, 'resources', 'resource.png')
            if os.path.exists(resource_path):
                resource_img = pygame.image.load(resource_path).convert_alpha()
                # Scale to fit in slot
                scaled_resource = pygame.transform.scale(resource_img, (SLOT_SIZE - 8, SLOT_SIZE - 8))
                sprites['resource'] = scaled_resource
            else:
                # Try alternative path
                alt_path = os.path.join(BASE_DIR, 'assets', 'sprites', 'resource.png')
                if os.path.exists(alt_path):
                    resource_img = pygame.image.load(alt_path).convert_alpha()
                    scaled_resource = pygame.transform.scale(resource_img, (SLOT_SIZE - 8, SLOT_SIZE - 8))
                    sprites['resource'] = scaled_resource
                else:
                    print(f"Resource sprite not found at {resource_path} or {alt_path}")
        except Exception as e:
            print(f"Error loading resource sprite: {e}")
        
        # You can add more item sprites here
        # sprites['sword'] = load_sword_sprite()
        # sprites['potion'] = load_potion_sprite()
        
        return sprites
    
    def draw_hotbar(self, inventory):
        """Draw the hotbar"""
        # Only draw background if texture exists
        if self.hotbar_bg is not None:
            self.screen.blit(self.hotbar_bg, self.hotbar_pos)
        
        # Calculate slot positions
        hotbar_x, hotbar_y = self.hotbar_pos
        start_x = hotbar_x + (HOTBAR_WIDTH - (HOTBAR_SLOTS * (SLOT_SIZE + SLOT_MARGIN))) // 2
        start_y = hotbar_y + (HOTBAR_HEIGHT - SLOT_SIZE) // 2
        
        # Draw hotbar slots
        for i in range(HOTBAR_SLOTS):
            slot_x = start_x + i * (SLOT_SIZE + SLOT_MARGIN)
            slot_y = start_y
            
            # Check if slot is hovered
            mouse_pos = pygame.mouse.get_pos()
            slot_rect = pygame.Rect(slot_x, slot_y, SLOT_SIZE, SLOT_SIZE)
            is_hovered = slot_rect.collidepoint(mouse_pos)
            is_selected = (i == self.selected_hotbar_slot)
            
            # Determine slot color
            if is_selected:
                slot_color = COLOR_SLOT_SELECTED
            elif is_hovered:
                slot_color = COLOR_SLOT_HOVER
            else:
                slot_color = COLOR_SLOT_EMPTY
            
            # Draw slot background
            pygame.draw.rect(self.screen, slot_color, slot_rect, border_radius=4)
            pygame.draw.rect(self.screen, COLOR_UI_BORDER, slot_rect, 1, border_radius=4)
            
            # Draw slot number
            number_text = self.small_font.render(str(i + 1), True, COLOR_TEXT_UI)
            self.screen.blit(number_text, (slot_x + 2, slot_y + 2))
            
            # Draw item in slot if it exists and we're not dragging from this slot
            if i < len(inventory.hotbar):
                item = inventory.hotbar[i]
                if (item and item['count'] > 0 and 
                    not (self.dragging_item and self.dragging_from_slot == 
                         ((INVENTORY_ROWS - 1) * INVENTORY_COLS + i))):
                    
                    # Draw item sprite or colored square
                    self.draw_item(item, slot_x + 4, slot_y + 4)
        
        return start_x, start_y
    
    def draw_inventory(self, inventory):
        """Draw the full inventory when opened"""
        if not self.inventory_visible:
            return
        
        # Draw inventory background if texture exists
        if self.inventory_bg is not None:
            self.screen.blit(self.inventory_bg, self.inventory_pos)
        
        # Calculate slot grid positions
        inv_x, inv_y = self.inventory_pos
        grid_width = INVENTORY_COLS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN
        grid_height = INVENTORY_ROWS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN
        
        start_x = inv_x + (INVENTORY_WIDTH - grid_width) // 2
        start_y = inv_y + (INVENTORY_HEIGHT - grid_height) // 2
        
        # Draw all inventory slots
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_slot = None
        
        for row in range(INVENTORY_ROWS):
            for col in range(INVENTORY_COLS):
                slot_index = row * INVENTORY_COLS + col
                slot_x = start_x + col * (SLOT_SIZE + SLOT_MARGIN)
                slot_y = start_y + row * (SLOT_SIZE + SLOT_MARGIN)
                
                # Check if this is a hotbar slot (bottom row)
                is_hotbar_slot = (row == INVENTORY_ROWS - 1)
                is_selected_hotbar = is_hotbar_slot and (col == self.selected_hotbar_slot)
                
                # Check if slot is hovered
                slot_rect = pygame.Rect(slot_x, slot_y, SLOT_SIZE, SLOT_SIZE)
                is_hovered = slot_rect.collidepoint(mouse_pos)
                
                if is_hovered:
                    self.hovered_slot = slot_index
                
                # Determine slot color
                if is_selected_hotbar:
                    slot_color = COLOR_SLOT_SELECTED
                elif is_hovered:
                    slot_color = COLOR_SLOT_HOVER
                elif is_hotbar_slot:
                    slot_color = COLOR_SLOT_FILLED
                else:
                    slot_color = COLOR_SLOT_EMPTY
                
                # Draw slot background
                pygame.draw.rect(self.screen, slot_color, slot_rect, border_radius=4)
                pygame.draw.rect(self.screen, COLOR_UI_BORDER, slot_rect, 1, border_radius=4)
                
                # Draw slot number
                slot_number = inventory.get_slot_number_display(slot_index)
                if slot_number:
                    number_text = self.small_font.render(slot_number, True, COLOR_TEXT_UI)
                    self.screen.blit(number_text, (slot_x + 2, slot_y + 2))
                
                # Draw item in slot if it exists and we're not dragging from this slot
                if (slot_index < len(inventory.slots) and 
                    not (self.dragging_item and self.dragging_from_slot == slot_index)):
                    item = inventory.slots[slot_index]
                    if item and item['count'] > 0:
                        # Draw item
                        self.draw_item(item, slot_x + 4, slot_y + 4)
        
        # Draw dragged item on top of everything
        if self.dragging_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            draw_x = mouse_x - self.drag_offset[0]
            draw_y = mouse_y - self.drag_offset[1]
            self.draw_item(self.dragging_item, draw_x, draw_y)
        
        # Draw hover tooltip (if not dragging)
        if self.hovered_slot is not None and not self.dragging_item:
            self.draw_item_tooltip(inventory, mouse_pos[0], mouse_pos[1])
    
    def draw_item(self, item, x, y):
        """Draw an item at specified position"""
        item_type = item['type']
        
        # Try to use sprite if available
        if item_type in self.item_sprites:
            sprite = self.item_sprites[item_type]
            self.screen.blit(sprite, (x, y))
            
            # Draw count on top of sprite
            if item['count'] > 1:
                count_text = self.small_font.render(str(item['count']), True, COLOR_TEXT_UI)
                # Draw semi-transparent background for count
                count_bg = pygame.Surface((count_text.get_width() + 4, count_text.get_height() + 2), 
                                         pygame.SRCALPHA)
                count_bg.fill((0, 0, 0, 150))
                self.screen.blit(count_bg, (x + SLOT_SIZE - 8 - count_text.get_width() - 6, 
                                          y + SLOT_SIZE - 8 - count_text.get_height() - 2))
                self.screen.blit(count_text, (x + SLOT_SIZE - 8 - count_text.get_width() - 4, 
                                            y + SLOT_SIZE - 8 - count_text.get_height()))
        else:
            # Fallback to colored square
            item_color = self.get_item_color(item_type)
            pygame.draw.rect(self.screen, item_color, 
                            (x, y, SLOT_SIZE - 8, SLOT_SIZE - 8), 
                            border_radius=2)
            
            # Draw item count
            if item['count'] > 1:
                count_text = self.small_font.render(str(item['count']), True, COLOR_TEXT_UI)
                self.screen.blit(count_text, (x + SLOT_SIZE - 8 - count_text.get_width() - 4, 
                                            y + SLOT_SIZE - 8 - count_text.get_height() - 2))
    
    # [file name]: ui_manager.py (fix color handling)
    # Update the draw_item_tooltip method:

    def draw_item_tooltip(self, inventory, mouse_x, mouse_y):
        """Draw tooltip for hovered item"""
        if self.hovered_slot >= len(inventory.slots):
            return
        
        item = inventory.slots[self.hovered_slot]
        if not item or item['count'] <= 0:
            return
        
        # Create tooltip text
        slot_number = inventory.get_slot_number_display(self.hovered_slot)
        item_name = ITEM_TYPES.get(item['type'], item['type'].title())
        item_desc = f"Slot: {slot_number} | Count: {item['count']}"
        
        # Render text surfaces
        name_surf = self.font.render(item_name, True, COLOR_TEXT_UI[:3])  # Use RGB only for font
        desc_surf = self.small_font.render(item_desc, True, COLOR_TEXT_UI[:3])  # Use RGB only for font
        
        # Calculate tooltip dimensions
        padding = 8
        tooltip_width = max(name_surf.get_width(), desc_surf.get_width()) + padding * 2
        tooltip_height = name_surf.get_height() + desc_surf.get_height() + padding * 3
        
        # Position tooltip
        tooltip_x = mouse_x + 20
        tooltip_y = mouse_y + 20
        
        if tooltip_x + tooltip_width > SCREEN_W:
            tooltip_x = mouse_x - tooltip_width - 10
        if tooltip_y + tooltip_height > SCREEN_H:
            tooltip_y = mouse_y - tooltip_height - 10
        
        # Draw tooltip with semi-transparent background
        tooltip_surface = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
        
        # Use the color directly (it should already have alpha)
        pygame.draw.rect(tooltip_surface, COLOR_UI_BACKGROUND, 
                        (0, 0, tooltip_width, tooltip_height), border_radius=4)
        pygame.draw.rect(tooltip_surface, COLOR_UI_BORDER, 
                        (0, 0, tooltip_width, tooltip_height), 1, border_radius=4)
        
        self.screen.blit(tooltip_surface, (tooltip_x, tooltip_y))
        
        # Draw text
        self.screen.blit(name_surf, (tooltip_x + padding, tooltip_y + padding))
        self.screen.blit(desc_surf, (tooltip_x + padding, tooltip_y + padding + name_surf.get_height() + 4))
    
    def handle_events(self, event, inventory):
        """Handle UI-related events including dragging"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.inventory_visible = not self.inventory_visible
            elif pygame.K_1 <= event.key <= pygame.K_9:
                self.selected_hotbar_slot = event.key - pygame.K_1
            elif event.key == pygame.K_LEFT:
                self.selected_hotbar_slot = (self.selected_hotbar_slot - 1) % HOTBAR_SLOTS
            elif event.key == pygame.K_RIGHT:
                self.selected_hotbar_slot = (self.selected_hotbar_slot + 1) % HOTBAR_SLOTS
        
        elif event.type == pygame.MOUSEBUTTONDOWN and self.inventory_visible:
            if event.button == 1:  # Left mouse button
                if self.hovered_slot is not None:
                    # Start dragging item
                    if (self.hovered_slot < len(inventory.slots) and 
                        inventory.slots[self.hovered_slot] and 
                        inventory.slots[self.hovered_slot]['count'] > 0):
                        
                        self.dragging_item = inventory.slots[self.hovered_slot].copy()
                        self.dragging_from_slot = self.hovered_slot
                        
                        # Calculate drag offset (where in the item we clicked)
                        mouse_pos = pygame.mouse.get_pos()
                        inv_x, inv_y = self.inventory_pos
                        grid_width = INVENTORY_COLS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN
                        grid_height = INVENTORY_ROWS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN
                        
                        start_x = inv_x + (INVENTORY_WIDTH - grid_width) // 2
                        start_y = inv_y + (INVENTORY_HEIGHT - grid_height) // 2
                        
                        row = self.hovered_slot // INVENTORY_COLS
                        col = self.hovered_slot % INVENTORY_COLS
                        
                        item_x = start_x + col * (SLOT_SIZE + SLOT_MARGIN) + 4
                        item_y = start_y + row * (SLOT_SIZE + SLOT_MARGIN) + 4
                        
                        self.drag_offset = (mouse_pos[0] - item_x, mouse_pos[1] - item_y)
        
        elif event.type == pygame.MOUSEBUTTONUP and self.inventory_visible:
            if event.button == 1:  # Left mouse button released
                if self.dragging_item and self.hovered_slot is not None:
                    # Move item to new slot
                    self.move_item(inventory, self.dragging_from_slot, self.hovered_slot)
                
                # Reset dragging state
                self.dragging_item = None
                self.dragging_from_slot = None
                self.drag_offset = (0, 0)
    
    def move_item(self, inventory, from_slot, to_slot):
        """Move item from one slot to another"""
        if from_slot == to_slot:
            return  # Same slot, do nothing
        
        if (from_slot >= len(inventory.slots) or to_slot >= len(inventory.slots) or
            from_slot < 0 or to_slot < 0):
            return  # Invalid slot
        
        from_item = inventory.slots[from_slot]
        to_item = inventory.slots[to_slot]
        
        # If both slots have items of the same type, merge them
        if from_item and to_item and from_item['type'] == to_item['type']:
            # Merge counts
            to_item['count'] += from_item['count']
            inventory.slots[from_slot] = None
        elif to_item is None:
            # Move item to empty slot
            inventory.slots[to_slot] = from_item
            inventory.slots[from_slot] = None
        else:
            # Swap items
            inventory.slots[from_slot], inventory.slots[to_slot] = \
                inventory.slots[to_slot], from_item
        
        # Update hotbar
        inventory.sync_hotbar()
    
    def update(self, inventory):
        """Update UI state"""
        inventory.sync_hotbar()
        
        # Update hovered slot even when dragging
        if self.inventory_visible:
            mouse_pos = pygame.mouse.get_pos()
            inv_x, inv_y = self.inventory_pos
            grid_width = INVENTORY_COLS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN
            grid_height = INVENTORY_ROWS * (SLOT_SIZE + SLOT_MARGIN) - SLOT_MARGIN
            
            start_x = inv_x + (INVENTORY_WIDTH - grid_width) // 2
            start_y = inv_y + (INVENTORY_HEIGHT - grid_height) // 2
            
            self.hovered_slot = None
            
            for row in range(INVENTORY_ROWS):
                for col in range(INVENTORY_COLS):
                    slot_x = start_x + col * (SLOT_SIZE + SLOT_MARGIN)
                    slot_y = start_y + row * (SLOT_SIZE + SLOT_MARGIN)
                    
                    slot_rect = pygame.Rect(slot_x, slot_y, SLOT_SIZE, SLOT_SIZE)
                    if slot_rect.collidepoint(mouse_pos):
                        slot_index = row * INVENTORY_COLS + col
                        self.hovered_slot = slot_index
                        break
                if self.hovered_slot is not None:
                    break
    
    def draw(self, inventory):
        """Draw all UI elements"""
        # Always draw hotbar
        self.draw_hotbar(inventory)
        
        # Draw inventory if visible
        if self.inventory_visible:
            self.draw_inventory(inventory)
    
    def get_item_color(self, item_type):
        """Get color for an item type (fallback if no sprite)"""
        colors = {
            'resource': (200, 180, 60),
            'sword': (180, 180, 200),
            'shield': (100, 150, 200),
            'potion': (220, 80, 80),
            'key': (220, 220, 100)
        }
        return colors.get(item_type, (150, 150, 150))