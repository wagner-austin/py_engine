"""
layout_constants.py - Contains layout and z-index constants for UI components and layers.

Version: 1.1
"""

from enum import IntEnum

class ButtonLayout:
    WIDTH_FACTOR = 300
    HEIGHT_FACTOR = 70
    MARGIN_FACTOR = 30
    START_Y_FACTOR = 150

class TitleLayout:
    Y_OFFSET = 40

class BorderLayout:
    THICKNESS_FACTOR = 4

class ArtLayout:
    STAR_MARGIN_FACTOR = 20
    BACKGROUND_VERTICAL_FACTOR = 0.5

class LayerZIndex(IntEnum):
    """
    Enum for layer z-index values.
    """
    STAR_ART = 0
    RAIN_EFFECT = 1
    BACKGROUND_ART = 2
    INSTRUCTIONS = 3
    MENU = 4
    BORDER = 5
    TEST = 6