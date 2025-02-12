"""
config.py - Global configuration using a dataclass.

Version: 1.5 (updated with Theme dataclass and global input keys)
"""

import pygame
from dataclasses import dataclass, field
from typing import Tuple

@dataclass
class Theme:
    background_color: Tuple[int, int, int] = (0, 0, 0)             # Black background
    title_color: Tuple[int, int, int] = (57, 255, 20)                # Neon green for title
    button_normal_color: Tuple[int, int, int] = (200, 0, 200)        # Neon purple for buttons (unselected)
    button_selected_color: Tuple[int, int, int] = (57, 255, 20)      # Neon green for selected buttons
    highlight_color: Tuple[int, int, int] = (57, 255, 20)            # Neon green for highlight border
    border_color: Tuple[int, int, int] = (57, 255, 20)               # Border color (neon green)
    instruction_color: Tuple[int, int, int] = (255, 255, 255)        # White instructions text
    font_color: Tuple[int, int, int] = (255, 255, 255)               # White font color

@dataclass
class Config:
    base_width: int = 800
    base_height: int = 600
    fps: int = 60
    base_font_size: int = 32
    scale: float = 1.0
    screen_width: int = 800
    screen_height: int = 600
    theme: Theme = field(default_factory=Theme)
    global_input_keys: Tuple[int, int] = (pygame.K_ESCAPE, pygame.K_q)  # Configurable global input keys

    def update_dimensions(self, width: int, height: int) -> None:
        """Updates the screen dimensions and recalculates the scale.

        Parameters:
            width: The new width of the screen.
            height: The new height of the screen.
        """
        self.screen_width = width
        self.screen_height = height
        self.scale = min(
            self.screen_width / self.base_width,
            self.screen_height / self.base_height
        )

    def scale_value(self, base_value: int) -> int:
        """Scales the provided base value using the current scale factor.

        Parameters:
            base_value: The base value to scale.

        Returns:
            The scaled integer value.
        """
        return int(base_value * self.scale)