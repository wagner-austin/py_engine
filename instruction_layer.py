# FileName: instruction_layer.py
# version: 1.0
# Summary: Provides the instruction layer that displays on-screen instructions.
# Tags: layers, instructions, UI, modular

import pygame
import config

class InstructionLayer:
    def __init__(self, font):
        self.z = 3
        self.font = font
        self.text = "Use W/S to navigate, Enter to select, Q/Esc to return."
        self.color = config.THEME["instruction_color"]

    def update(self):
        pass

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (int(20 * config.SCALE), config.SCREEN_HEIGHT - int(40 * config.SCALE)))