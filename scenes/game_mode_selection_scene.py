"""
game_mode_selection_scene.py - Scene for selecting a game mode using a plug-and-play particle effect.
Version: 1.0.2
"""

import pygame
from scenes.base_scene import BaseScene
from core.config import Config
from managers.layer_manager import LayerManager
from managers.scene_manager import SceneManager
from plugins.plugins import register_scene, layer_registry
from layers.game_mode_selection_layer import GameModeSelectionLayer

@register_scene("game_mode_selection")
class GameModeSelectionScene(BaseScene):
    def __init__(self, scene_manager: SceneManager, font: pygame.font.Font, config: Config, layer_manager: LayerManager) -> None:
        """
        GameModeSelectionScene - Initializes the scene for selecting a game mode.
        Version: 1.0.2
        """
        extra_layers = []
        super().__init__("GameModeSelection", config, font, layer_manager, extra_layers)
        self.scene_manager = scene_manager
        self.last_selection_index = 0

    def on_enter(self) -> None:
        """
        Called when the scene becomes active.
        Version: 1.0.2
        """
        super().on_enter()
        selection_layer = GameModeSelectionLayer(
            self.font,
            self.config,
            self.layer_manager,
            self.scene_manager,
            parent_scene=self,
            initial_selected_index=self.last_selection_index
        )
        self.layer_manager.add_layer(selection_layer)

        if "menu_particle_effect" in layer_registry:
            particle_cls = layer_registry["menu_particle_effect"]["class"]
            particle_layer_instance = particle_cls(self.font, self.config, selection_layer)
            self.layer_manager.add_layer(particle_layer_instance)

        print("Entered Game Mode Selection Scene")