# File: test_scene.py
# Version: 1.3 (modified)
# Summary: Test scene to confirm that the universal layered system and scene switching work.
#          Uses universal layers along with a custom TestLayer for scene-specific content.
# Tags: test, scene, layers, modular

import pygame
from base_scene import BaseScene
from base_layer import BaseLayer  # Import BaseLayer for TestLayer

class TestScene(BaseScene):
    def __init__(self, scene_manager, font, config):
        extra_layers = [TestLayer(font, config)]
        super().__init__("Test Scene", config, font, extra_layers)
        self.scene_manager = scene_manager

    def on_input(self, event):
        # Forward input events using the common helper.
        self.forward_input(event)

class TestLayer(BaseLayer):
    def __init__(self, font, config):
        self.z = 6  # Drawn on top of universal layers.
        self.font = font
        self.config = config
        self.angle = 0  # For simple animation

    def update(self):
        self.angle = (self.angle + 2) % 360

    def draw(self, screen):
        # Draw test scene text.
        text = "TEST SCENE"
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(
                self.config.screen_width // 2,
                self.config.screen_height // 2,
            )
        )
        screen.blit(text_surface, text_rect)

    def on_input(self, event):
        # (Optional) Test-specific input handling.
        pass