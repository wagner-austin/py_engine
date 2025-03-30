"""
scenes/menu_scene.py - Main menu scene built using a layered system with an interactive menu layer.
Summary: Initializes the menu scene with mouse/touch-based navigation and handles directional input for menu selection.
Version: 2.7.5
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
        scenes/menu_scene.py - Initializes the MenuScene.
        Version: 2.7.5
        """
        super().__init__("Menu", config, font, layer_manager, extra_layers=[])
        self.scene_manager = scene_manager
        self.menu_layer_instance = None

    def on_enter(self) -> None:
        """
        scenes/menu_scene.py - Called when the MenuScene becomes active.
        Version: 2.7.5
        Summary: Creates the menu layer and particle effect layer if available using mouse/touch input.
        """
        super().on_enter()
        if "menu_layer" in layer_registry:
            menu_cls = layer_registry["menu_layer"]["class"]
            # Removed keyboard-based initial selected index for mouse-only navigation.
            menu_layer_instance = menu_cls(
                self.font,
                self.config,
                self.scene_manager,
                [("Play", "game_mode_selection"), ("Settings", "settings"), ("Quit", "quit")]
            )
            self.layer_manager.add_layer(menu_layer_instance)
            self.menu_layer_instance = menu_layer_instance
            if "menu_particle_effect" in layer_registry:
                particle_cls = layer_registry["menu_particle_effect"]["class"]
                particle_layer_instance = particle_cls(self.font, self.config, menu_layer_instance)
                self.layer_manager.add_layer(particle_layer_instance)
        print("Entered Menu Scene")

    def on_directional_input(self, direction: str, pressed: bool) -> None:
        """
        scenes/menu_scene.py - Handles directional input to update the menu selection.
        Version: 2.7.5
        Summary: Updates the menu layer's selected_index based on 'up' or 'down' input.
        """
        if not pressed or self.menu_layer_instance is None:
            return

        # Retrieve the current selected index and total buttons count.
        current_index = self.menu_layer_instance.selected_index
        total_buttons = len(self.menu_layer_instance.buttons)
        if total_buttons == 0:
            return

        if direction.lower() == "up":
            self.menu_layer_instance.selected_index = (current_index - 1) % total_buttons
        elif direction.lower() == "down":
            self.menu_layer_instance.selected_index = (current_index + 1) % total_buttons

# End of scenes/menu_scene.py