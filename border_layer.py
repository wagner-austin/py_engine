"""
border_layer.py - Provides the border layer that draws a border around the screen.

Version: 1.0
"""

import pygame
from typing import Any
from base_layer import BaseLayer
from layout_constants import BorderLayout, LayerZIndex
from config import Config

class BorderLayer(BaseLayer):
    """
    Layer that draws a border around the screen.
    """

    def __init__(self, config: Config) -> None:
        """
        Initializes the BorderLayer with the provided configuration.

        Parameters:
            config: The configuration object containing theme, screen dimensions, and scale.
        """
        self.z: int = LayerZIndex.BORDER
        self.config: Config = config
        self.border_color: Any = self.config.theme["border_color"]

    def update(self) -> None:
        """Updates the border layer. No dynamic behavior implemented."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the border onto the provided screen.

        Parameters:
            screen: The pygame Surface on which to draw the border.
        """
        thickness: int = self.config.scale_value(BorderLayout.THICKNESS_FACTOR)
        pygame.draw.rect(
            screen,
            self.border_color,
            (0, 0, self.config.screen_width, self.config.screen_height),
            thickness,
        )