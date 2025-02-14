"""
themes.py - Contains multiple theme definitions for the application using plugin registration.

To add a new theme, define it below with the @register_theme decorator and then
enable it by commenting/uncommenting the appropriate ACTIVE_THEME assignment.
"""

from dataclasses import dataclass
from typing import Tuple
from plugins.plugins import register_theme, theme_registry

@dataclass
class Theme:
    background_color: Tuple[int, int, int]
    title_color: Tuple[int, int, int]
    button_normal_color: Tuple[int, int, int]
    button_selected_color: Tuple[int, int, int]
    highlight_color: Tuple[int, int, int]
    border_color: Tuple[int, int, int]
    instruction_color: Tuple[int, int, int]
    font_color: Tuple[int, int, int]
    particle_color_palette: Tuple[Tuple[int, int, int], ...]  # New field for particle effect colors

@register_theme('default')
def default_theme() -> Theme:
    return Theme(
        background_color=(0, 0, 0),             # Black background
        title_color=(57, 255, 20),              # Neon green for title
        button_normal_color=(200, 0, 200),      # Neon purple for buttons (unselected)
        button_selected_color=(57, 255, 20),    # Neon green for selected buttons
        highlight_color=(57, 255, 20),          # Neon green for highlight border
        border_color=(57, 255, 20),             # Border color (neon green)
        instruction_color=(255, 255, 255),      # White instructions text
        font_color=(255, 255, 255),             # White font color
        particle_color_palette=((200, 150, 255), (150, 200, 255))
    )

@register_theme('light')
def light_theme() -> Theme:
    return Theme(
        background_color=(245, 245, 245),       # Off-white background
        title_color=(50, 50, 50),               # Dark gray for title
        button_normal_color=(200, 200, 200),    # Light gray for buttons (unselected)
        button_selected_color=(70, 70, 70),     # Darker gray for selected buttons
        highlight_color=(70, 70, 70),           # Darker gray for highlight border
        border_color=(150, 150, 150),           # Gray border
        instruction_color=(50, 50, 50),         # Dark gray instructions text
        font_color=(50, 50, 50),                # Dark gray font color
        particle_color_palette=((180, 180, 180), (160, 160, 160))
    )

@register_theme('retro80')
def retro80_theme() -> Theme:
    return Theme(
        background_color=(0, 0, 0),          # Dark bluish background
        title_color=(255, 20, 147),             # Hot pink for title
        button_normal_color=(75, 0, 130),       # Indigo for buttons (unselected)
        button_selected_color=(0, 255, 127),    # Neon green for selected buttons
        highlight_color=(0, 255, 255),          # Electric blue for highlight border
        border_color=(255, 105, 180),           # Pinkish border
        instruction_color=(255, 255, 255),      # White instructions text
        font_color=(255, 255, 255),             # White font color
        particle_color_palette=((255, 105, 180), (0, 255, 127))
    )

@register_theme('pastel')
def pastel_theme() -> Theme:
    return Theme(
        background_color=(255, 250, 240),       # Floral white background
        title_color=(135, 206, 250),            # Light sky blue for title
        button_normal_color=(152, 251, 152),    # Pale green for buttons (unselected)
        button_selected_color=(255, 182, 193),  # Light pink for selected buttons
        highlight_color=(221, 160, 221),        # Plum for highlight border
        border_color=(216, 191, 216),           # Thistle border
        instruction_color=(105, 105, 105),      # Dim gray instructions text
        font_color=(47, 79, 79),                # Dark slate gray font color
        particle_color_palette=((255, 182, 193), (152, 251, 152))
    )

@register_theme('halloween')
def halloween_theme() -> Theme:
    return Theme(
        background_color=(20, 20, 20),          # Very dark background
        title_color=(255, 140, 0),              # Dark orange for title
        button_normal_color=(139, 69, 19),      # Saddle brown for buttons (unselected)
        button_selected_color=(255, 69, 0),     # Orange red for selected buttons
        highlight_color=(255, 140, 0),          # Dark orange for highlight border
        border_color=(255, 140, 0),             # Dark orange border
        instruction_color=(255, 255, 255),      # White instructions text
        font_color=(255, 255, 255),             # White font color
        particle_color_palette=((255, 140, 0), (128, 0, 128))
    )

@register_theme('christmas')
def christmas_theme() -> Theme:
    return Theme(
        background_color=(0, 128, 0),           # Dark green background
        title_color=(255, 0, 0),                # Red for title
        button_normal_color=(34, 139, 34),      # Forest green for buttons (unselected)
        button_selected_color=(255, 0, 0),      # Red for selected buttons
        highlight_color=(255, 215, 0),          # Gold for highlight border
        border_color=(255, 0, 0),               # Red border
        instruction_color=(255, 255, 255),      # White instructions text
        font_color=(255, 255, 255),             # White font color
        particle_color_palette=((255, 0, 0), (0, 255, 0))
    )

@register_theme('starwars')
def starwars_theme() -> Theme:
    return Theme(
        background_color=(0, 0, 0),             # Black background
        title_color=(192, 192, 192),            # Silver for title
        button_normal_color=(64, 64, 64),       # Dark gray for buttons (unselected)
        button_selected_color=(192, 192, 192),  # Silver for selected buttons
        highlight_color=(0, 191, 255),          # Deep sky blue for highlight border
        border_color=(192, 192, 192),           # Silver border
        instruction_color=(192, 192, 192),      # Silver instructions text
        font_color=(192, 192, 192),             # Silver font color
        particle_color_palette=((192, 192, 192), (0, 191, 255))
    )

# -----------------------------------------------------------------------------
# Set the active theme.
# To change the active theme, simply comment/uncomment one of the assignments below.
# No need to touch any other file!

# ACTIVE_THEME = theme_registry.get('default')
# ACTIVE_THEME = theme_registry.get('light')
#ACTIVE_THEME = theme_registry.get('retro80')
#ACTIVE_THEME = theme_registry.get('pastel')
#ACTIVE_THEME = theme_registry.get('halloween')
#ACTIVE_THEME = theme_registry.get('christmas')
ACTIVE_THEME = theme_registry.get('starwars')

# Default to the 'default' theme if none is selected.

if ACTIVE_THEME is None:
    ACTIVE_THEME = theme_registry.get('default')