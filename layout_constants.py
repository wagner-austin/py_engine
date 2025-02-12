"""
layout_constants.py - Contains layout and z-index constants for UI components and layers.

Version: 1.2 (updated with additional color constants)
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

class ArtColors:
    STAR_TEXT = (150, 150, 150)
    BACKGROUND_TEXT = (100, 255, 100)

class InstructionLayout:
    # Base pixel margins (before scaling) for the instruction layer
    LEFT_MARGIN_PX = 20
    BOTTOM_MARGIN_PX = 40

class MenuLayout:
    # Debounce interval (in milliseconds) for menu navigation input
    DEBOUNCE_INTERVAL_MS = 100

class EffectColors:
    RAIN_EFFECT = (100, 100, 255)

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