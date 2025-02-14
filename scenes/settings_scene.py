"""  
settings_scene.py - Basic Settings scene.  
Version: 1.1.1  
"""  

from plugins.plugins import register_scene
import pygame
from scenes.base_scene import BaseScene
from core.config import Config
from managers.layer_manager import LayerManager

@register_scene("settings")
class SettingsScene(BaseScene):
    def __init__(self, font: pygame.font.Font, config: Config, layer_manager: LayerManager) -> None:
        """
        Initializes the SettingsScene with static configuration.
          
        Parameters:
            font (pygame.font.Font): The font used for rendering.
            config (Config): The global configuration object.
            layer_manager (LayerManager): The shared LayerManager.
        """
        extra_layers = []  # No extra layers for now.
        super().__init__("Settings", config, font, layer_manager, extra_layers)

    def on_enter(self) -> None:
        """
        Called when the SettingsScene becomes active. Performs dynamic initialization actions.
        """
        super().on_enter()
        print("Entered Settings Scene")