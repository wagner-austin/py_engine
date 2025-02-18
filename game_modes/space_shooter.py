"""
space_shooter.py - A blank template for a space shooter game mode.
Version: 1.0.0
Summary: Registers a new game mode called "space_shooter" that integrates with the GameManager and PlayAreaLayer.
"""

import pygame
from core.config import Config
from managers.layer_manager import LayerManager
from plugins.plugins import register_play_mode

@register_play_mode("Space Shooter")
class SpaceShooter:
    """
    space_shooter.py - A placeholder for the Space Shooter game mode.
    Version: 1.0.0
    Summary: This game mode is registered via the plugin system and can be selected dynamically.
    """

    def __init__(self, font: pygame.font.Font, config: Config, layer_manager: LayerManager) -> None:
        """
        Initializes the Space Shooter game mode.
        Version: 1.0.0
        """
        self.font = font
        self.config = config
        self.layer_manager = layer_manager

    def on_enter(self) -> None:
        """
        Called when the game mode starts.
        Version: 1.0.0
        """
        print("Entered Space Shooter mode.")

    def update(self, dt: float) -> None:
        """
        Updates game logic.
        Version: 1.0.0
        """
        pass  # Placeholder for game update logic

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the game onto the screen.
        Version: 1.0.0
        """
        text = self.font.render("Space Shooter Mode", True, self.config.theme.font_color)
        rect = text.get_rect(center=(self.config.screen_width // 2, self.config.screen_height // 2))
        screen.blit(text, rect)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Handles player input.
        Version: 1.0.0
        """
        pass  # Placeholder for input handling