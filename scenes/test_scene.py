"""  
test_scene.py - Test scene to confirm that the universal layered system and scene switching work.  
Uses a custom TestLayer for scene-specific content.  
Version: 1.0 (updated)  
"""  

from plugins.plugins import register_scene
import pygame
from .base_scene import BaseScene
from layers.base_layer import BaseLayer
from ui.layout_constants import LayerZIndex
from core.config import Config
from managers.layer_manager import LayerManager

#@register_scene("test")
class TestScene(BaseScene):
    """
    Test scene to confirm that the universal layered system and scene switching work.
    """
    def __init__(self, font: pygame.font.Font, config: Config, layer_manager: LayerManager) -> None:
        """
        Initializes the TestScene with a custom test layer.
          
        Parameters:
            font: The pygame font used for rendering.
            config: The configuration object.
            layer_manager: The shared LayerManager for managing layers.
        """
        extra_layers = [TestLayer(font, config)]
        super().__init__("Test Scene", config, font, layer_manager, extra_layers)

class TestLayer(BaseLayer):
    """
    A test layer that displays test scene text and animates a simple rotation.
    """
    def __init__(self, font: pygame.font.Font, config: Config) -> None:
        """
        Initializes the TestLayer with the provided font and configuration.
          
        Parameters:
            font: The pygame font used for rendering.
            config: The configuration object.
        """
        self.z: int = LayerZIndex.TEST
        self.font: pygame.font.Font = font
        self.config: Config = config
        self.angle: float = 0

    def update(self, dt: float) -> None:
        """
        Updates the layer by incrementing the angle for animation.
        """
        # Assume a rotation speed of 120 degrees per second.
        self.angle = (self.angle + 120 * dt) % 360

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the test scene text onto the provided screen.
          
        Parameters:
            screen: The pygame Surface on which to draw the test scene.
        """
        text: str = "TEST SCENE"
        text_surface: pygame.Surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(
                self.config.screen_width // 2,
                self.config.screen_height // 2,
            )
        )
        screen.blit(text_surface, text_rect)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Handles input events for the test layer.
          
        Parameters:
            event: A pygame event.
        """
        pass