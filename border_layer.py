# FileName: border_layer.py
# version: 1.1 (modified)
# Summary: Provides the border layer that draws a border around the screen. The border is drawn fully inside
#          the screen bounds so that no edge is clipped.
# Tags: layers, border, UI, modular

import pygame
import config  # Now using config.config

class BorderLayer:
    def __init__(self):
        self.z = 5
        self.border_color = config.config.theme["border_color"]
        # Deprecated: Static thickness calculation removed.
        # self.thickness = int(4 * config.config.scale)

    def update(self):
        pass

    def draw(self, screen):
        # Dynamically compute thickness based on current scale.
        thickness = int(4 * config.config.scale)
        pygame.draw.rect(screen, self.border_color,
                         (0, 0, config.config.screen_width, config.config.screen_height), thickness)