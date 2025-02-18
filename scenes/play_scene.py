"""
play_scene.py - Dynamic Play scene supporting plug-and-play integration of different game modes.
Version: 1.2.3
Summary: Upgraded PlayScene to use a dedicated PlayAreaLayer for hosting game modes within a defined area.
"""

import pygame
from scenes.base_scene import BaseScene
from core.config import Config
from managers.layer_manager import LayerManager
from plugins.plugins import register_scene

@register_scene("play")
class PlayScene(BaseScene):
    def __init__(self, font: pygame.font.Font, config: Config, layer_manager: LayerManager) -> None:
        """
        play_scene.py - Initializes the PlayScene.
        Version: 1.2.3
        Summary: Uses the regular scene and layer manager, with a dedicated play area layer for game modes.
        """
        extra_layers = []  # No extra layers initially.
        super().__init__("Play", config, font, layer_manager, extra_layers)

    def on_enter(self) -> None:
        """
        Called when the PlayScene becomes active.
        Version: 1.2.3
        Summary: Clears the scene and adds a dedicated PlayAreaLayer to host game modes.
        """
        super().on_enter()
        from layers.play_area_layer import PlayAreaLayer
        # Use the selected game mode from the configuration rather than always "default"
        play_area_layer = PlayAreaLayer(self.font, self.config, self.layer_manager, game_key=self.config.selected_game_mode)
        self.layer_manager.add_layer(play_area_layer)
        print("Entered Play Scene with dedicated play area layer.")