"""
art_layers.py - Provides art layers for universal background and foreground art.
Version: 1.1.1
"""

import pygame
import math
from typing import List
from assets.art_assets import STAR_ART, BACKGROUND_ART
from .base_layer import BaseLayer
from ui.layout_constants import ArtLayout, LayerZIndex, ArtColors
from core.config import Config
from plugins.plugins import register_layer

def stretch_line(line: str, font: pygame.font.Font, target_width: int) -> str:
    """
    Inserts extra spaces between characters to stretch the line horizontally.

    Parameters:
        line (str): The original string to stretch.
        font (pygame.font.Font): The pygame font used to measure text width.
        target_width (int): The desired width in pixels.

    Returns:
        str: The stretched string.
    """
    current_width: int = font.size(line)[0]
    if current_width >= target_width:
        return line
    gaps: int = len(line) - 1
    if gaps <= 0:
        return line
    space_width: int = font.size(" ")[0]
    extra_spaces: int = math.ceil((target_width - current_width) / (gaps * space_width))
    new_line: str = line[0]
    for char in line[1:]:
        new_line += " " * extra_spaces + char
    return new_line

@register_layer("star_art", "background")
class StarArtLayer(BaseLayer):
    """
    Layer for displaying star art in the background.
    """
    def __init__(self, font: pygame.font.Font, config: Config) -> None:
        """
        Initializes the StarArtLayer with the provided font and configuration.

        Parameters:
            font (pygame.font.Font): The pygame font used for rendering.
            config (Config): The configuration object containing screen dimensions and scale.
        """
        self.z: int = LayerZIndex.STAR_ART
        self.font: pygame.font.Font = font
        self.config: Config = config
        self.art: List[str] = STAR_ART
        self.line_height: int = self.font.get_height()
        self.persistent: bool = True  # Mark as persistent so it does not dim during transitions

    def update(self, dt: float) -> None:
        """
        Updates the layer. No dynamic behavior implemented.

        Parameters:
            dt (float): Delta time in seconds.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the star art onto the provided screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the star art.
        """
        top_margin: int = self.config.scale_value(ArtLayout.STAR_MARGIN_FACTOR)
        bottom_margin: int = self.config.scale_value(ArtLayout.STAR_MARGIN_FACTOR)
        available_height: int = self.config.screen_height - top_margin - bottom_margin
        num_lines: int = len(self.art)
        spacing: float = available_height / (num_lines - 1) if num_lines > 1 else available_height
        for i, line in enumerate(self.art):
            stretched_line: str = stretch_line(line, self.font, self.config.screen_width)
            y: float = top_margin + i * spacing
            text_surface: pygame.Surface = self.font.render(stretched_line, True, ArtColors.STAR_TEXT)
            text_rect: pygame.Rect = text_surface.get_rect(
                center=(self.config.screen_width // 2, int(y))
            )
            screen.blit(text_surface, text_rect)

#@register_layer:("background_art", "background")
class BackGroundArtLayer(BaseLayer):
    """
    Layer for displaying background art in the foreground.
    """
    def __init__(self, font: pygame.font.Font, config: Config) -> None:
        """
        Initializes the BackGroundArtLayer with the provided font and configuration.

        Parameters:
            font (pygame.font.Font): The pygame font used for rendering.
            config (Config): The configuration object containing screen dimensions and scale.
        """
        self.z: int = LayerZIndex.BACKGROUND_ART
        self.font: pygame.font.Font = font
        self.config: Config = config
        self.art: List[str] = BACKGROUND_ART
        self.line_height: int = self.font.get_height()
        self.persistent: bool = True  # Mark as persistent so it does not dim during transitions

    def update(self, dt: float) -> None:
        """
        Updates the layer. No dynamic behavior implemented.

        Parameters:
            dt (float): Delta time in seconds.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the background art onto the provided screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the background art.
        """
        y: int = int(self.config.screen_height * 0.5)  # Using 0.5 as a vertical factor, adjust as needed.
        for line in self.art:
            text_surface: pygame.Surface = self.font.render(line, True, ArtColors.BACKGROUND_TEXT)
            text_rect: pygame.Rect = text_surface.get_rect(
                center=(self.config.screen_width // 2, y)
            )
            screen.blit(text_surface, text_rect)
            y += self.line_height