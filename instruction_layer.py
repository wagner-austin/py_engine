"""
instruction_layer.py - Provides the instruction layer that displays on-screen instructions.

Version: 1.2
"""

import pygame
from typing import Any
from base_layer import BaseLayer
from layout_constants import LayerZIndex
from config import Config

INSTRUCTION_LEFT_MARGIN_FACTOR: int = 20
INSTRUCTION_BOTTOM_MARGIN_FACTOR: int = 40

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
        self.color: Any = self.config.theme["instruction_color"]

    def update(self) -> None:
        """Updates the instruction layer. No dynamic behavior implemented."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the instruction text onto the provided screen.
        
        Parameters:
            screen: The pygame Surface on which to draw the instructions.
        """
        left_margin: int = self.config.scale_value(INSTRUCTION_LEFT_MARGIN_FACTOR)
        bottom_margin: int = self.config.scale_value(INSTRUCTION_BOTTOM_MARGIN_FACTOR)
        text_surface: pygame.Surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (left_margin, self.config.screen_height - bottom_margin))