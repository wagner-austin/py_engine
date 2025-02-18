"""
menu_layer.py - Provides the interactive menu layer (title and buttons) for the main menu.
Version: 2.13.2
"""

import pygame
from typing import Callable, List, Tuple
from ui.ui_elements import Button
from .base_layer import BaseLayer
from ui.layout_constants import ButtonLayout, TitleLayout, MenuLayout, LayerZIndex
from managers.scene_manager import SceneManager
from core.config import Config
from core.controls import MENU_NAVIGATION
from plugins.plugins import register_layer

@register_layer("menu_layer", "menu_only")
class MenuLayer(BaseLayer):
    def __init__(self, font: pygame.font.Font, config: Config, scene_manager: SceneManager, menu_items: List[Tuple[str, str]], initial_selected_index: int = 0) -> None:
        """
        Initializes the MenuLayer with standardized constructor signature.
        Version: 2.13.2

        Parameters:
            font (pygame.font.Font): The font used for rendering.
            config (Config): The configuration object.
            scene_manager (SceneManager): The scene manager for navigation.
            menu_items (List[Tuple[str, str]]): A list of tuples containing button label and target scene key.
            initial_selected_index (int, optional): The initial selected button index. Defaults to 0.
        """
        self.font: pygame.font.Font = font
        self.config: Config = config
        self.scene_manager: SceneManager = scene_manager
        self.menu_items: List[Tuple[str, str]] = menu_items
        self.selected_index: int = initial_selected_index
        self.last_nav_time: int = 0
        self.debounce_interval: int = MenuLayout.DEBOUNCE_INTERVAL_MS
        self.buttons: List[Button] = []
        self.title_y: int = 0
        self.z: int = LayerZIndex.MENU
        self._setup_buttons()

    def _setup_buttons(self) -> None:
        """
        Creates and positions the buttons for the menu.
        """
        button_width: int = self.config.scale_value(ButtonLayout.WIDTH_FACTOR)
        button_height: int = self.config.scale_value(ButtonLayout.HEIGHT_FACTOR)
        margin: int = self.config.scale_value(ButtonLayout.MARGIN_FACTOR)

        title_text: str = "MAIN MENU"
        title_surface: pygame.Surface = self.font.render(title_text, True, self.config.theme.title_color)
        title_height: int = title_surface.get_height()
        title_to_button_margin: int = margin

        n: int = len(self.menu_items)
        total_buttons_height: int = n * button_height + (n - 1) * margin
        total_menu_height: int = title_height + title_to_button_margin + total_buttons_height
        start_y: int = (self.config.screen_height - total_menu_height) // 2
        self.title_y = start_y
        button_start_y: int = start_y + title_height + title_to_button_margin

        x: int = (self.config.screen_width - button_width) // 2
        self.buttons = []
        for i, (label, scene_key) in enumerate(self.menu_items):
            y: int = button_start_y + i * (button_height + margin)
            rect = (x, y, button_width, button_height)
            button = Button(
                rect,
                label,
                callback=lambda key=scene_key: self._change_scene(key),
                font=self.font,
                normal_color=self.config.theme.button_normal_color,
                selected_color=self.config.theme.button_selected_color,
            )
            self.buttons.append(button)

    def _change_scene(self, scene_key: str) -> None:
        """
        Helper function to change the scene.
        Stores the current selection in the parent scene for persistence.
        """
        if hasattr(self.scene_manager.current_scene, "last_menu_index"):
            self.scene_manager.current_scene.last_menu_index = self.selected_index
        else:
            self.scene_manager.current_scene.last_menu_index = self.selected_index
        if scene_key == "quit":
            import sys
            pygame.quit()
            sys.exit(0)
        else:
            self.scene_manager.set_scene(scene_key)

    def update(self, dt: float) -> None:
        """
        Updates the menu layer.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the menu title and buttons.
        """
        title_text: str = "MAIN MENU"
        title_surface: pygame.Surface = self.font.render(title_text, True, self.config.theme.title_color)
        title_x: int = (self.config.screen_width - title_surface.get_width()) // 2
        screen.blit(title_surface, (title_x, self.title_y))
        for i, button in enumerate(self.buttons):
            selected: bool = (i == self.selected_index)
            button.draw(screen, selected)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Handles input events for menu navigation.
        """
        current_time: int = pygame.time.get_ticks()
        if current_time - self.last_nav_time < self.debounce_interval:
            return

        if event.type == pygame.KEYDOWN:
            self._process_navigation(event.key)
            self.last_nav_time = current_time

    def _process_navigation(self, key: int) -> None:
        """
        Processes navigation keys.
        """
        if key == MENU_NAVIGATION["up"]:
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
        elif key == MENU_NAVIGATION["down"]:
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
        elif key in MENU_NAVIGATION["select"]:
            self.buttons[self.selected_index].callback()