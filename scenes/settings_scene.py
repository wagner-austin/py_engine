"""
settings_scene.py - Basic Settings scene allowing theme modification with particle effects.
Version: 1.1.4
"""

from plugins.plugins import register_scene
import pygame
from scenes.base_scene import BaseScene
from core.config import Config
from managers.layer_manager import LayerManager
from managers.scene_manager import SceneManager  # Import SceneManager for scene transitions

@register_scene("settings")
class SettingsScene(BaseScene):
    def __init__(self, scene_manager: SceneManager, font: pygame.font.Font, config: Config, layer_manager: LayerManager) -> None:
        """
        Initializes the SettingsScene with static configuration.

        Parameters:  
            scene_manager (SceneManager): The scene manager for handling scene transitions.
            font (pygame.font.Font): The font used for rendering.
            config (Config): The global configuration object.
            layer_manager (LayerManager): The shared LayerManager.
        """
        extra_layers = []  # No extra layers for now.
        super().__init__("Settings", config, font, layer_manager, extra_layers)
        self.scene_manager = scene_manager

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
        # Create the theme selection layer with a refresh callback and a back callback to return to the main menu.
        theme_layer = ThemeSelectionLayer(
            self.config,
            self.font,
            self.layer_manager,
            refresh_callback=self.refresh_scene,
            back_callback=lambda: self.scene_manager.set_scene("menu")
        )
        self.layer_manager.add_layer(theme_layer)
        # Add particle effect layer if available.
        from plugins.plugins import layer_registry
        if "menu_particle_effect" in layer_registry:
            particle_cls = layer_registry["menu_particle_effect"]["class"]
            # Pass the theme_layer as the reference for the particle effect.
            particle_layer_instance = particle_cls(self.config, theme_layer)
            self.layer_manager.add_layer(particle_layer_instance)
        print("Entered Settings Scene with Theme Selection and Particle Effect")