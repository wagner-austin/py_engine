"""  
play_scene.py - Basic Play scene.  
Version: 1.1.1  
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
        Initializes the PlayScene with static configuration.
          
        Parameters:
            font (pygame.font.Font): The font used for rendering.
            config (Config): The global configuration object.
            layer_manager (LayerManager): The shared LayerManager.
        """
        extra_layers = []  # No extra layers for now.
        super().__init__("Play", config, font, layer_manager, extra_layers)

    def on_enter(self) -> None:
        """
        Called when the PlayScene becomes active. Performs dynamic initialization actions.
        """
        super().on_enter()
        print("Entered Play Scene")