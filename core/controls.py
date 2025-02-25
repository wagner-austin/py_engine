"""
core/controls.py - Defines global input keys and menu navigation keys.
Version: 1.0.0
"""

import pygame

# Global keys that trigger global input handling
# Removed pygame.K_q so that the Q key (mapped to "B") is handled by individual scenes.
GLOBAL_INPUT_KEYS = (pygame.K_ESCAPE,)

# Menu navigation keys
MENU_NAVIGATION = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "select": (pygame.K_RETURN, pygame.K_SPACE)
}