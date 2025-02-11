# FileName: effect_layers.py
# version: 1.0
# Summary: Provides effect layers such as the rain effect.
# Tags: layers, effects, rain, modular

import pygame
import random
import config

class RainEffectLayer:
    def __init__(self):
        self.z = 1
        self.lines = []
        self.num_lines = 50
        self.speed = int(5 * config.SCALE)
        for _ in range(self.num_lines):
            x = random.uniform(0, config.SCREEN_WIDTH)
            y = random.uniform(0, config.SCREEN_HEIGHT)
            length = int(10 * config.SCALE)
            self.lines.append({"x": x, "y": y, "length": length})
    
    def update(self):
        for line in self.lines:
            line["y"] += self.speed
            if line["y"] > config.SCREEN_HEIGHT:
                line["y"] = -line["length"]
    
    def draw(self, screen):
        color = (100, 100, 255)
        for line in self.lines:
            start_pos = (int(line["x"]), int(line["y"]))
            end_pos = (int(line["x"]), int(line["y"] + line["length"]))
            pygame.draw.line(screen, color, start_pos, end_pos, 1)