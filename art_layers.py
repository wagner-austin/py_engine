# FileName: art_layers.py
# version: 1.0 (modified)
# Summary: Provides art layers for universal background and foreground art.
#          Includes a helper function to stretch ASCII art lines horizontally.
# Tags: layers, art, ascii, modular

import pygame
import math
import config
from art_assets import STAR_ART, BACKGROUND_ART

def stretch_line(line, font, target_width):
    """Inserts extra spaces between characters to stretch the line horizontally."""
    current_width = font.size(line)[0]
    if current_width >= target_width:
        return line
    gaps = len(line) - 1
    if gaps <= 0:
        return line
    space_width = font.size(" ")[0]
    extra_spaces = math.ceil((target_width - current_width) / (gaps * space_width))
    new_line = line[0]
    for char in line[1:]:
        new_line += " " * extra_spaces + char
    return new_line

class StarArtLayer:
    def __init__(self, font):
        self.z = 0
        self.font = font
        self.art = STAR_ART
        self.line_height = self.font.get_height()

    def update(self):
        pass

    def draw(self, screen):
        # Stretch horizontally using stretch_line and distribute vertically
        top_margin = int(20 * config.config.scale)
        bottom_margin = int(20 * config.config.scale)
        available_height = config.config.screen_height - top_margin - bottom_margin
        num_lines = len(self.art)
        spacing = available_height / (num_lines - 1) if num_lines > 1 else available_height
        for i, line in enumerate(self.art):
            stretched_line = stretch_line(line, self.font, config.config.screen_width)
            y = top_margin + i * spacing
            text_surface = self.font.render(stretched_line, True, (150, 150, 150))
            text_rect = text_surface.get_rect(center=(config.config.screen_width // 2, int(y)))
            screen.blit(text_surface, text_rect)

class BackGroundArtLayer:
    def __init__(self, font):
        self.z = 2
        self.font = font
        self.art = BACKGROUND_ART
        self.line_height = self.font.get_height()

    def update(self):
        pass

    def draw(self, screen):
        # Draw background art centered horizontally in the lower half of the screen.
        y = int(config.config.screen_height * 0.5)
        for line in self.art:
            text_surface = self.font.render(line, True, (100, 255, 100))
            text_rect = text_surface.get_rect(center=(config.config.screen_width // 2, y))
            screen.blit(text_surface, text_rect)
            y += self.line_height