"""
play_scene.py - Basic Play scene.
Version: 1.0 (updated: removed duplicate on_input)
"""

from plugins import register_scene
import pygame
from scenes.base_scene import BaseScene
from config import Config
from managers.layer_manager import LayerManager
from layers.universal_layers import UniversalLayerFactory

@register_scene("play")
class PlayScene(BaseScene):
    def __init__(self, font: pygame.font.Font, config: Config, layer_manager: LayerManager, universal_factory: UniversalLayerFactory) -> None:
        """
        Initializes the PlayScene.

        Parameters:
            font: The pygame font used for rendering.
            config: The configuration object.
            layer_manager: The shared LayerManager.
            universal_factory: The universal layer factory.
        """
        extra_layers = []  # No extra layers for now.
        super().__init__("Play", config, font, layer_manager, universal_factory, extra_layers)

    def on_enter(self) -> None:
        """
        Called when the scene becomes active.
        """
        print("Entered Play Scene")