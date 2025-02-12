# File: menu_scene.py
# Version: 2.6 (modified)
# Summary: Main menu scene built using a layered system with universal layers and an interactive menu layer.
# Tags: menu, scene, layers, modular, UI

from base_scene import BaseScene
from menu_layer import MenuLayer

class MenuScene(BaseScene):
    def __init__(self, scene_manager, font, config):
        extra_layers = [MenuLayer(scene_manager, font, [("Test Scene", "test")], config)]
        super().__init__("Menu", config, font, extra_layers)
        self.scene_manager = scene_manager

    def on_input(self, event):
        # Forward input events using the helper method.
        self.forward_input(event)