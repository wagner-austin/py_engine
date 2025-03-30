"""
themes/themes.py - Contains theme definitions and dynamic blending for the application.
Summary: Provides multiple themes with a blending system; no keyboard references are present.
Version: 1.5.1
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
            if len(old_val) == len(new_val):
                new_field_values[field_name] = tuple(
                    interpolate_color(c1, c2, t)
                    for c1, c2 in zip(old_val, new_val)
                )
            else:
                new_field_values[field_name] = old_val if t < 1.0 else new_val

        else:
            new_field_values[field_name] = old_val if t < 1.0 else new_val

    return Theme(**new_field_values)


@register_theme('default')
def default_theme() -> Theme:
    return Theme(
        background_color=(0, 0, 0),
        title_color=(57, 255, 20),
        button_normal_color=(200, 0, 200),
        button_selected_color=(57, 255, 20),
        highlight_color=(57, 255, 20),
        border_color=(57, 255, 20),
        instruction_color=(255, 255, 255),
        font_color=(255, 255, 255),
        particle_color_palette=((200, 150, 255), (150, 200, 255)),
        star_text_color=(255, 255, 255),
        background_text_color=(57, 255, 20),
        rain_color=(0, 120, 255),
        snow_color=(255, 255, 255),
    )


@register_theme('light')
def light_theme() -> Theme:
    return Theme(
        background_color=(245, 245, 245),
        title_color=(50, 50, 50),
        button_normal_color=(200, 200, 200),
        button_selected_color=(70, 70, 70),
        highlight_color=(70, 70, 70),
        border_color=(150, 150, 150),
        instruction_color=(50, 50, 50),
        font_color=(50, 50, 50),
        particle_color_palette=((180, 180, 180), (160, 160, 160)),
        star_text_color=(50, 50, 50),
        background_text_color=(90, 90, 90),
        rain_color=(100, 100, 255),
        snow_color=(220, 220, 220),
    )


@register_theme('retro80')
def retro80_theme() -> Theme:
    return Theme(
        background_color=(0, 0, 0),
        title_color=(255, 20, 147),
        button_normal_color=(75, 0, 130),
        button_selected_color=(0, 255, 127),
        highlight_color=(0, 255, 255),
        border_color=(255, 105, 180),
        instruction_color=(255, 255, 255),
        font_color=(255, 255, 255),
        particle_color_palette=((255, 105, 180), (0, 255, 127)),
        star_text_color=(255, 255, 0),
        background_text_color=(0, 255, 127),
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
        star_text_color=(255, 140, 0),
        background_text_color=(128, 0, 128),
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
        star_text_color=(255, 255, 255),
        background_text_color=(255, 215, 0),
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
        star_text_color=(255, 255, 0),
        background_text_color=(192, 192, 192),
        rain_color=(0, 191, 255),
        snow_color=(192, 192, 192),
    )


ACTIVE_THEME = theme_registry.get('default')
if ACTIVE_THEME is None:
    ACTIVE_THEME = theme_registry.get('default')

# End of themes/themes.py