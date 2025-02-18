"""
settings_scene.py - Basic Settings scene allowing theme modification with particle effects.
Version: 1.1.6
"""

from plugins.plugins import register_scene
import pygame
from scenes.base_scene import BaseScene
from core.config import Config
from managers.layer_manager import LayerManager
from managers.scene_manager import SceneManager

@register_scene("settings")
class SettingsScene(BaseScene):
    def __init__(self, scene_manager: SceneManager, font: pygame.font.Font, config: Config, layer_manager: LayerManager) -> None:
        """
        Initializes the SettingsScene with static configuration.
        Version: 1.1.6
        """
        extra_layers = []  # No extra layers for now.
        super().__init__("Settings", config, font, layer_manager, extra_layers)
        self.scene_manager = scene_manager
        self.last_theme_index = 0

    def refresh_scene(self) -> None:
        """
        Refreshes the current scene by clearing layers and re-entering the scene.
        """
        self.layer_manager.clear()
        self.on_enter()

    def on_enter(self) -> None:
        """
        Called when the SettingsScene becomes active.
        Populates the scene with universal layers, adds the ThemeSelectionLayer to allow
        modifying the active theme, and adds a particle effect layer if available.
        """
        super().on_enter()
        from layers.theme_selection_layer import ThemeSelectionLayer
        # Correct the order: first font, then config, then layer_manager, etc.
        theme_layer = ThemeSelectionLayer(
            self.font,
            self.config,
            self.layer_manager,
            parent_scene=self,
            refresh_callback=self.refresh_scene,
            back_callback=lambda: self.scene_manager.set_scene("menu"),
            initial_selected_index=getattr(self, "last_theme_index", 0)
        )
        self.layer_manager.add_layer(theme_layer)
        from plugins.plugins import layer_registry
        if "menu_particle_effect" in layer_registry:
            particle_cls = layer_registry["menu_particle_effect"]["class"]
            # Update the parameter order here as well
            particle_layer_instance = particle_cls(self.font, self.config, theme_layer)
            self.layer_manager.add_layer(particle_layer_instance)
        print("Entered Settings Scene with Theme Selection and Particle Effect")