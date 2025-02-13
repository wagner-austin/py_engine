"""
instruction_layer.py - Provides the instruction layer that displays on-screen instructions.
Version: 1.2 (updated)
"""

import pygame
from typing import Any
from .base_layer import BaseLayer
from layout_constants import LayerZIndex, InstructionLayout
from config import Config
from plugins import register_universal_layer  # New import for universal layer registration

@register_universal_layer("instruction", "foreground")
class InstructionLayer(BaseLayer):
    def __init__(self, font: pygame.font.Font, config: Config) -> None:
        """
        Initializes the InstructionLayer with the provided font and configuration.
        
        Parameters:
            font: The pygame font used for rendering text.
            config: The configuration object containing theme and scaling information.
        """
        self.z: int = LayerZIndex.INSTRUCTIONS
        self.font: pygame.font.Font = font
        self.config: Config = config
        self.text: str = "Use W/S to navigate, Enter to select, Q/Esc to return."
        self.color: Any = self.config.theme.instruction_color

    def update(self, dt: float) -> None:
        """Updates the instruction layer. No dynamic behavior implemented."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the instruction text onto the provided screen.
        
        Parameters:
            screen: The pygame Surface on which to draw the instructions.
        """
        left_margin: int = self.config.scale_value(InstructionLayout.LEFT_MARGIN_PX)
        bottom_margin: int = self.config.scale_value(InstructionLayout.BOTTOM_MARGIN_PX)
        text_surface: pygame.Surface = self.font.render(self.text, True, self.config.theme.instruction_color)
        screen.blit(text_surface, (left_margin, self.config.screen_height - bottom_margin))