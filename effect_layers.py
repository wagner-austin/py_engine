# FileName: effect_layers.py
# version: 1.0 (modified)
# Summary: Provides effect layers such as the rain effect.
# Tags: layers, effects, rain, modular

import pygame
import random
import config  # Now using config.config

class RainEffectLayer:
    def __init__(self):
        self.z = 1
        self.lines = []
        self.num_lines = 50
        # Removed static speed calculation.
        for _ in range(self.num_lines):
            x = random.uniform(0, config.config.screen_width)
            y = random.uniform(0, config.config.screen_height)
            length = int(10 * config.config.scale)
            self.lines.append({"x": x, "y": y, "length": length})
    
    def update(self):
        # Dynamically recalc speed based on current scale.
        speed = int(5 * config.config.scale)
        for line in self.lines:
            line["y"] += speed
            if line["y"] > config.config.screen_height:
                line["y"] = -line["length"]
    
    def draw(self, screen):
        color = (100, 100, 255)
        for line in self.lines:
            start_pos = (int(line["x"]), int(line["y"]))
            end_pos = (int(line["x"]), int(line["y"] + line["length"]))
            pygame.draw.line(screen, color, start_pos, end_pos, 1)