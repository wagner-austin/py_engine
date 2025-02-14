"""
menu_scene.py
-------------
Main menu scene built using a layered system with an interactive menu layer.
Version: 2.7.0
"""

from plugins.plugins import register_scene, layer_registry
from .base_scene import BaseScene
from core.config import Config
import pygame
from managers.layer_manager import LayerManager
from managers.scene_manager import SceneManager

@register_scene("menu")
class MenuScene(BaseScene):
    """
    The MenuScene. It dynamically loads the 'menu_layer' plugin, and now also
    optionally loads a separate 'menu_particle_effect' plugin for particles.
    """

    def __init__(
        self,
        scene_manager: SceneManager,
        font: pygame.font.Font,
        config: Config,
        layer_manager: LayerManager
    ) -> None:
        """
        Initializes the MenuScene.

        Parameters:
            scene_manager (SceneManager): Manages scene transitions.
            font (pygame.font.Font): Font for rendering.
            config (Config): Global configuration object.
            layer_manager (LayerManager): The layer manager for this scene.
        """
        super().__init__("Menu", config, font, layer_manager, extra_layers=[])
        self.scene_manager = scene_manager

    def on_enter(self) -> None:
        """
        Called when the MenuScene becomes active.
        Loads the menu layer from the registry, and also tries to load the
        menu_particle_effect plugin layer to replicate the old particle behavior.
        """
        super().on_enter()

        # 1) Load "menu_layer" from registry if available.
        if "menu_layer" in layer_registry:
            menu_cls = layer_registry["menu_layer"]["class"]
            menu_layer_instance = menu_cls(
                self.scene_manager,
                self.font,
                [("Play", "play"), ("Settings", "settings"), ("Quit", "quit")],
                self.config
            )
            self.layer_manager.add_layer(menu_layer_instance)

            # 2) Also load "menu_particle_effect" from registry if available.
            if "menu_particle_effect" in layer_registry:
                particle_cls = layer_registry["menu_particle_effect"]["class"]
                # Pass the config and the newly-created menu_layer_instance.
                particle_layer_instance = particle_cls(self.config, menu_layer_instance)
                self.layer_manager.add_layer(particle_layer_instance)

        print("Entered Menu Scene")