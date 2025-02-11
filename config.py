# FileName: config.py
# version: 1.4
# Summary: Global configuration including base resolution, FPS, font size, scale, default screen dimensions,
#          and universal theme settings. Provides a function to update screen dimensions and scale.
# Tags: config, global, theme, scaling

BASE_WIDTH = 800
BASE_HEIGHT = 600
FPS = 60
BASE_FONT_SIZE = 32

# Default values—these will be updated at runtime.
SCALE = 1.0
SCREEN_WIDTH = BASE_WIDTH
SCREEN_HEIGHT = BASE_HEIGHT

THEME = {
    "background_color": (0, 0, 0),             # Black background
    "title_color": (57, 255, 20),              # Neon green for title
    "button_normal_color": (200, 0, 200),      # Neon purple for buttons (unselected)
    "button_selected_color": (57, 255, 20),     # Neon green for selected buttons
    "highlight_color": (57, 255, 20),          # Neon green for highlight border
    "border_color": (57, 255, 20),             # Border color (neon green)
    "instruction_color": (255, 255, 255),      # White instructions text
    "font_color": (255, 255, 255)
}

def update_dimensions(width, height):
    """
    Updates the global screen dimensions and scale based on the new width and height.
    This centralizes all calculations so that any module importing config will have the correct values.
    """
    global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE
    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height
    SCALE = min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT)