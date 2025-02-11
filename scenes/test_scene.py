# FileName: test_scene.py
# version: 1.2 (modified)
# Summary: Test scene to confirm that the universal layered system and scene switching work.
#          Uses universal layers along with a custom TestLayer for scene-specific content.
# Tags: test, scene, layers, modular

import pygame
from base_scene import BaseScene
from universal_layers import get_universal_layers

class TestScene(BaseScene):
    def __init__(self, scene_manager, font, config):
        super().__init__("Test Scene")
        self.scene_manager = scene_manager
        self.font = font
        self.config = config
        # Combine universal layers with a TestLayer.
        self.layers = get_universal_layers(font) + [TestLayer(font, config)]
    
    def on_input(self, event):
        # Forward input events using the common helper.
        self.forward_input(event)

class TestLayer:
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
        text_rect = text_surface.get_rect(center=(self.config.screen_width // 2, self.config.screen_height // 2))
        screen.blit(text_surface, text_rect)

    def on_input(self, event):
        # (Optional) Test-specific input handling.
        pass