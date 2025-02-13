"""
base_scene.py - Base scene class providing common functionality and input handling for all scenes.
"""

import pygame
from typing import List, Optional
from config import Config
from managers.layer_manager import LayerManager
from layers.universal_layers import UniversalLayerFactory
from layers.base_layer import BaseLayer  # For type hinting extra_layers
from interfaces import IInputHandler

class BaseScene:
    def __init__(
        self,
        name: str,
        config: Config,
        font: pygame.font.Font,
        layer_manager: LayerManager,
        universal_factory: UniversalLayerFactory,
        extra_layers: Optional[List[BaseLayer]] = None,
    ) -> None:
        self.name: str = name
        self.config: Config = config
        self.font: pygame.font.Font = font
        self.layer_manager: LayerManager = layer_manager
        self.universal_factory: UniversalLayerFactory = universal_factory
        self.extra_layers: List[BaseLayer] = extra_layers or []

    def populate_layers(self) -> None:
        self.layer_manager.clear()
        # Add all universal layers.
        for layer in self.universal_factory.get_universal_layers(self.font, self.config):
            self.layer_manager.add_layer(layer)
        # Add scene-specific extra layers.
        for layer in self.extra_layers:
            self.layer_manager.add_layer(layer)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Dispatches the event to the scene's input handler."""
        self.on_input(event)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Default behavior: Forwards the event to the highest z-index layer that implements on_input.
        Subclasses may override this method for scene-specific input handling.
        """
        self.forward_input(event)

    def forward_input(self, event: pygame.event.Event) -> None:
        """Forwards the input event to the highest z-index layer that implements on_input."""
        for layer in self.layer_manager.get_sorted_layers(reverse=True):
            if hasattr(layer, "on_input"):
                layer.on_input(event)
                break

    def update(self, dt: float) -> None:
        """Updates the scene by updating the layer manager."""
        self.layer_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the scene onto the provided screen.

        Parameters:
            screen: The pygame Surface on which to draw the scene.
        """
        bg_color = self.config.theme.background_color
        screen.fill(bg_color)
        self.layer_manager.draw(screen)

    def on_enter(self) -> None:
        """Called when the scene becomes active."""
        pass