"""
menu_scene.py - Main menu scene built using a layered system with universal layers and an interactive menu layer.

Version: 2.6 (modified for new home scene options)
"""

from plugins import register_scene
from .base_scene import BaseScene
from layers.menu_layer import MenuLayer
from config import Config
import pygame
from managers.layer_manager import LayerManager
from layers.universal_layers import UniversalLayerFactory
from managers.scene_manager import SceneManager

@register_scene("menu")
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
        # Updated menu options: Play, Settings, Quit
        extra_layers = [MenuLayer(scene_manager, font, [("Play", "play"), ("Settings", "settings"), ("Quit", "quit")], config)]
        super().__init__("Menu", config, font, layer_manager, universal_factory, extra_layers)
        self.scene_manager = scene_manager