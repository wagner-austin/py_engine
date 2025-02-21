"""
config.py - Global configuration using a dataclass.
Version: 1.5.1
Summary: Updated with Theme selection, global input keys, a selected game mode attribute, and a flag to enable global control layers.
Note: The Theme dataclass and theme instances are defined in themes.py.
To change the active theme, update the ACTIVE_THEME variable in themes.py.
"""

from dataclasses import dataclass, field
from typing import Tuple
from themes.themes import ACTIVE_THEME, Theme  # Import ACTIVE_THEME from themes.py
from .controls import GLOBAL_INPUT_KEYS  # Import global keys from controls module

@dataclass
class Config:
    base_width: int = 800
    base_height: int = 600
    fps: int = 60
    base_font_size: int = 32
    scale: float = 1.0
    screen_width: int = 800
    screen_height: int = 600
    theme: Theme = field(default_factory=lambda: ACTIVE_THEME)
    global_input_keys: Tuple[int, int] = GLOBAL_INPUT_KEYS  # Use centralized keys
    selected_game_mode: str = "default"  # New attribute for the selected game mode
    enable_global_controls: bool = True  # New flag to enable global directional control layer

    def update_dimensions(self, width: int, height: int) -> None:
        """
        Updates the screen dimensions and recalculates the scale.
        Version: 1.5.1
        """
        self.screen_width = width
        self.screen_height = height
        self.scale = min(
            self.screen_width / self.base_width,
            self.screen_height / self.base_height
        )

    def scale_value(self, base_value: int) -> int:
        """
        Scales the provided base value using the current scale factor.
        Version: 1.5.1
        """
        return int(base_value * self.scale)