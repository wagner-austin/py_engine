# File: instruction_layer.py
# Version: 1.2 (modified)
# Summary: Provides the instruction layer that displays on-screen instructions.
# Tags: layers, instructions, UI, modular

import pygame
from base_layer import BaseLayer

# Layout Constants
INSTRUCTION_LEFT_MARGIN_FACTOR = 20
INSTRUCTION_BOTTOM_MARGIN_FACTOR = 40

class InstructionLayer(BaseLayer):
    def __init__(self, font, config):
        self.z = 3
        self.font = font
        self.config = config
        self.text = "Use W/S to navigate, Enter to select, Q/Esc to return."
        self.color = self.config.theme["instruction_color"]

    def update(self):
        pass

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(
            text_surface,
            (
                int(INSTRUCTION_LEFT_MARGIN_FACTOR * self.config.scale),
                self.config.screen_height - int(INSTRUCTION_BOTTOM_MARGIN_FACTOR * self.config.scale),
            ),
        )