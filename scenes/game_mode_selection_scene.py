"""
game_mode_selection_scene.py - Scene for selecting a game mode using a plug-and-play particle effect.
Version: 1.0.2
Summary: Provides a dedicated scene where the user can choose a game mode from available options.
         Integrates a plug-and-play particle effect layer if available and recalls the last selected option.
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
        Summary: Uses a dedicated selection layer for game modes, integrates plug-and-play particle effects,
                 and remembers the last selected option.
        """
        extra_layers = []  # No extra layers initially.
        super().__init__("GameModeSelection", config, font, layer_manager, extra_layers)
        self.scene_manager = scene_manager
        self.last_selection_index = 0

    def on_enter(self) -> None:
        """
        Called when the scene becomes active.
        Version: 1.0.2
        Summary: Clears layers and adds the GameModeSelectionLayer (passing itself as parent) along with an optional particle effect layer.
        """
        super().on_enter()
        selection_layer = GameModeSelectionLayer(
            self.config,
            self.font,
            self.layer_manager,
            self.scene_manager,
            parent_scene=self,
            initial_selected_index=self.last_selection_index
        )
        self.layer_manager.add_layer(selection_layer)

        # Integrate plug-and-play particle effect if available
        if "menu_particle_effect" in layer_registry:
            particle_cls = layer_registry["menu_particle_effect"]["class"]
            particle_layer_instance = particle_cls(self.config, selection_layer)
            self.layer_manager.add_layer(particle_layer_instance)

        print("Entered Game Mode Selection Scene")