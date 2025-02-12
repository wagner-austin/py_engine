"""
instruction_layer.py - Provides the instruction layer that displays on-screen instructions.

Version: 1.2
"""

import pygame
from base_layer import BaseLayer
from layout_constants import LayerZIndex

# Layout Constants
INSTRUCTION_LEFT_MARGIN_FACTOR = 20
INSTRUCTION_BOTTOM_MARGIN_FACTOR = 40

class InstructionLayer(BaseLayer):
    def __init__(self, font, config):
        """
        Initializes the InstructionLayer with the provided font and configuration.
        
        Parameters:
            font: The pygame font used for rendering text.
            config: The configuration object containing theme and scaling information.
        """
        self.z = LayerZIndex.INSTRUCTIONS
        self.font = font
        self.config = config
        self.text = "Use W/S to navigate, Enter to select, Q/Esc to return."
        self.color = self.config.theme["instruction_color"]

    def update(self):
        """Updates the instruction layer. No dynamic behavior implemented."""
        pass

    def draw(self, screen):
        """
        Draws the instruction text onto the provided screen.
        
        Parameters:
            screen: The pygame Surface on which to draw the instructions.
        """
        left_margin = self.config.scale_value(INSTRUCTION_LEFT_MARGIN_FACTOR)
        bottom_margin = self.config.scale_value(INSTRUCTION_BOTTOM_MARGIN_FACTOR)
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(
            text_surface,
            (left_margin, self.config.screen_height - bottom_margin),
        )