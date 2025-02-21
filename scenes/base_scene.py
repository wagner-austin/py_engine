"""
base_scene.py - Base scene class providing common functionality and input handling for all scenes.
Version: 1.2.3 (Updated to propagate unhandled input events to lower layers)
"""

import pygame  
from typing import List, Optional  
from core.config import Config  
from managers.layer_manager import LayerManager  
from layers.base_layer import BaseLayer  # For type hinting extra_layers  
from plugins.plugins import layer_registry  # Import the unified layer registry  
  
class BaseScene:  
    def __init__(  
        self,  
        name: str,  
        config: Config,  
        font: pygame.font.Font,  
        layer_manager: LayerManager,  
        extra_layers: Optional[List[BaseLayer]] = None,  
    ) -> None:  
        """  
        Initializes the BaseScene with static configuration.  
    
        Parameters:  
            name (str): The name of the scene.  
            config (Config): The global configuration object.  
            font (pygame.font.Font): The font used for rendering.  
            layer_manager (LayerManager): The layer manager instance.  
            extra_layers (Optional[List[BaseLayer]]): Additional scene-specific layers.  
        """  
        self.name: str = name  
        self.config: Config = config  
        self.font: pygame.font.Font = font  
        self.layer_manager: LayerManager = layer_manager  
        self.extra_layers: List[BaseLayer] = extra_layers or []  
  
    def populate_layers(self) -> None:  
        """  
        Clears non‑persistent layers and repopulates the layer manager with universal layers and scene‑specific layers.  
        """  
        self.layer_manager.clear()  
        for key, info in layer_registry.items():  
            if info["category"] in ["background", "effect", "foreground"]:  
                layer_cls = info["class"]  
                if any(isinstance(layer, layer_cls) for layer in self.layer_manager.layers):  
                    continue  
                try:  
                    layer_instance = layer_cls(self.font, self.config)  
                except TypeError:  
                    try:  
                        layer_instance = layer_cls(self.config)  
                    except TypeError:  
                        layer_instance = layer_cls()  
                self.layer_manager.add_layer(layer_instance)  
        if self.extra_layers:  
            for layer in self.extra_layers:  
                self.layer_manager.add_layer(layer)  
  
    def handle_event(self, event: pygame.event.Event) -> None:  
        """  
        Dispatches the event to the scene's input handler.  
        """  
        self.on_input(event)  
  
    def on_input(self, event: pygame.event.Event) -> None:  
        """  
        Default input handling: Forwards the event to the highest z‑index layer that implements on_input.  
        """  
        self.forward_input(event)  
  
    def forward_input(self, event: pygame.event.Event) -> None:  
        """  
        Forwards the input event to layers in order of descending z-index until one consumes the event.  
        Each layer’s on_input should return True if the event is handled.
        """  
        for layer in self.layer_manager.get_sorted_layers(reverse=True):  
            if hasattr(layer, "on_input"):  
                if layer.on_input(event):  
                    break  
  
    def update(self, dt: float) -> None:  
        """  
        Updates the scene by updating the layer manager.  
        """  
        self.layer_manager.update(dt)  
  
    def draw_dynamic(self, screen: pygame.Surface) -> None:  
        """  
        Draws only the non‑persistent (dynamic) layers onto the provided screen.  
        """  
        for layer in self.layer_manager.get_sorted_layers():  
            if not getattr(layer, "persistent", False):  
                layer.draw(screen)  
  
    def draw_persistent(self, screen: pygame.Surface) -> None:  
        """  
        Draws only the persistent layers onto the provided screen.  
        """  
        for layer in self.layer_manager.get_sorted_layers():  
            if getattr(layer, "persistent", False):  
                layer.draw(screen)  
  
    def draw(self, screen: pygame.Surface) -> None:  
        """  
        Draws the scene onto the provided screen by drawing dynamic layers first, then persistent layers on top.  
        """  
        bg_color = self.config.theme.background_color  
        screen.fill(bg_color)  
        self.draw_dynamic(screen)  
        self.draw_persistent(screen)  
  
    def on_enter(self) -> None:  
        """  
        Called when the scene becomes active.  
        Repopulates the layers.  
        """  
        self.populate_layers()