# File: base_scene.py
# Version: 2.3 (modified)
# Summary: Base scene class providing common functionality and input handling for all scenes.
#          Supports a layered system and clears the screen before drawing.
#          Now accepts a config instance and font as dependencies, and automatically adds universal layers.
# Tags: scene, base, modular, input handling

import pygame
from layer_manager import LayerManager
from universal_layers import get_universal_layers

class BaseScene:
    def __init__(self, name, config, font, extra_layers=None):
        self.name = name
        self.config = config
        self.font = font
        self.layer_manager = LayerManager()
        # Add universal layers
        for layer in get_universal_layers(font, config):
            self.layer_manager.add_layer(layer)
        # Add any extra layers provided by the subclass
        if extra_layers:
            for layer in extra_layers:
                self.layer_manager.add_layer(layer)

    def handle_event(self, event):
        # Delegate scene-specific input.
        self.on_input(event)

    def on_input(self, event):
        """Override in subclasses for scene-specific input handling.
        Default behavior is to forward the event to the highest z-index layer that implements on_input.
        """
        self.forward_input(event)

    def forward_input(self, event):
        """
        Forwards the input event to the highest z-index layer that implements on_input.
        """
        for layer in self.layer_manager.get_sorted_layers(reverse=True):
            if hasattr(layer, "on_input"):
                layer.on_input(event)
                break

    def update(self):
        self.layer_manager.update()

    def draw(self, screen):
        # Use the config's theme for background color
        bg_color = self.config.theme.get("background_color", (0, 0, 0))
        screen.fill(bg_color)
        self.layer_manager.draw(screen)

    def on_enter(self):
        """Called when the scene becomes active.
        (Text input is now centrally initialized in main().)
        """
        pass