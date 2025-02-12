"""
base_scene.py - Base scene class providing common functionality and input handling for all scenes.

Version: 2.3
"""

import pygame

class BaseScene:
    def __init__(self, name, config, font, layer_manager, universal_factory, extra_layers=None):
        self.name = name
        self.config = config
        self.font = font
        self.layer_manager = layer_manager
        self.universal_factory = universal_factory
        self.extra_layers = extra_layers or []

    def populate_layers(self):
        """Clears the shared LayerManager and repopulates it with universal and scene-specific layers."""
        self.layer_manager.clear()
        # Add universal layers.
        for layer in self.universal_factory.get_universal_layers(self.font, self.config):
            self.layer_manager.add_layer(layer)
        # Add any extra (scene-specific) layers.
        for layer in self.extra_layers:
            self.layer_manager.add_layer(layer)

    def handle_event(self, event):
        self.on_input(event)

    def on_input(self, event):
        """Override in subclasses for scene-specific input handling.
        Default behavior forwards the event to the highest z-index layer that implements on_input.
        """
        self.forward_input(event)

    def forward_input(self, event):
        """Forwards the input event to the highest z-index layer that implements on_input."""
        for layer in self.layer_manager.get_sorted_layers(reverse=True):
            if hasattr(layer, "on_input"):
                layer.on_input(event)
                break

    def update(self):
        self.layer_manager.update()

    def draw(self, screen):
        # Use the config's theme for background color.
        bg_color = self.config.theme.get("background_color", (0, 0, 0))
        screen.fill(bg_color)
        self.layer_manager.draw(screen)

    def on_enter(self):
        """Called when the scene becomes active."""
        pass