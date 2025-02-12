"""
menu_layer.py - Provides the interactive menu layer (title and buttons) for the main menu.

Version: 2.6
"""

import pygame
from typing import Any, Callable, List, Tuple
from ui_manager import Button
from base_layer import BaseLayer
from layout_constants import ButtonLayout, TitleLayout, LayerZIndex
from scene_manager import SceneManager
from config import Config

class MenuLayer(BaseLayer):
    """
    The interactive menu layer that displays a title and buttons for scene selection.
    """

    def __init__(self, scene_manager: SceneManager, font: pygame.font.Font, menu_items: List[Tuple[str, str]], config: Config) -> None:
        """
        Initializes the MenuLayer with the given scene manager, font, menu items, and configuration.
        
        Parameters:
            scene_manager: The manager responsible for scene transitions.
            font: The pygame font to be used for rendering text.
            menu_items: A list of tuples containing (label, scene_key) for each menu button.
            config: The configuration object containing theme and scaling information.
        """
        self.z: int = LayerZIndex.MENU
        self.scene_manager: SceneManager = scene_manager
        self.font: pygame.font.Font = font
        self.config: Config = config
        self.menu_items: List[Tuple[str, str]] = menu_items
        self.selected_index: int = 0
        self.last_nav_time: int = 0
        self.debounce_interval: int = 100  # milliseconds
        self.buttons: List[Any] = []
        self.create_buttons()

    def create_buttons(self) -> None:
        """
        Creates and positions the buttons for the menu based on configuration and scaling factors.
        Computes each scale value once and stores it in local variables.
        """
        button_width: int = self.config.scale_value(ButtonLayout.WIDTH_FACTOR)
        button_height: int = self.config.scale_value(ButtonLayout.HEIGHT_FACTOR)
        margin: int = self.config.scale_value(ButtonLayout.MARGIN_FACTOR)
        start_y: int = self.config.scale_value(ButtonLayout.START_Y_FACTOR)
        x: int = (self.config.screen_width - button_width) // 2
        self.buttons = []
        for i, (label, scene_key) in enumerate(self.menu_items):
            y: int = start_y + i * (button_height + margin)
            rect: Tuple[int, int, int, int] = (x, y, button_width, button_height)
            button: Button = Button(
                rect,
                label,
                self.make_callback(scene_key),
                self.font,
                normal_color=self.config.theme["button_normal_color"],
                selected_color=self.config.theme["button_selected_color"],
            )
            self.buttons.append(button)

    def make_callback(self, scene_key: str) -> Callable[[], None]:
        """
        Creates a callback function that sets the scene based on the provided scene_key.
        
        Parameters:
            scene_key: The key of the scene to switch to.
        
        Returns:
            A lambda function that calls the scene manager's set_scene method with the captured scene_key.
        """
        return lambda sk=scene_key: self.scene_manager.set_scene(sk)

    def _process_navigation(self, key: int) -> None:
        """
        Processes keyboard navigation input to move between menu items or select an item.
        
        Parameters:
            key: The key code from a KEYDOWN event.
        """
        if key in (pygame.K_w,):
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
        elif key in (pygame.K_s,):
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            self.buttons[self.selected_index].callback()

    def update(self) -> None:
        """
        Updates the menu layer.
        
        Currently, no dynamic updates are implemented.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the menu title and buttons onto the provided screen.
        
        Parameters:
            screen: The pygame Surface on which to draw the menu.
        """
        title_text: str = "MAIN MENU"
        title_surface: pygame.Surface = self.font.render(title_text, True, self.config.theme["title_color"])
        title_x: int = (self.config.screen_width - title_surface.get_width()) // 2
        screen.blit(title_surface, (title_x, self.config.scale_value(TitleLayout.Y_OFFSET)))
        for i, button in enumerate(self.buttons):
            selected: bool = i == self.selected_index
            button.draw(screen, selected)
            if selected:
                pygame.draw.rect(screen, self.config.theme["highlight_color"], button.rect, 3)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Handles input events for menu navigation.
        
        Parameters:
            event: A pygame event.
        """
        current_time: int = pygame.time.get_ticks()
        if current_time - self.last_nav_time < self.debounce_interval:
            return
        if event.type == pygame.KEYDOWN:
            self._process_navigation(event.key)
            self.last_nav_time = current_time
        elif event.type == pygame.TEXTINPUT:
            pass