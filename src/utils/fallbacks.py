import pygame
from constants import *

def create_fallback_sprite(color, size=48):
    """Create a simple fallback sprite"""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (size//2, size//2), size//2)
    pygame.draw.circle(surf, (0, 0, 0, 160), (size//2, size//2), size//2, 2)
    pygame.draw.circle(surf, (255, 255, 255), (size//2 - 8, size//2 - 6), 4)
    pygame.draw.circle(surf, (255, 255, 255), (size//2 + 8, size//2 - 6), 4)
    return surf