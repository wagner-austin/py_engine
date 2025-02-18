"""
play_area_layer.py - Provides a dedicated play area layer for hosting plug-and-play game modes.
Version: 1.0.0
Summary: Defines a layer that occupies most of the screen and delegates game logic to a GameManager.
"""

import pygame
from layers.base_layer import BaseLayer
from core.config import Config
from managers.game_manager import GameManager
from managers.layer_manager import LayerManager

class PlayAreaLayer(BaseLayer):
    def __init__(self, font: pygame.font.Font, config: Config, layer_manager: LayerManager, game_key: str = "default", margin: int = None) -> None:
        """
        play_area_layer.py - Initializes the PlayAreaLayer.
        Version: 1.0.0
        Summary: Sets up a dedicated play area within the scene that hosts a game mode via GameManager.
        """
        self.font = font
        self.config = config
        self.layer_manager = layer_manager
        self.game_key = game_key
        # Use provided margin or default to a scaled value (e.g., 50 pixels).
        self.margin = margin if margin is not None else config.scale_value(50)
        self.game_manager = GameManager(font, config, layer_manager)
        self.game_manager.load_game(game_key)
        self.z = 1  # Set an appropriate z-index for the play area layer

    def update(self, dt: float) -> None:
        self.game_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        # Define the play area rectangle based on the margin.
        area_rect = pygame.Rect(self.margin, self.margin, self.config.screen_width - 2 * self.margin, self.config.screen_height - 2 * self.margin)
        # Fill the play area with the active theme's background color.
        pygame.draw.rect(screen, self.config.theme.background_color, area_rect)
        # Set the clipping region so that drawing is confined to the play area.
        prev_clip = screen.get_clip()
        screen.set_clip(area_rect)
        self.game_manager.draw(screen)
        screen.set_clip(prev_clip)

    def on_input(self, event: pygame.event.Event) -> None:
        # For mouse events, only forward the event if the position is within the play area.
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            if hasattr(event, "pos"):
                area_rect = pygame.Rect(self.margin, self.margin, self.config.screen_width - 2 * self.margin, self.config.screen_height - 2 * self.margin)
                if not area_rect.collidepoint(event.pos):
                    return
        self.game_manager.on_input(event)