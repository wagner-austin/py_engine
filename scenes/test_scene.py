"""
test_scene.py - Test scene to confirm that the universal layered system and scene switching work.
Uses universal layers along with a custom TestLayer for scene-specific content.

Version: 1.0
"""

import pygame
from base_scene import BaseScene
from base_layer import BaseLayer  # Import BaseLayer for TestLayer
from layout_constants import LayerZIndex

class TestScene(BaseScene):
    """
    Test scene to confirm that the universal layered system and scene switching work.
    """

    def __init__(self, font, config, layer_manager, universal_factory):
        """
        Initializes the TestScene with a custom test layer.
        
        Parameters:
            font: The pygame font used for rendering.
            config: The configuration object containing screen dimensions and scale.
            layer_manager: The shared LayerManager for managing layers.
            universal_factory: The UniversalLayerFactory for creating universal layers.
        """
        extra_layers = [TestLayer(font, config)]
        super().__init__("Test Scene", config, font, layer_manager, universal_factory, extra_layers)

class TestLayer(BaseLayer):
    """
    A test layer that displays test scene text and animates a simple rotation.
    """

    def __init__(self, font, config):
        """
        Initializes the TestLayer with the provided font and configuration.
        
        Parameters:
            font: The pygame font used for rendering.
            config: The configuration object containing screen dimensions and scale.
        """
        self.z = LayerZIndex.TEST  # Drawn on top of universal layers.
        self.font = font
        self.config = config
        self.angle = 0  # For simple animation

    def update(self):
        """Updates the layer by incrementing the angle for animation."""
        self.angle = (self.angle + 2) % 360

    def draw(self, screen):
        """
        Draws the test scene text onto the provided screen.
        
        Parameters:
            screen: The pygame Surface on which to draw.
        """
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
        """
        Handles input events for the test layer.
        
        Parameters:
            event: A pygame event.
        """
        pass