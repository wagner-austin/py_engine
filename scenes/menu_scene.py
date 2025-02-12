"""
menu_scene.py - Main menu scene built using a layered system with universal layers and an interactive menu layer.

Version: 2.6
"""

from base_scene import BaseScene
from menu_layer import MenuLayer
from typing import Any
from config import Config
import pygame
from layer_manager import LayerManager
from universal_layers import UniversalLayerFactory
from scene_manager import SceneManager

class MenuScene(BaseScene):
    def __init__(self, scene_manager: SceneManager, font: pygame.font.Font, config: Config, layer_manager: LayerManager, universal_factory: UniversalLayerFactory) -> None:
        """
        Initializes the MenuScene with an interactive menu layer.
        
        Parameters:
            scene_manager: The manager responsible for scene transitions.
            font: The pygame font used for rendering.
            config: The configuration object.
            layer_manager: The shared layer manager.
            universal_factory: The universal layer factory.
        """
        extra_layers = [MenuLayer(scene_manager, font, [("Test Scene", "test")], config)]
        super().__init__("Menu", config, font, layer_manager, universal_factory, extra_layers)
        self.scene_manager = scene_manager