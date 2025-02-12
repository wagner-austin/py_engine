"""
effect_layers.py - Provides effect layers such as the rain effect.

Version: 1.1 (updated with centralized color constants)
"""

import pygame
import random
from typing import Dict, List
from .base_layer import BaseLayer
from layout_constants import LayerZIndex, EffectColors
from config import Config
from plugins import register_effect

@register_effect("rain_effect")
class RainEffectLayer(BaseLayer):
    def __init__(self, config: Config) -> None:
        """
        Initializes the RainEffectLayer with the provided configuration.
        
        Parameters:
            config: The configuration object containing screen dimensions and scale.
        """
        self.z: int = LayerZIndex.RAIN_EFFECT
        self.config: Config = config
        self.lines: List[Dict[str, float]] = []
        self.num_lines: int = 50
        for _ in range(self.num_lines):
            x: float = random.uniform(0, self.config.screen_width)
            y: float = random.uniform(0, self.config.screen_height)
            length: int = self.config.scale_value(10)
            self.lines.append({"x": x, "y": y, "length": length})

    def update(self) -> None:
        """
        Updates the rain effect layer by moving each rain line.
        Recalculates the speed dynamically based on the current scale.
        """
        speed: int = self.config.scale_value(5)
        for line in self.lines:
            line["y"] += speed
            if line["y"] > self.config.screen_height:
                line["y"] = -line["length"]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the rain effect onto the provided screen.
        
        Parameters:
            screen: The pygame Surface on which to draw the rain effect.
        """
        color = EffectColors.RAIN_EFFECT
        for line in self.lines:
            start_pos = (int(line["x"]), int(line["y"]))
            end_pos = (int(line["x"]), int(line["y"] + line["length"]))
            pygame.draw.line(screen, color, start_pos, end_pos, 1)