"""
art_layers.py - Provides art layers for universal background and foreground art.
Includes a helper function to stretch ASCII art lines horizontally.

Version: 1.0
"""

import pygame
import math
from art_assets import STAR_ART, BACKGROUND_ART
from base_layer import BaseLayer
from layout_constants import ArtLayout, LayerZIndex

def stretch_line(line, font, target_width):
    """
    Inserts extra spaces between characters to stretch the line horizontally.

    Parameters:
        line: The original string to stretch.
        font: The pygame font used to measure text width.
        target_width: The desired width in pixels.

    Returns:
        The stretched string.
    """
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

class StarArtLayer(BaseLayer):
    """
    Layer for displaying star art in the background.
    """

    def __init__(self, font, config):
        """
        Initializes the StarArtLayer with the provided font and configuration.

        Parameters:
            font: The pygame font used for rendering.
            config: The configuration object containing screen dimensions and scale.
        """
        self.z = LayerZIndex.STAR_ART
        self.font = font
        self.config = config
        self.art = STAR_ART
        self.line_height = self.font.get_height()

    def update(self):
        """Updates the layer. No dynamic behavior implemented."""
        pass

    def draw(self, screen):
        """
        Draws the star art onto the provided screen.

        Parameters:
            screen: The pygame Surface on which to draw the star art.
        """
        top_margin = self.config.scale_value(ArtLayout.STAR_MARGIN_FACTOR)
        bottom_margin = self.config.scale_value(ArtLayout.STAR_MARGIN_FACTOR)
        available_height = self.config.screen_height - top_margin - bottom_margin
        num_lines = len(self.art)
        spacing = available_height / (num_lines - 1) if num_lines > 1 else available_height
        for i, line in enumerate(self.art):
            stretched_line = stretch_line(line, self.font, self.config.screen_width)
            y = top_margin + i * spacing
            text_surface = self.font.render(stretched_line, True, (150, 150, 150))
            text_rect = text_surface.get_rect(
                center=(self.config.screen_width // 2, int(y))
            )
            screen.blit(text_surface, text_rect)

class BackGroundArtLayer(BaseLayer):
    """
    Layer for displaying background art in the foreground.
    """

    def __init__(self, font, config):
        """
        Initializes the BackGroundArtLayer with the provided font and configuration.

        Parameters:
            font: The pygame font used for rendering.
            config: The configuration object containing screen dimensions and scale.
        """
        self.z = LayerZIndex.BACKGROUND_ART
        self.font = font
        self.config = config
        self.art = BACKGROUND_ART
        self.line_height = self.font.get_height()

    def update(self):
        """Updates the layer. No dynamic behavior implemented."""
        pass

    def draw(self, screen):
        """
        Draws the background art onto the provided screen.

        Parameters:
            screen: The pygame Surface on which to draw the background art.
        """
        y = int(self.config.screen_height * ArtLayout.BACKGROUND_VERTICAL_FACTOR)
        for line in self.art:
            text_surface = self.font.render(line, True, (100, 255, 100))
            text_rect = text_surface.get_rect(
                center=(self.config.screen_width // 2, y)
            )
            screen.blit(text_surface, text_rect)
            y += self.line_height