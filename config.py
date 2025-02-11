# FileName: config.py
# version: 1.4 (modified)
# Summary: Global configuration using a dataclass. Contains base resolution, FPS, font size, scale,
#          default screen dimensions, and universal theme settings. Provides a method to update screen dimensions.
# Tags: config, global, theme, scaling

from dataclasses import dataclass, field

@dataclass
class Config:
    base_width: int = 800
    base_height: int = 600
    fps: int = 60
    base_font_size: int = 32
    scale: float = 1.0
    screen_width: int = 800
    screen_height: int = 600
    theme: dict = field(default_factory=lambda: {
        "background_color": (0, 0, 0),             # Black background
        "title_color": (57, 255, 20),              # Neon green for title
        "button_normal_color": (200, 0, 200),      # Neon purple for buttons (unselected)
        "button_selected_color": (57, 255, 20),     # Neon green for selected buttons
        "highlight_color": (57, 255, 20),          # Neon green for highlight border
        "border_color": (57, 255, 20),             # Border color (neon green)
        "instruction_color": (255, 255, 255),      # White instructions text
        "font_color": (255, 255, 255)
    })

    def update_dimensions(self, width: int, height: int):
        """
        Updates the screen dimensions and recalculates the scale.
        """
        self.screen_width = width
        self.screen_height = height
        self.scale = min(self.screen_width / self.base_width, self.screen_height / self.base_height)

# Global configuration instance
config = Config()