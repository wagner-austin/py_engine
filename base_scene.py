# FileName: base_scene.py
# version: 2.2
# Summary: Base scene class providing common functionality and input handling for all scenes.
#          Supports a layered system and clears the screen before drawing.
# Tags: scene, base, modular, input handling

import pygame
import config

class BaseScene:
    def __init__(self, name):
        self.name = name
        # List of layers (each must have a 'z' attribute and update/draw methods).
        self.layers = []

    def handle_event(self, event):
        # Common input: restart text input on mouse click.
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.key.start_text_input()
        # Delegate scene-specific input.
        self.on_input(event)

    def on_input(self, event):
        """Override in subclasses for scene-specific input handling."""
        pass

    def update(self):
        # Update all layers.
        for layer in self.layers:
            if hasattr(layer, "update"):
                layer.update()

    def draw(self, screen):
        # Clear the screen using a scene-specific background if set, else use the universal background.
        bg_color = getattr(self, "background_color", config.THEME["background_color"])
        screen.fill(bg_color)
        # Draw layers sorted by their z-index.
        for layer in sorted(self.layers, key=lambda l: l.z):
            if hasattr(layer, "draw"):
                layer.draw(screen)

    def on_enter(self):
        """Called when the scene becomes active."""
        pygame.key.start_text_input()