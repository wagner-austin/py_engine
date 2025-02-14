"""
border_layer.py - Provides the border layer that draws a border around the screen.
Version: 1.1.0
"""

import pygame
from .base_layer import BaseLayer
from ui.layout_constants import BorderLayout, LayerZIndex
from core.config import Config
from plugins.plugins import register_layer

@register_layer("border", "foreground")
class BorderLayer(BaseLayer):
    """
    Layer that draws a border around the screen.
    """
    def __init__(self, config: Config) -> None:
        """
        Initializes the BorderLayer with the provided configuration.
        Marks the layer as persistent to ensure it is not dimmed during transitions.

        Parameters:
            config (Config): The configuration object.
        """
        self.z: int = LayerZIndex.BORDER
        self.config: Config = config
        self.border_color = self.config.theme.border_color
        self.persistent: bool = True  # Mark as persistent so it's not affected by the fade transition

    def update(self, dt: float) -> None:
        """
        Updates the border layer. No dynamic behavior implemented.
        
        Parameters:
            dt (float): Delta time in seconds.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the border onto the provided screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the border.
        """
        thickness: int = self.config.scale_value(BorderLayout.THICKNESS_FACTOR)
        pygame.draw.rect(
            screen,
            self.border_color,
            (0, 0, self.config.screen_width, self.config.screen_height),
            thickness,
        )