# FileName: menu_scene.py
# version: 2.4
# Summary: Main menu scene built using a layered system with universal layers (imported from separate modules)
#          and an interactive menu layer.
# Tags: menu, scene, layers, retro, modular, UI

from base_scene import BaseScene
from universal_layers import get_universal_layers
from menu_layer import MenuLayer

class MenuScene(BaseScene):
    def __init__(self, scene_manager, font):
        super().__init__("Menu")
        self.scene_manager = scene_manager
        self.font = font
        # Define menu items as (label, scene_key) tuples.
        menu_items = [
            ("Test Scene", "test")
        ]
        # Combine universal layers with the interactive menu layer.
        self.layers = get_universal_layers(font) + [MenuLayer(scene_manager, font, menu_items)]
    
    def on_input(self, event):
        # Forward input events to the top-most layer that implements an on_input handler.
        for layer in sorted(self.layers, key=lambda l: l.z, reverse=True):
            if hasattr(layer, "on_input"):
                layer.on_input(event)
                break