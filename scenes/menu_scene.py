"""
menu_scene.py - Main menu scene built using a layered system with universal layers and an interactive menu layer.

Version: 2.6
"""

from base_scene import BaseScene
from menu_layer import MenuLayer

class MenuScene(BaseScene):
    def __init__(self, scene_manager, font, config, layer_manager, universal_factory):
        extra_layers = [MenuLayer(scene_manager, font, [("Test Scene", "test")], config)]
        super().__init__("Menu", config, font, layer_manager, universal_factory, extra_layers)
        self.scene_manager = scene_manager