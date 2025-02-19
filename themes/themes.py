"""
themes/themes.py
----------------
Contains multiple theme definitions for the application using plugin registration, 
and provides a dynamic blending system so that new or changed fields in Theme 
do not require modifications outside this file.
Version: 1.5.1 (added rain_color and snow_color)
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
    particle_color_palette: Tuple[Tuple[int, int, int], ...]

    # New fields for star and background art text
    star_text_color: Tuple[int, int, int]
    background_text_color: Tuple[int, int, int]

    # Added fields for effects:
    rain_color: Tuple[int, int, int]
    snow_color: Tuple[int, int, int]


def interpolate_color(color1: Tuple[int, int, int],
                      color2: Tuple[int, int, int],
                      t: float) -> Tuple[int, int, int]:
    """
    Interpolates between two RGB colors based on t (0.0 to 1.0).
    """
    return (
        int(color1[0] + (color2[0] - color1[0]) * t),
        int(color1[1] + (color2[1] - color1[1]) * t),
        int(color1[2] + (color2[2] - color1[2]) * t),
    )


def blend_themes(old_theme: 'Theme', new_theme: 'Theme', t: float) -> 'Theme':
    """
    Dynamically blends two Theme instances by examining all dataclass fields.
    - If a field is a 3-int tuple, it is treated as an RGB color and interpolated.
    - If a field is a tuple of 3-int tuples, it is treated as a color palette and blended element-wise.
    - Otherwise, if t < 1.0, the old_theme's value is used; if t >= 1.0, the new_theme's value is used.

    This allows adding new fields to the Theme dataclass without modifying code outside this file.
    """
    new_field_values = {}
    for field_name in old_theme.__dataclass_fields__:
        old_val = getattr(old_theme, field_name)
        new_val = getattr(new_theme, field_name)

        # Check if it's a single color: (r, g, b)
        if (
            isinstance(old_val, tuple)
            and len(old_val) == 3
            and all(isinstance(x, int) for x in old_val)
            and isinstance(new_val, tuple)
            and len(new_val) == 3
            and all(isinstance(x, int) for x in new_val)
        ):
            # Interpolate as a color
            new_field_values[field_name] = interpolate_color(old_val, new_val, t)

        # Check if it's a palette of multiple colors
        elif (
            isinstance(old_val, tuple)
            and len(old_val) > 0
            and all(isinstance(x, tuple) and len(x) == 3 for x in old_val)
            and isinstance(new_val, tuple)
            and len(new_val) > 0
            and all(isinstance(x, tuple) and len(x) == 3 for x in new_val)
        ):
            # If the palettes have the same length, blend them element-wise
            if len(old_val) == len(new_val):
                new_field_values[field_name] = tuple(
                    interpolate_color(c1, c2, t)
                    for c1, c2 in zip(old_val, new_val)
                )
            else:
                # If lengths differ, just switch to new_val by the end of blending
                if t < 1.0:
                    new_field_values[field_name] = old_val
                else:
                    new_field_values[field_name] = new_val

        else:
            # For any non-color field or other data, smoothly transition from old to new at t=1
            if t < 1.0:
                new_field_values[field_name] = old_val
            else:
                new_field_values[field_name] = new_val

    return Theme(**new_field_values)


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
        particle_color_palette=((200, 150, 255), (150, 200, 255)),
        star_text_color=(255, 255, 255),        # default star text color
        background_text_color=(57, 255, 20),    # default background art color

        # Effects
        rain_color=(0, 120, 255),
        snow_color=(255, 255, 255),
    )


@register_theme('light')
def light_theme() -> Theme:
    return Theme(
        background_color=(245, 245, 245),       # Off-white background
        title_color=(50, 50, 50),               # Dark gray for title
        button_normal_color=(200, 200, 200),    # Light gray for buttons
        button_selected_color=(70, 70, 70),     # Darker gray for selected buttons
        highlight_color=(70, 70, 70),           # Darker gray highlight border
        border_color=(150, 150, 150),           # Gray border
        instruction_color=(50, 50, 50),         # Dark gray instructions text
        font_color=(50, 50, 50),                # Dark gray font color
        particle_color_palette=((180, 180, 180), (160, 160, 160)),
        star_text_color=(50, 50, 50),           # star text color
        background_text_color=(90, 90, 90),     # background art color

        # Effects
        rain_color=(100, 100, 255),
        snow_color=(220, 220, 220),
    )


@register_theme('retro80')
def retro80_theme() -> Theme:
    return Theme(
        background_color=(0, 0, 0),
        title_color=(255, 20, 147),             # Hot pink
        button_normal_color=(75, 0, 130),       # Indigo
        button_selected_color=(0, 255, 127),    # Neon green
        highlight_color=(0, 255, 255),          # Electric blue highlight
        border_color=(255, 105, 180),           # Pinkish border
        instruction_color=(255, 255, 255),
        font_color=(255, 255, 255),
        particle_color_palette=((255, 105, 180), (0, 255, 127)),
        star_text_color=(255, 255, 0),          # bright yellow for star text
        background_text_color=(0, 255, 127),    # same neon green as button

        # Effects
        rain_color=(0, 255, 255),
        snow_color=(255, 20, 147),
    )


@register_theme('pastel')
def pastel_theme() -> Theme:
    return Theme(
        background_color=(255, 250, 240),
        title_color=(135, 206, 250),
        button_normal_color=(85, 216, 242),
        button_selected_color=(255, 182, 193),
        highlight_color=(221, 160, 221),
        border_color=(216, 191, 216),
        instruction_color=(105, 105, 105),
        font_color=(47, 79, 79),
        particle_color_palette=((255, 182, 193), (152, 251, 152)),
        star_text_color=(221, 160, 221),
        background_text_color=(135, 206, 250),

        # Effects
        rain_color=(135, 206, 250),
        snow_color=(255, 182, 193),
    )


@register_theme('halloween')
def halloween_theme() -> Theme:
    return Theme(
        background_color=(20, 20, 20),
        title_color=(255, 140, 0),
        button_normal_color=(139, 69, 19),
        button_selected_color=(255, 69, 0),
        highlight_color=(255, 140, 0),
        border_color=(255, 140, 0),
        instruction_color=(255, 255, 255),
        font_color=(255, 255, 255),
        particle_color_palette=((255, 140, 0), (128, 0, 128)),
        star_text_color=(255, 140, 0),          # dark orange star text
        background_text_color=(128, 0, 128),    # purple background art

        # Effects
        rain_color=(255, 140, 0),
        snow_color=(128, 0, 128),
    )


@register_theme('christmas')
def christmas_theme() -> Theme:
    return Theme(
        background_color=(0, 64, 0),
        title_color=(255, 0, 0),
        button_normal_color=(255, 255, 255),
        button_selected_color=(255, 0, 0),
        highlight_color=(255, 215, 0),
        border_color=(255, 0, 0),
        instruction_color=(255, 255, 255),
        font_color=(255, 255, 255),
        particle_color_palette=((255, 0, 0), (0, 255, 0)),
        star_text_color=(255, 255, 255),        # white star text
        background_text_color=(255, 215, 0),    # gold for background art

        # Effects
        rain_color=(0, 255, 0),
        snow_color=(255, 255, 255),
    )


@register_theme('starwars')
def starwars_theme() -> Theme:
    return Theme(
        background_color=(0, 0, 0),
        title_color=(192, 192, 192),
        button_normal_color=(64, 64, 64),
        button_selected_color=(192, 192, 192),
        highlight_color=(0, 191, 255),
        border_color=(192, 192, 192),
        instruction_color=(192, 192, 192),
        font_color=(192, 192, 192),
        particle_color_palette=((192, 192, 192), (0, 191, 255)),
        star_text_color=(255, 255, 0),          # bright yellow text
        background_text_color=(192, 192, 192),  # silverish text

        # Effects
        rain_color=(0, 191, 255),
        snow_color=(192, 192, 192),
    )


# Set the active theme.
ACTIVE_THEME = theme_registry.get('default')
#ACTIVE_THEME = theme_registry.get('light')
#ACTIVE_THEME = theme_registry.get('retro80')
#ACTIVE_THEME = theme_registry.get('pastel')
#ACTIVE_THEME = theme_registry.get('halloween')
#ACTIVE_THEME = theme_registry.get('christmas')
#ACTIVE_THEME = theme_registry.get('starwars')

if ACTIVE_THEME is None:
    ACTIVE_THEME = theme_registry.get('default')