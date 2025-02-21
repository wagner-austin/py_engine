"""
menu_scene.py - Main menu scene built using a layered system with an interactive menu layer.
Version: 2.7.5
Summary: Initializes the menu scene without manually adding directional controls.
         All directional input is handled globally by the SceneManager.
"""

from plugins.plugins import register_scene, layer_registry
from .base_scene import BaseScene
from core.config import Config
import pygame
from managers.layer_manager import LayerManager
from managers.scene_manager import SceneManager

@register_scene("menu")
class MenuScene(BaseScene):
    def __init__(self, scene_manager: SceneManager, font: pygame.font.Font, config: Config, layer_manager: LayerManager) -> None:
        """
        menu_scene.py - Initializes the MenuScene.
        Version: 2.7.5
        """
        super().__init__("Menu", config, font, layer_manager, extra_layers=[])
        self.scene_manager = scene_manager
        self.last_menu_index = 0
        self.menu_layer_instance = None

    def on_enter(self) -> None:
        """
        menu_scene.py - Called when the MenuScene becomes active.
        Version: 2.7.5
        Summary: Creates the menu layer and particle effect layer if available.
                 Does not add directional controls here since they are handled globally.
        """
        super().on_enter()
        if "menu_layer" in layer_registry:
            menu_cls = layer_registry["menu_layer"]["class"]
            menu_layer_instance = menu_cls(
                self.font,
                self.config,
                self.scene_manager,
                [("Play", "game_mode_selection"), ("Settings", "settings"), ("Quit", "quit")],
                initial_selected_index=self.last_menu_index
            )
            self.layer_manager.add_layer(menu_layer_instance)
            self.menu_layer_instance = menu_layer_instance
            if "menu_particle_effect" in layer_registry:
                particle_cls = layer_registry["menu_particle_effect"]["class"]
                particle_layer_instance = particle_cls(self.font, self.config, menu_layer_instance)
                self.layer_manager.add_layer(particle_layer_instance)
        print("Entered Menu Scene")