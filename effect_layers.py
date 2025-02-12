"""
effect_layers.py - Provides effect layers such as the rain effect.

Version: 1.1
"""

import pygame
import random
from base_layer import BaseLayer
from layout_constants import LayerZIndex

class RainEffectLayer(BaseLayer):
    def __init__(self, config):
        """
        Initializes the RainEffectLayer with the provided configuration.
        
        Parameters:
            config: The configuration object containing screen dimensions and scale.
        """
        self.z = LayerZIndex.RAIN_EFFECT
        self.config = config
        self.lines = []
        self.num_lines = 50
        # Removed static speed calculation.
        for _ in range(self.num_lines):
            x = random.uniform(0, self.config.screen_width)
            y = random.uniform(0, self.config.screen_height)
            length = self.config.scale_value(10)
            self.lines.append({"x": x, "y": y, "length": length})

    def update(self):
        """
        Updates the rain effect layer by moving each rain line.
        Recalculates the speed dynamically based on the current scale.
        """
        speed = self.config.scale_value(5)
        for line in self.lines:
            line["y"] += speed
            if line["y"] > self.config.screen_height:
                line["y"] = -line["length"]

    def draw(self, screen):
        """
        Draws the rain effect onto the provided screen.
        
        Parameters:
            screen: The pygame Surface on which to draw the rain effect.
        """
        color = (100, 100, 255)
        for line in self.lines:
            start_pos = (int(line["x"]), int(line["y"]))
            end_pos = (int(line["x"]), int(line["y"] + line["length"]))
            pygame.draw.line(screen, color, start_pos, end_pos, 1)