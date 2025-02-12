# File: instruction_layer.py
# Version: 1.1 (modified)
# Summary: Provides the instruction layer that displays on-screen instructions.
# Tags: layers, instructions, UI, modular

import pygame
from base_layer import BaseLayer

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
                int(20 * self.config.scale),
                self.config.screen_height - int(40 * self.config.scale),
            ),
        )