# [file name]: inventory.py (modified to fill hotbar first)
import pygame
from constants import *

class Inventory:
    def __init__(self):
        # Initialize all slots as empty
        self.slots = [None] * TOTAL_SLOTS
        self.hotbar = [None] * HOTBAR_SLOTS
        
        # Sync initial hotbar
        self.sync_hotbar()
    
    def add_item(self, item_type, count=1):
        """Add items to inventory - FILL HOTBAR FIRST, THEN GO UP"""
        remaining_count = count
        
        # PHASE 1: Try to stack with existing items of same type in HOTBAR FIRST
        bottom_row_start = (INVENTORY_ROWS - 1) * INVENTORY_COLS
        
        # Check hotbar slots first (bottom row, slots 1-9)
        for hotbar_slot in range(HOTBAR_SLOTS):
            inventory_slot = bottom_row_start + hotbar_slot
            if inventory_slot < len(self.slots):
                slot = self.slots[inventory_slot]
                if slot and slot['type'] == item_type:
                    # Stack in hotbar
                    slot['count'] += remaining_count
                    self.sync_hotbar()
                    return True
        
        # PHASE 2: Try to stack with existing items in other slots
        for i, slot in enumerate(self.slots):
            if slot and slot['type'] == item_type:
                slot['count'] += remaining_count
                self.sync_hotbar()
                return True
        
        # PHASE 3: Find empty slots, starting from HOTBAR, then going up
        # Check hotbar slots first (bottom row, left to right)
        for hotbar_slot in range(HOTBAR_SLOTS):
            inventory_slot = bottom_row_start + hotbar_slot
            if inventory_slot < len(self.slots) and not self.slots[inventory_slot]:
                # Found empty hotbar slot
                self.slots[inventory_slot] = {'type': item_type, 'count': remaining_count}
                self.sync_hotbar()
                return True
        
        # PHASE 4: Check remaining slots from bottom to top, left to right
        # Start from row above hotbar and go up
        for row in range(INVENTORY_ROWS - 2, -1, -1):  # From row 3 to 0 (0-indexed)
            for col in range(INVENTORY_COLS):
                slot_index = row * INVENTORY_COLS + col
                if not self.slots[slot_index]:
                    # Found empty slot
                    self.slots[slot_index] = {'type': item_type, 'count': remaining_count}
                    self.sync_hotbar()
                    return True
        
        # No empty slots
        return False
    
    def remove_item(self, slot_index, count=1):
        """Remove items from a specific slot"""
        if 0 <= slot_index < len(self.slots):
            slot = self.slots[slot_index]
            if slot and slot['count'] >= count:
                slot['count'] -= count
                if slot['count'] <= 0:
                    self.slots[slot_index] = None
                self.sync_hotbar()
                return True
        return False
    
    def get_hotbar_item(self, hotbar_index):
        """Get item in hotbar slot"""
        if 0 <= hotbar_index < len(self.hotbar):
            return self.hotbar[hotbar_index]
        return None
    
    def use_hotbar_item(self, hotbar_index):
        """Use/consume item in hotbar"""
        # Find which inventory slot corresponds to this hotbar slot
        bottom_row_start = (INVENTORY_ROWS - 1) * INVENTORY_COLS
        inventory_slot = bottom_row_start + hotbar_index
        
        if 0 <= inventory_slot < len(self.slots):
            return self.remove_item(inventory_slot, 1)
        return False
    
    def sync_hotbar(self):
        """Sync hotbar with bottom row of inventory"""
        bottom_row_start = (INVENTORY_ROWS - 1) * INVENTORY_COLS
        
        for i in range(HOTBAR_SLOTS):
            inventory_slot = bottom_row_start + i
            if inventory_slot < len(self.slots):
                self.hotbar[i] = self.slots[inventory_slot]
            else:
                self.hotbar[i] = None
    
    def get_item_count(self, item_type):
        """Get total count of a specific item type"""
        total = 0
        for slot in self.slots:
            if slot and slot['type'] == item_type:
                total += slot['count']
        return total
    
    def has_item(self, item_type, count=1):
        """Check if inventory has at least count of item_type"""
        return self.get_item_count(item_type) >= count
    
    def is_empty(self):
        """Check if inventory is completely empty"""
        for slot in self.slots:
            if slot:
                return False
        return True
    
    def get_total_items(self):
        """Get total number of items in inventory"""
        total = 0
        for slot in self.slots:
            if slot:
                total += slot['count']
        return total
    
    def get_slot_number_display(self, slot_index):
        """Get the display number for a slot (1-9 for hotbar, 10+ for others)"""
        if slot_index < 0 or slot_index >= len(self.slots):
            return ""
        
        # Calculate row and column
        row = slot_index // INVENTORY_COLS
        col = slot_index % INVENTORY_COLS
        
        # Bottom row (hotbar) is slots 1-9
        if row == INVENTORY_ROWS - 1:
            return str(col + 1)  # 1-9
        
        # For other rows, calculate number: 10, 11, 12, 13, 14, 15, 16, 17, 18 (row 3)
        # 19, 20, 21, 22, 23, 24, 25, 26, 27 (row 2)
        # 28, 29, 30, 31, 32, 33, 34, 35, 36 (row 1)
        # 37, 38, 39, 40, 41, 42, 43, 44, 45 (row 0)
        hotbar_slots = HOTBAR_SLOTS  # 9
        hotbar_row = INVENTORY_ROWS - 2  # Bottom row (row 4 in 5 rows)
        
        # Calculate number
        rows_above = hotbar_row - row
        slot_number = (rows_above * INVENTORY_COLS) + col + 1 + hotbar_slots
        
        return str(slot_number)