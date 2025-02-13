"""
menu_layer.py - Provides the interactive menu layer (title and buttons) for the main menu.
Version: 2.12 (modified for Quit option handling, centered menu, and unified particle effects)
"""

import pygame
from typing import Callable, List, Tuple
from functools import partial
from ui_elements import Button
from effects.particle_effect import create_default_continuous_effect
from .base_layer import BaseLayer
from layout_constants import ButtonLayout, TitleLayout, MenuLayout, LayerZIndex
from managers.scene_manager import SceneManager
from config import Config
from controls import MENU_NAVIGATION  # Import centralized menu navigation keys

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
        self.debounce_interval: int = MenuLayout.DEBOUNCE_INTERVAL_MS  # Debounce interval in milliseconds.
        self.buttons: List[Button] = []
        self.title_y: int = 0  # Will be computed in create_buttons()
        self.create_buttons()
        # Instantiate a single particle effect using the continuous effect factory.
        self.continuous_effect = create_default_continuous_effect()
        self.continuous_spawn_timer: float = 0.0
        self.continuous_spawn_interval: float = 0.2  # Spawn gentle particles every 0.2 seconds

    def update(self, dt: float) -> None:
        """
        Updates the menu layer, including the particle effect.
        
        Parameters:
            dt: Delta time in seconds.
        """
        self.continuous_effect.update(dt)
        self.continuous_spawn_timer += dt
        if self.continuous_spawn_timer >= self.continuous_spawn_interval:
            # Continuously spawn gentle, softly falling particles around the highlighted button.
            current_button = self.buttons[self.selected_index]
            self.continuous_effect.spawn_continuous_from_rect(current_button.rect)
            self.continuous_spawn_timer = 0.0

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the menu title, buttons, and the particle effect onto the provided screen.
        
        Parameters:
            screen: The pygame Surface on which to draw the menu.
        """
        title_text: str = "MAIN MENU"
        title_surface: pygame.Surface = self.font.render(title_text, True, self.config.theme.title_color)
        title_x: int = (self.config.screen_width - title_surface.get_width()) // 2
        screen.blit(title_surface, (title_x, self.title_y))
        for i, button in enumerate(self.buttons):
            selected: bool = i == self.selected_index
            button.draw(screen, selected)
        # Draw the continuous particle effect.
        self.continuous_effect.draw(screen)

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

    def create_buttons(self) -> None:
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
            rect: Tuple[int, int, int, int] = (x, y, button_width, button_height)
            button: Button = Button(
                rect,
                label,
                self.make_callback(scene_key),
                self.font,
                normal_color=self.config.theme.button_normal_color,
                selected_color=self.config.theme.button_selected_color,
            )
            self.buttons.append(button)

    def make_callback(self, scene_key: str) -> Callable[[], None]:
        """
        Creates a callback function that sets the scene based on the provided scene_key.
        
        Parameters:
            scene_key: The key of the scene to switch to.
        
        Returns:
            A callable that calls the scene manager's set_scene method with the captured scene_key.
        """
        return partial(self._change_scene, scene_key)

    def _process_navigation(self, key: int) -> None:
        """
        Processes keyboard navigation input to move between menu items or select an item.
        Triggers a particle effect upon selection change.
        
        Parameters:
            key: The key code from a KEYDOWN event.
        """
        old_index = self.selected_index
        if key == MENU_NAVIGATION["up"]:
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
        elif key == MENU_NAVIGATION["down"]:
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
        elif key in MENU_NAVIGATION["select"]:
            self.buttons[self.selected_index].callback()
        if self.selected_index != old_index:
            # Trigger a particle effect when the selection changes.
            new_button = self.buttons[self.selected_index]
            self.continuous_effect.spawn_continuous_from_rect(new_button.rect)

    def _change_scene(self, scene_key: str) -> None:
        """
        Helper function to change the scene.
        
        Parameters:
            scene_key: The key of the scene to switch to.
        """
        if scene_key == "quit":
            import sys
            pygame.quit()
            sys.exit(0)
        else:
            self.scene_manager.set_scene(scene_key)