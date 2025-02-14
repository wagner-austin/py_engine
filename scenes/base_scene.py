"""
base_scene.py - Base scene class providing common functionality and input handling for all scenes.
Version: 1.2.3 (Updated with debug print statements for layer registration, 
                now modified to skip re‑instantiating persistent layers)
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
        print(f"BaseScene '{self.name}' initialized with font: {self.font} and config: {self.config}")

    def populate_layers(self) -> None:
        """
        Clears non‑persistent layers and repopulates the layer manager with universal layers and scene‑specific layers.

        Universal layers are fetched from the unified layer_registry by filtering on the categories:
        "background", "effect", and "foreground". They are instantiated (using a constructor of either
        (font, config), (config), or no arguments) and added to the layer manager.

        If a layer of a certain class is already in the layer manager (and is persistent),
        we skip re‑instantiating it, to avoid duplicates.
        """
        # Remove all non‑persistent layers first
        self.layer_manager.clear()
        print("Populating universal layers from registry...")
        print("Layer registry contents:", layer_registry)

        # Add universal layers from the plugin registry
        for key, info in layer_registry.items():
            if info["category"] in ["background", "effect", "foreground"]:
                layer_cls = info["class"]

                # If a layer of this class is already in self.layer_manager (persistent),
                # skip re-adding it to avoid duplicates
                if any(isinstance(layer, layer_cls) for layer in self.layer_manager.layers):
                    continue

                print(f"Adding registered layer: '{key}' with category: '{info['category']}'")

                # Attempt to instantiate with (font, config), then (config), then no args
                try:
                    layer_instance = layer_cls(self.font, self.config)
                except TypeError:
                    try:
                        layer_instance = layer_cls(self.config)
                    except TypeError:
                        layer_instance = layer_cls()
                self.layer_manager.add_layer(layer_instance)

        # Then add scene‑specific extra layers (if any).
        if self.extra_layers:
            print("Adding scene-specific extra layers...")
        for layer in self.extra_layers:
            self.layer_manager.add_layer(layer)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Dispatches the event to the scene's input handler.
  
        Parameters:
            event (pygame.event.Event): The event to be handled.
        """
        self.on_input(event)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Default input handling: Forwards the event to the highest z‑index layer that implements on_input.
        Subclasses may override this method for scene‑specific input handling.
  
        Parameters:
            event (pygame.event.Event): The event to be processed.
        """
        self.forward_input(event)

    def forward_input(self, event: pygame.event.Event) -> None:
        """
        Forwards the input event to the highest z‑index layer that implements on_input.
  
        Parameters:
            event (pygame.event.Event): The event to be forwarded.
        """
        for layer in self.layer_manager.get_sorted_layers(reverse=True):
            if hasattr(layer, "on_input"):
                layer.on_input(event)
                break

    def update(self, dt: float) -> None:
        """
        Updates the scene by updating the layer manager.
  
        Parameters:
            dt (float): Delta time in seconds.
        """
        self.layer_manager.update(dt)

    def draw_dynamic(self, screen: pygame.Surface) -> None:
        """
        Draws only the non‑persistent (dynamic) layers onto the provided screen.
  
        Parameters:
            screen (pygame.Surface): The surface on which to draw the dynamic layers.
        """
        for layer in self.layer_manager.get_sorted_layers():
            if not getattr(layer, "persistent", False):
                layer.draw(screen)

    def draw_persistent(self, screen: pygame.Surface) -> None:
        """
        Draws only the persistent layers onto the provided screen.
  
        Parameters:
            screen (pygame.Surface): The surface on which to draw the persistent layers.
        """
        for layer in self.layer_manager.get_sorted_layers():
            if getattr(layer, "persistent", False):
                layer.draw(screen)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the scene onto the provided screen by drawing dynamic layers first,
        then persistent layers on top.
  
        Parameters:
            screen (pygame.Surface): The pygame Surface on which to draw the scene.
        """
        bg_color = self.config.theme.background_color
        screen.fill(bg_color)
        self.draw_dynamic(screen)
        self.draw_persistent(screen)

    def on_enter(self) -> None:
        """
        Called when the scene becomes active.
  
        This dynamic hook repopulates the layers by calling populate_layers().
        """
        print(f"Scene on_enter() called for '{self.name}'")
        self.populate_layers()