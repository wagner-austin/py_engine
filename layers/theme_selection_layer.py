"""
theme_selection_layer.py - Provides a layer for selecting and modifying the application theme.
Version: 1.0.4
"""

import pygame
from ui.ui_elements import Button
from layers.base_layer import BaseLayer
from plugins.plugins import theme_registry
from core.config import Config
from typing import List, Optional, Callable
from ui.layout_constants import LayerZIndex, ButtonLayout, TitleLayout
from core.controls import MENU_NAVIGATION  # Import centralized menu navigation keys

class ThemeSelectionLayer(BaseLayer):
    def __init__(
        self,
        config: Config,
        font: pygame.font.Font,
        layer_manager,
        refresh_callback: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Initializes the ThemeSelectionLayer.

        Parameters:
            config (Config): The global configuration object.
            font (pygame.font.Font): The font used for rendering.
            layer_manager: The manager responsible for handling layers.
            refresh_callback (Optional[Callable[[], None]]): Callback to refresh the scene after a theme is selected.
        """
        self.config = config
        self.font = font
        self.layer_manager = layer_manager
        self.refresh_callback = refresh_callback
        self.selected_index: int = 0
        self.buttons: List[Button] = []
        self.title: str = "Select Theme"
        # Set the z-index so that the layer manager can sort layers without error.
        self.z = LayerZIndex.MENU + 1
        self._setup_buttons()

    def _setup_buttons(self) -> None:
        """
        Creates buttons for each available theme (alphabetically sorted)
        and adds a 'Back' option.
        """
        # Get all registered theme keys and sort them
        theme_keys = list(theme_registry.keys())
        theme_keys.sort()
        # Append a "Back" option to allow returning from the theme selector.
        theme_keys.append("Back")
        
        # Use configuration scaling for button layout values
        button_width = self.config.scale_value(ButtonLayout.WIDTH_FACTOR)
        button_height = self.config.scale_value(ButtonLayout.HEIGHT_FACTOR)
        margin = self.config.scale_value(ButtonLayout.MARGIN_FACTOR)
        
        # Render title to get its height.
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
        If a theme is selected, update the config.theme accordingly and refresh the scene.
        If 'Back' is pressed, remove this layer.
        """
        if key == "Back":
            self.layer_manager.remove_layer(self)
        else:
            new_theme = theme_registry.get(key)
            if new_theme:
                self.config.theme = new_theme
                print(f"Theme changed to: {key}")
                # Refresh the scene if a refresh callback is provided.
                if self.refresh_callback:
                    self.refresh_callback()
            self.layer_manager.remove_layer(self)

    def update(self, dt: float) -> None:
        """
        Updates the layer (no dynamic elements needed for now).
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the theme selection title and buttons.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the layer.
        """
        # Draw the title using a layout constant for the Y offset.
        title_surface = self.font.render(self.title, True, self.config.theme.title_color)
        title_x = (self.config.screen_width - title_surface.get_width()) // 2
        screen.blit(title_surface, (title_x, TitleLayout.Y_OFFSET))
        # Draw all buttons, highlighting the currently selected one.
        for i, button in enumerate(self.buttons):
            selected = (i == self.selected_index)
            button.draw(screen, selected)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Handles keyboard input for navigating the theme selection.
        Use W/S keys to change the selection and RETURN/SPACE to select.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == MENU_NAVIGATION["up"]:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
            elif event.key == MENU_NAVIGATION["down"]:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
            elif event.key in MENU_NAVIGATION["select"]:
                self.buttons[self.selected_index].callback()