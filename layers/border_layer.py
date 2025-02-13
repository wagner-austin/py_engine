"""
border_layer.py - Provides the border layer that draws a border around the screen.
Version: 1.0
"""

import pygame
from typing import Any
from .base_layer import BaseLayer
from layout_constants import BorderLayout, LayerZIndex
from config import Config
from plugins import register_universal_layer  # New import for universal layer registration

@register_universal_layer("border", "foreground")
class BorderLayer(BaseLayer):
    """
    Layer that draws a border around the screen.
    """

    def __init__(self, config: Config) -> None:
        """
        Initializes the BorderLayer with the provided configuration.
        """
        self.z: int = LayerZIndex.BORDER
        self.config: Config = config
        self.border_color = self.config.theme.border_color

    def update(self, dt: float) -> None:
        """Updates the border layer. No dynamic behavior implemented."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the border onto the provided screen.
        """
        thickness: int = self.config.scale_value(BorderLayout.THICKNESS_FACTOR)
        pygame.draw.rect(
            screen,
            self.border_color,
            (0, 0, self.config.screen_width, self.config.screen_height),
            thickness,
        )