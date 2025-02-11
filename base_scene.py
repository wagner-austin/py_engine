# FileName: base_scene.py
# version: 2.2 (modified)
# Summary: Base scene class providing common functionality and input handling for all scenes.
#          Supports a layered system and clears the screen before drawing.
# Tags: scene, base, modular, input handling

import pygame
import config  # Now using config.config

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
        """Override in subclasses for scene-specific input handling.
           Legacy duplicate implementation below is now replaced:
        
        # for layer in sorted(self.layers, key=lambda l: l.z, reverse=True):
        #     if hasattr(layer, "on_input"):
        #         layer.on_input(event)
        #         break
        """
        self.forward_input(event)

    def forward_input(self, event):
        """
        Forwards the input event to the highest z-index layer that implements on_input.
        """
        for layer in sorted(self.layers, key=lambda l: l.z, reverse=True):
            if hasattr(layer, "on_input"):
                layer.on_input(event)
                break

    def update(self):
        # Update all layers.
        for layer in self.layers:
            if hasattr(layer, "update"):
                layer.update()

    def draw(self, screen):
        # Clear the screen using a scene-specific background if set, else use the universal background.
        bg_color = getattr(self, "background_color", config.config.theme["background_color"])
        screen.fill(bg_color)
        # Draw layers sorted by their z-index.
        for layer in sorted(self.layers, key=lambda l: l.z):
            if hasattr(layer, "draw"):
                layer.draw(screen)

    def on_enter(self):
        """Called when the scene becomes active."""
        pygame.key.start_text_input()