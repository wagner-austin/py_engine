"""
menu_scene.py - Main menu scene built using a layered system with an interactive menu layer.
Version: 2.6.2 (Updated to load scene‑specific layers from the registry)
"""

from plugins import register_scene, layer_registry
from .base_scene import BaseScene
from config import Config
import pygame
from managers.layer_manager import LayerManager
from managers.scene_manager import SceneManager

# Option 2 for scene‑specific layer:
# In your MenuLayer file (e.g. layers/menu_layer.py) decorate with:
# @register_layer("menu_layer", category="menu_only")
# If you prefer Option 1 (manual creation), simply don't decorate MenuLayer and create it in extra_layers.

@register_scene("menu")
class MenuScene(BaseScene):
    def __init__(self, scene_manager: SceneManager, font: pygame.font.Font, config: Config, layer_manager: LayerManager) -> None:
        # Do not include the menu layer in extra_layers if you want to load it from the registry.
        super().__init__("Menu", config, font, layer_manager, extra_layers=[])
        self.scene_manager = scene_manager

    def on_enter(self) -> None:
        super().on_enter()
        # Load scene-specific "menu_only" layer from registry if available.
        # (This assumes you have decorated MenuLayer with @register_layer("menu_layer", category="menu_only"))
        if "menu_layer" in layer_registry:
            menu_cls = layer_registry["menu_layer"]["class"]
            # Instantiate MenuLayer using its constructor.
            # For example, if MenuLayer expects (scene_manager, font, menu_items, config):
            menu_layer_instance = menu_cls(
                self.scene_manager,
                self.font,
                [("Play", "play"), ("Settings", "settings"), ("Quit", "quit")],
                self.config
            )
            self.layer_manager.add_layer(menu_layer_instance)
        print("Entered Menu Scene")