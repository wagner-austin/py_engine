"""
effect_layers.py - Provides effect layers such as the rain effect and snow effect.
Version: 1.2.1
"""

import pygame
import random
from typing import Dict, List
from layers.base_layer import BaseLayer
from ui.layout_constants import LayerZIndex, EffectColors
from core.config import Config
from plugins.plugins import register_layer

@register_layer("rain_effect", "effect")
class RainEffectLayer(BaseLayer):
    def __init__(self, config: Config) -> None:
        """
        Initializes the RainEffectLayer with the provided configuration.

        Parameters:
            config (Config): The configuration object containing screen dimensions and scale.
        """
        self.z: int = LayerZIndex.RAIN_EFFECT
        self.config: Config = config
        self.lines: List[Dict[str, float]] = []
        self.num_lines: int = 50
        
        self.persistent = True  # Mark this layer as persistent to maintain state across scenes.
        for _ in range(self.num_lines):
            x: float = random.uniform(0, self.config.screen_width)
            y: float = random.uniform(0, self.config.screen_height)
            length: int = self.config.scale_value(10)
            self.lines.append({"x": x, "y": y, "length": length})

    def update(self, dt: float) -> None:
        """
        Updates the rain effect layer by moving each rain line.

        Parameters:
            dt (float): Delta time in seconds.
        """
        speed: int = self.config.scale_value(5)
        for line in self.lines:
            line["y"] += speed * dt
            if line["y"] > self.config.screen_height:
                line["y"] = -line["length"]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the rain effect onto the provided screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the rain effect.
        """
        color = EffectColors.RAIN_EFFECT
        for line in self.lines:
            start_pos = (int(line["x"]), int(line["y"]))
            end_pos = (int(line["x"]), int(line["y"] + line["length"]))
            pygame.draw.line(screen, color, start_pos, end_pos, 1)

@register_layer("snow_effect", "effect")
class SnowEffectLayer(BaseLayer):
    def __init__(self, config: Config) -> None:
        """
        Initializes the SnowEffectLayer with the provided configuration.

        Parameters:
            config (Config): The configuration object containing screen dimensions and scale.
        """
        self.z: int = LayerZIndex.RAIN_EFFECT  # Same z-index as rain effect; adjust if needed.
        self.config: Config = config
        self.num_snowflakes: int = 100  # Increased density: more snowflakes.
        self.snowflakes: List[Dict[str, any]] = []
        self.persistent = True  # Mark this layer as persistent to maintain state across scenes.
        for _ in range(self.num_snowflakes):
            snowflake = {
                "x": random.uniform(0, self.config.screen_width),
                "y": random.uniform(0, self.config.screen_height),
                "size": random.uniform(4, 8),  # Larger size range.
                "speed": random.uniform(20, 40),  # Increased speed range.
                "drift": random.uniform(-0.5, 0.5)  # Horizontal drift.
            }
            self.snowflakes.append(snowflake)

    def update(self, dt: float) -> None:
        """
        Updates the snow effect layer by moving each snowflake.
        Snowflakes gently fall with a slight horizontal drift.

        Parameters:
            dt (float): Delta time in seconds.
        """
        for flake in self.snowflakes:
            flake["y"] += flake["speed"] * dt
            flake["x"] += flake["drift"] * dt
            flake["drift"] += random.uniform(-0.05, 0.05) * dt
            flake["drift"] = max(min(flake["drift"], 1), -1)
            if flake["y"] > self.config.screen_height:
                flake["y"] = -flake["size"]
                flake["x"] = random.uniform(0, self.config.screen_width)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the snow effect onto the provided screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the snow effect.
        """
        snow_color = (255, 255, 255)
        for flake in self.snowflakes:
            x = int(flake["x"])
            y = int(flake["y"])
            size = int(flake["size"])
            pygame.draw.circle(screen, snow_color, (x, y), size)