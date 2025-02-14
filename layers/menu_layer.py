"""
menu_layer.py
-------------
Provides the interactive menu layer (title and buttons) for the main menu.
Version: 2.13.0
"""

import pygame
from typing import Callable, List, Tuple
from functools import partial
from ui.ui_elements import Button
from .base_layer import BaseLayer
from ui.layout_constants import ButtonLayout, TitleLayout, MenuLayout, LayerZIndex
from managers.scene_manager import SceneManager
from core.config import Config
from core.controls import MENU_NAVIGATION  # Import centralized menu navigation keys
from plugins.plugins import register_layer

@register_layer("menu_layer", "menu_only")
class MenuLayer(BaseLayer):
    """
    The interactive menu layer that displays a title and buttons for scene selection.
    """

    def __init__(
        self,
        scene_manager: SceneManager,
        font: pygame.font.Font,
        menu_items: List[Tuple[str, str]],
        config: Config
    ) -> None:
        """
        Initializes the MenuLayer with static configuration.

        Parameters:
            scene_manager (SceneManager): The manager responsible for scene transitions.
            font (pygame.font.Font): The pygame font to be used for rendering text.
            menu_items (List[Tuple[str, str]]): A list of tuples containing (label, scene_key) for each menu button.
            config (Config): The configuration object containing theme and scaling information.
        """
        self.z: int = LayerZIndex.MENU
        self.scene_manager: SceneManager = scene_manager
        self.font: pygame.font.Font = font
        self.config: Config = config
        self.menu_items: List[Tuple[str, str]] = menu_items

        self.selected_index: int = 0
        self.last_nav_time: int = 0
        self.debounce_interval: int = MenuLayout.DEBOUNCE_INTERVAL_MS  # Debounce interval in ms.
        self.buttons: List[Button] = []
        self.title_y: int = 0  # Computed in _setup_buttons().

        self._setup_buttons()

    def update(self, dt: float) -> None:
        """
        Updates the menu layer. 
        Currently, no dynamic animation or effect is handled here.
        """
        pass  # Particle logic is now handled in a separate plugin layer.

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the menu title and buttons onto the provided screen.

        Parameters:
            screen (pygame.Surface): The pygame Surface on which to draw the menu.
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

        Parameters:
            event (pygame.event.Event): The input event to be processed.
        """
        current_time: int = pygame.time.get_ticks()
        if current_time - self.last_nav_time < self.debounce_interval:
            return

        if event.type == pygame.KEYDOWN:
            self._process_navigation(event.key)
            self.last_nav_time = current_time
        elif event.type == pygame.TEXTINPUT:
            pass

    def _setup_buttons(self) -> None:
        """
        Creates and positions the buttons for the menu based on configuration and scaling factors.

        The entire menu (title plus buttons) is centered vertically.
        """
        button_width: int = self.config.scale_value(ButtonLayout.WIDTH_FACTOR)
        button_height: int = self.config.scale_value(ButtonLayout.HEIGHT_FACTOR)
        margin: int = self.config.scale_value(ButtonLayout.MARGIN_FACTOR)

        # Render title to get its height.
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
                self._make_callback(scene_key),
                self.font,
                normal_color=self.config.theme.button_normal_color,
                selected_color=self.config.theme.button_selected_color,
            )
            self.buttons.append(button)

    def _make_callback(self, scene_key: str) -> Callable[[], None]:
        """
        Creates a callback function that sets the scene based on the provided scene_key.

        Parameters:
            scene_key (str): The key of the scene to switch to.

        Returns:
            Callable[[], None]: A callable that calls the scene manager's set_scene method with the captured scene_key.
        """
        return partial(self._change_scene, scene_key)

    def _process_navigation(self, key: int) -> None:
        """
        Processes keyboard navigation input to move between menu items or select an item.

        Parameters:
            key (int): The key code from a KEYDOWN event.
        """
        old_index = self.selected_index
        if key == MENU_NAVIGATION["up"]:
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
        elif key == MENU_NAVIGATION["down"]:
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
        elif key in MENU_NAVIGATION["select"]:
            self.buttons[self.selected_index].callback()

    def _change_scene(self, scene_key: str) -> None:
        """
        Helper function to change the scene or quit the application.

        Parameters:
            scene_key (str): The key of the scene to switch to.
        """
        if scene_key == "quit":
            import sys
            pygame.quit()
            sys.exit(0)
        else:
            self.scene_manager.set_scene(scene_key)