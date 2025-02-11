# FileName: border_layer.py
# version: 1.1
# Summary: Provides the border layer that draws a border around the screen. The border is drawn fully inside
#          the screen bounds so that no edge is clipped.
# Tags: layers, border, UI, modular

import pygame
import config

class BorderLayer:
    def __init__(self):
        self.z = 5
        self.border_color = config.THEME["border_color"]
        self.thickness = int(4 * config.SCALE)
    
    def update(self):
        pass
    
    def draw(self, screen):
        # Draw the border inside the screen bounds using the full screen dimensions.
        pygame.draw.rect(screen, self.border_color,
                         (0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT), self.thickness)