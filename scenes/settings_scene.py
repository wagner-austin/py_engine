"""
scenes/settings_scene.py - Basic Settings scene allowing theme modification with particle effects.
Summary: Configures the Settings scene for mouse/touch-only input, enabling theme changes via on-screen buttons.
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
        settings_scene.py - Initializes the SettingsScene.
        Version: 1.1.6
        """
        extra_layers = []  # No extra layers for now.
        super().__init__("Settings", config, font, layer_manager, extra_layers)
        self.scene_manager = scene_manager

    def refresh_scene(self) -> None:
        """
        settings_scene.py - Refreshes the current scene by clearing layers and re-entering the scene.
        """
        self.layer_manager.clear()
        self.on_enter()

    def on_enter(self) -> None:
        """
        settings_scene.py - Called when the SettingsScene becomes active.
        Summary: Populates the scene with universal layers, adds the ThemeSelectionLayer for theme changes using mouse/touch input, and adds a particle effect layer if available.
        """
        super().on_enter()
        from layers.theme_selection_layer import ThemeSelectionLayer
        # Removed keyboard-based initial selected index; now using mouse/touch for navigation.
        theme_layer = ThemeSelectionLayer(
            self.font,
            self.config,
            self.layer_manager,
            parent_scene=self,
            refresh_callback=self.refresh_scene,
            back_callback=lambda: self.scene_manager.set_scene("menu")
        )
        self.layer_manager.add_layer(theme_layer)
        from plugins.plugins import layer_registry
        if "menu_particle_effect" in layer_registry:
            particle_cls = layer_registry["menu_particle_effect"]["class"]
            particle_layer_instance = particle_cls(self.font, self.config, theme_layer)
            self.layer_manager.add_layer(particle_layer_instance)
        print("Entered Settings Scene with Theme Selection and Particle Effect")

# End of scenes/settings_scene.py