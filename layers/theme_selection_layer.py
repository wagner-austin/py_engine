"""
theme_selection_layer.py - Provides a layer for selecting and modifying the application theme.
Version: 1.0.7
"""

import pygame
from ui.ui_elements import Button
from .base_layer import BaseLayer
from plugins.plugins import theme_registry
from core.config import Config
from typing import List, Optional, Callable, Tuple
from ui.layout_constants import LayerZIndex, ButtonLayout, TitleLayout
from core.controls import MENU_NAVIGATION
from themes.themes import Theme  # For type annotations

def interpolate_color(color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    """
    Interpolates between two colors.
    Version: 1.0.7
    """
    return (
        int(color1[0] + (color2[0] - color1[0]) * t),
        int(color1[1] + (color2[1] - color1[1]) * t),
        int(color1[2] + (color2[2] - color1[2]) * t)
    )

def blend_themes(old_theme: Theme, new_theme: Theme, t: float) -> Theme:
    """
    Blends two themes based on t (0.0 to 1.0).
    Version: 1.0.7
    """
    def blend_palette(palette1, palette2, t):
        if len(palette1) == len(palette2):
            return tuple(interpolate_color(p1, p2, t) for p1, p2 in zip(palette1, palette2))
        else:
            return palette2

    return Theme(
        background_color=interpolate_color(old_theme.background_color, new_theme.background_color, t),
        title_color=interpolate_color(old_theme.title_color, new_theme.title_color, t),
        button_normal_color=interpolate_color(old_theme.button_normal_color, new_theme.button_normal_color, t),
        button_selected_color=interpolate_color(old_theme.button_selected_color, new_theme.button_selected_color, t),
        highlight_color=interpolate_color(old_theme.highlight_color, new_theme.highlight_color, t),
        border_color=interpolate_color(old_theme.border_color, new_theme.border_color, t),
        instruction_color=interpolate_color(old_theme.instruction_color, new_theme.instruction_color, t),
        font_color=interpolate_color(old_theme.font_color, new_theme.font_color, t),
        particle_color_palette=blend_palette(old_theme.particle_color_palette, new_theme.particle_color_palette, t)
    )

class ThemeSelectionLayer(BaseLayer):
    def __init__(self, font: pygame.font.Font, config: Config, layer_manager, parent_scene, 
                 refresh_callback: Optional[Callable[[], None]] = None, 
                 back_callback: Optional[Callable[[], None]] = None,
                 initial_selected_index: int = 0) -> None:
        """
        Initializes the ThemeSelectionLayer with standardized constructor signature.
        Version: 1.0.7

        Parameters:
            font (pygame.font.Font): The font used for rendering.
            config (Config): The configuration object.
            layer_manager: The layer manager to add/remove layers.
            parent_scene: The parent scene that owns this layer.
            refresh_callback (Optional[Callable[[], None]]): Callback to refresh the scene after transition.
            back_callback (Optional[Callable[[], None]]): Callback for back navigation.
            initial_selected_index (int, optional): The initial selected index. Defaults to 0.
        """
        self.font: pygame.font.Font = font
        self.config: Config = config
        self.layer_manager = layer_manager
        self.parent_scene = parent_scene
        self.refresh_callback = refresh_callback
        self.back_callback = back_callback
        self.selected_index: int = initial_selected_index
        self.buttons: List[Button] = []
        self.title: str = "Select Theme"
        self.z = LayerZIndex.MENU + 1
        self._setup_buttons()
        self.old_theme: Optional[Theme] = None
        self.new_theme: Optional[Theme] = None
        self.theme_transition_elapsed: float = 0.0
        self.theme_transition_duration: float = 1.0

    def _setup_buttons(self) -> None:
        """
        Creates buttons for each available theme (alphabetically sorted)
        and adds a 'Back' option.
        Version: 1.0.7
        """
        theme_keys = list(theme_registry.keys())
        theme_keys.sort()
        theme_keys.append("Back")

        button_width = self.config.scale_value(ButtonLayout.WIDTH_FACTOR)
        button_height = self.config.scale_value(ButtonLayout.HEIGHT_FACTOR)
        margin = self.config.scale_value(ButtonLayout.MARGIN_FACTOR)

        title_surface = self.font.render(self.title, True, self.config.theme.title_color)
        title_height = title_surface.get_height()
        title_to_button_margin = margin

        n = len(theme_keys)
        total_buttons_height = n * button_height + (n - 1) * margin
        total_menu_height = title_height + title_to_button_margin + total_buttons_height
        start_y = (self.config.screen_height - total_menu_height) // 2
        button_start_y = start_y + title_height + title_to_button_margin
        start_x = (self.config.screen_width - button_width) // 2

        self.buttons = []
        for i, key in enumerate(theme_keys):
            rect = (start_x, button_start_y + i * (button_height + margin), button_width, button_height)
            button = Button(
                rect,
                key,
                callback=lambda key=key: self._on_button_pressed(key),
                font=self.font,
                normal_color=self.config.theme.button_normal_color,
                selected_color=self.config.theme.button_selected_color,
            )
            self.buttons.append(button)

    def _on_button_pressed(self, key: str) -> None:
        """
        Callback when a button is pressed.
        Version: 1.0.7

        If a theme is selected, begins a gradual transition from the current theme to the new theme.
        """
        self.parent_scene.last_theme_index = self.selected_index
        if key == "Back":
            if self.back_callback:
                self.back_callback()
            else:
                self.layer_manager.remove_layer(self)
        else:
            new_theme = theme_registry.get(key)
            if new_theme:
                self.old_theme = self.config.theme
                self.new_theme = new_theme
                self.theme_transition_elapsed = 0.0

    def update(self, dt: float) -> None:
        """
        Updates the layer.
        Version: 1.0.7

        Gradually updates the config.theme based on the transition progress.
        """
        for button in self.buttons:
            button.normal_color = self.config.theme.button_normal_color
            button.selected_color = self.config.theme.button_selected_color
            button.update()

        if self.new_theme is not None:
            self.theme_transition_elapsed += dt
            progress = min(1.0, self.theme_transition_elapsed / self.theme_transition_duration)
            self.config.theme = blend_themes(self.old_theme, self.new_theme, progress)
            if progress >= 1.0:
                self.new_theme = None
                if self.refresh_callback:
                    self.refresh_callback()
                self.layer_manager.remove_layer(self)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the theme selection title and buttons.
        Version: 1.0.7
        """
        title_surface = self.font.render(self.title, True, self.config.theme.title_color)
        title_x = (self.config.screen_width - title_surface.get_width()) // 2
        screen.blit(title_surface, (title_x, TitleLayout.Y_OFFSET))
        for i, button in enumerate(self.buttons):
            selected = (i == self.selected_index)
            button.draw(screen, selected)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Handles keyboard input for navigating the theme selection.
        Version: 1.0.7
        """
        if event.type == pygame.KEYDOWN:
            if event.key == MENU_NAVIGATION["up"]:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
            elif event.key == MENU_NAVIGATION["down"]:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
            elif event.key in MENU_NAVIGATION["select"]:
                self.buttons[self.selected_index].callback()