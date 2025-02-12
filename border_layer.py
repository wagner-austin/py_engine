# File: border_layer.py
# Version: 1.2 (modified)
# Summary: Provides the border layer that draws a border around the screen. The border is drawn fully inside
#          the screen bounds so that no edge is clipped.
# Tags: layers, border, UI, modular

import pygame
from base_layer import BaseLayer

class BorderLayer(BaseLayer):
    def __init__(self, config):
        self.z = 5
        self.config = config
        self.border_color = self.config.theme["border_color"]

    def update(self):
        pass

    def draw(self, screen):
        # Dynamically compute thickness based on current scale.
        thickness = int(4 * self.config.scale)
        pygame.draw.rect(
            screen,
            self.border_color,
            (0, 0, self.config.screen_width, self.config.screen_height),
            thickness,
        )