# FileName: test_scene.py
# version: 1.1
# Summary: Test scene to confirm that the universal layered system and scene switching work.
#          Uses universal layers along with a custom TestLayer for scene-specific content.
# Tags: test, scene, layers, modular

import pygame
from base_scene import BaseScene
import config
from universal_layers import get_universal_layers

class TestScene(BaseScene):
    def __init__(self, scene_manager, font):
        super().__init__("Test Scene")
        self.scene_manager = scene_manager
        self.font = font
        # Combine universal layers with a TestLayer.
        self.layers = get_universal_layers(font) + [TestLayer(font)]

    def on_input(self, event):
        # Forward input events to the top-most layer that supports input.
        for layer in sorted(self.layers, key=lambda l: l.z, reverse=True):
            if hasattr(layer, "on_input"):
                layer.on_input(event)
                break

class TestLayer:
    def __init__(self, font):
        self.z = 6  # Drawn on top of universal layers.
        self.font = font
        self.angle = 0  # For simple animation

    def update(self):
        self.angle = (self.angle + 2) % 360

    def draw(self, screen):
        # Draw test scene text.
        text = "TEST SCENE"
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

    def on_input(self, event):
        # (Optional) Test-specific input handling.
        pass