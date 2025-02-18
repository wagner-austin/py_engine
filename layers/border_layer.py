"""
border_layer.py - Provides the border layer that draws a border around the screen.
Version: 1.1.1
"""

import pygame
from .base_layer import BaseLayer
from ui.layout_constants import BorderLayout, LayerZIndex
from core.config import Config
from plugins.plugins import register_layer

@register_layer("border", "foreground")
class BorderLayer(BaseLayer):
    def __init__(self, font: pygame.font.Font, config: Config) -> None:
        """
        Initializes the BorderLayer with the provided font and configuration.
        Marks the layer as persistent to ensure it is not dimmed during transitions.

        Parameters:
            font (pygame.font.Font): The font used for rendering (standardized, even if not used).
            config (Config): The configuration object.
        """
        self.font: pygame.font.Font = font
        self.config: Config = config
        self.z: int = LayerZIndex.BORDER
        self.border_color = self.config.theme.border_color
        self.persistent: bool = True

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        thickness: int = self.config.scale_value(BorderLayout.THICKNESS_FACTOR)
        pygame.draw.rect(
            screen,
            self.border_color,
            (0, 0, self.config.screen_width, self.config.screen_height),
            thickness,
        )