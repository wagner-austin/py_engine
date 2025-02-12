"""
border_layer.py - Provides the border layer that draws a border around the screen.

Version: 1.0
"""

import pygame
from base_layer import BaseLayer
from layout_constants import BorderLayout, LayerZIndex

class BorderLayer(BaseLayer):
    """
    Layer that draws a border around the screen.
    """

    def __init__(self, config):
        """
        Initializes the BorderLayer with the provided configuration.

        Parameters:
            config: The configuration object containing theme, screen dimensions, and scale.
        """
        self.z = LayerZIndex.BORDER
        self.config = config
        self.border_color = self.config.theme["border_color"]

    def update(self):
        """Updates the border layer. No dynamic behavior implemented."""
        pass

    def draw(self, screen):
        """
        Draws the border onto the provided screen.

        Parameters:
            screen: The pygame Surface on which to draw the border.
        """
        thickness = self.config.scale_value(BorderLayout.THICKNESS_FACTOR)
        pygame.draw.rect(
            screen,
            self.border_color,
            (0, 0, self.config.screen_width, self.config.screen_height),
            thickness,
        )