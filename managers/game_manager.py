"""
managers/game_manager.py - Manages game modes and facilitates plug-and-play integration of different games.
Version: 1.0.0
Summary: Provides methods to load, switch, update, draw, and handle input for the current game mode.
"""

import pygame
from typing import Optional
from core.config import Config
from managers.layer_manager import LayerManager
from plugins.plugins import play_mode_registry

class GameManager:
    def __init__(self, font: pygame.font.Font, config: Config, layer_manager: LayerManager) -> None:
        """
        managers/game_manager.py - Initializes the GameManager.
        Version: 1.0.0
        Summary: Sets up the GameManager with the given font, configuration, and layer manager.
        """
        self.font = font
        self.config = config
        self.layer_manager = layer_manager
        self.current_game = None  # Instance of the current game mode.
        self.game_key: Optional[str] = None

    def load_game(self, game_key: str) -> None:
        """
        managers/game_manager.py - Loads a game mode from the play_mode_registry using the specified key.
        Version: 1.0.0
        """
        key = game_key.lower()
        if key in play_mode_registry:
            self.current_game = play_mode_registry[key](self.font, self.config, self.layer_manager)
            self.game_key = key
            if hasattr(self.current_game, "on_enter"):
                self.current_game.on_enter()
        else:
            print(f"Game mode '{game_key}' not found in play_mode_registry.")

    def update(self, dt: float) -> None:
        """
        managers/game_manager.py - Updates the current game mode.
        Version: 1.0.0
        """
        if self.current_game and hasattr(self.current_game, "update"):
            self.current_game.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """
        managers/game_manager.py - Draws the current game mode.
        Version: 1.0.0
        """
        if self.current_game and hasattr(self.current_game, "draw"):
            self.current_game.draw(screen)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        managers/game_manager.py - Forwards input events to the current game mode.
        Version: 1.0.0
        """
        if self.current_game and hasattr(self.current_game, "on_input"):
            self.current_game.on_input(event)

    def switch_game(self, game_key: str) -> None:
        """
        managers/game_manager.py - Switches to a different game mode.
        Version: 1.0.0
        """
        self.load_game(game_key)