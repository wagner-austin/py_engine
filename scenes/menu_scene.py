# FileName: menu_scene.py
# version: 2.5 (modified)
# Summary: Main menu scene built using a layered system with universal layers and an interactive menu layer.
# Tags: menu, scene, layers, modular, UI

from base_scene import BaseScene
from universal_layers import get_universal_layers
from menu_layer import MenuLayer

class MenuScene(BaseScene):
    def __init__(self, scene_manager, font, config):
        super().__init__("Menu")
        self.scene_manager = scene_manager
        self.font = font
        self.config = config
        # Define menu items as (label, scene_key) tuples.
        menu_items = [
            ("Test Scene", "test")
        ]
        # Combine universal layers with the interactive menu layer.
        self.layers = get_universal_layers(font) + [MenuLayer(scene_manager, font, menu_items, config)]
    
    def on_input(self, event):
        # Forward input events using the helper method.
        self.forward_input(event)