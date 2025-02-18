"""
game_mode_selection_layer.py - Provides a selection layer for choosing game modes.
Version: 1.0.2
Summary: Displays a list of available game modes from play_mode_registry; selecting a mode updates config.selected_game_mode and transitions to the Play scene.
         This layer supports plug-and-play particle effects via the unified layer registry and recalls the last selection.
"""

import pygame
from ui.ui_elements import Button
from layers.base_layer import BaseLayer
from plugins.plugins import play_mode_registry
from core.config import Config
from typing import List
from ui.layout_constants import LayerZIndex, ButtonLayout, TitleLayout
from core.controls import MENU_NAVIGATION
from managers.scene_manager import SceneManager

class GameModeSelectionLayer(BaseLayer):
    def __init__(self, config: Config, font: pygame.font.Font, layer_manager, scene_manager: SceneManager, parent_scene, initial_selected_index: int = 0) -> None:
        """
        Initializes the GameModeSelectionLayer.
        Version: 1.0.2
        Summary: Lists all registered game modes and provides a callback to change scenes.
                 Also accepts a parent_scene to remember the last selected index.
        """
        self.config = config
        self.font = font
        self.layer_manager = layer_manager
        self.scene_manager = scene_manager
        self.parent_scene = parent_scene
        self.selected_index: int = initial_selected_index
        self.buttons: List[Button] = []
        self.title: str = "Select Game Mode"
        self.z = LayerZIndex.MENU + 1
        self._setup_buttons()

    def _setup_buttons(self) -> None:
        """
        Creates buttons for each available game mode and adds a 'Back' option.
        Version: 1.0.2
        """
        # Get game mode keys from play_mode_registry and sort them
        game_mode_keys = sorted(play_mode_registry.keys())
        game_mode_keys.append("Back")
          
        button_width = self.config.scale_value(ButtonLayout.WIDTH_FACTOR)
        button_height = self.config.scale_value(ButtonLayout.HEIGHT_FACTOR)
        margin = self.config.scale_value(ButtonLayout.MARGIN_FACTOR)
          
        title_surface = self.font.render(self.title, True, self.config.theme.title_color)
        title_height = title_surface.get_height()
        title_to_button_margin = margin

        n = len(game_mode_keys)
        total_buttons_height = n * button_height + (n - 1) * margin
        total_menu_height = title_height + title_to_button_margin + total_buttons_height
        start_y = (self.config.screen_height - total_menu_height) // 2
        button_start_y = start_y + title_height + title_to_button_margin
        start_x = (self.config.screen_width - button_width) // 2

        self.buttons = []
        for i, key in enumerate(game_mode_keys):
            rect = (start_x, button_start_y + i * (button_height + margin), button_width, button_height)
            button = Button(
                rect,
                key.title(),  # Display with capitalized words
                callback=lambda key=key: self._on_button_pressed(key),
                font=self.font,
                normal_color=self.config.theme.button_normal_color,
                selected_color=self.config.theme.button_selected_color,
            )
            self.buttons.append(button)

    def _on_button_pressed(self, key: str) -> None:
        """
        Callback when a button is pressed.
        Version: 1.0.2
        Summary: If 'Back' is selected, returns to the Home scene; otherwise, updates the selected game mode and transitions to Play.
                 Also updates the parent's last selection index.
        """
        self.parent_scene.last_selection_index = self.selected_index
        if key.lower() == "back":
            self.scene_manager.set_scene("menu")
        else:
            self.config.selected_game_mode = key.lower()
            self.scene_manager.set_scene("play")

    def update(self, dt: float) -> None:
        """
        Updates the selection layer.
        Version: 1.0.2
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the game mode selection title and buttons.
        Version: 1.0.2
        """
        title_surface = self.font.render(self.title, True, self.config.theme.title_color)
        title_x = (self.config.screen_width - title_surface.get_width()) // 2
        screen.blit(title_surface, (title_x, TitleLayout.Y_OFFSET))
        for i, button in enumerate(self.buttons):
            selected = (i == self.selected_index)
            button.draw(screen, selected)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Handles keyboard input for navigating the selection.
        Version: 1.0.2
        """
        if event.type == pygame.KEYDOWN:
            if event.key == MENU_NAVIGATION["up"]:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
            elif event.key == MENU_NAVIGATION["down"]:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
            elif event.key in MENU_NAVIGATION["select"]:
                self.buttons[self.selected_index].callback()
            # Update parent's last selection index on navigation
            self.parent_scene.last_selection_index = self.selected_index