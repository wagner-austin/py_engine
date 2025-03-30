"""
core/config.py - Global configuration using a dataclass.
--------------------------------------------------------------------------------
Version: 1.5.1
Summary: Updated for mouse/touch-only input. Removed global keyboard input keys.
"""

from dataclasses import dataclass, field
from themes.themes import ACTIVE_THEME, Theme  # Import ACTIVE_THEME from themes.py

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
    selected_game_mode: str = "default"  # New attribute for the selected game mode
    enable_global_controls: bool = True  # Flag to enable global control layers (for mouse/touch)

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

# End of core/config.py