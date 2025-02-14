"""
universal_layers.py
Version: 1.1 (Updated)
Summary: Aggregates universal layers for scenes by instantiating new layer objects
         based on the current font and configuration. This factory now reads from the unified
         layer_registry (populated by the register_layer decorator) and instantiates layers
         in the order: background, then effect, then foreground.
         New universal layer modules placed in the designated packages will be imported automatically.
"""

import inspect
from typing import List
import pygame
from layers.base_layer import BaseLayer
from config import Config
from plugins import layer_registry  # Updated: use unified layer_registry instead of universal_layer_registry

class UniversalLayerFactory:
    """
    Factory for universal layers.

    This factory reads from the layer_registry to instantiate universal layers.
    The get_universal_layers(font, config) method returns a list of universal layers ordered by category:
      - "background": e.g., StarArtLayer, BackGroundArtLayer.
      - "effect": e.g., RainEffectLayer, SnowEffectLayer.
      - "foreground": e.g., InstructionLayer, BorderLayer.
    """
    
    def get_universal_layers(self, font: pygame.font.Font, config: Config) -> List[BaseLayer]:
        """
        Instantiates and returns a list of universal layers based on the current font and configuration.

        The universal layers are instantiated in order of category: background, effect, then foreground.

        Parameters:
            font (pygame.font.Font): The font used to render text in the layers.
            config (Config): The configuration object containing screen dimensions and scaling.

        Returns:
            List[BaseLayer]: A list of universal layer instances.
        """
        layers: List[BaseLayer] = []
        # Define the desired order for universal layers.
        category_order = ["background", "effect", "foreground"]
        for category in category_order:
            for key, reg in layer_registry.items():
                if reg["category"] == category:
                    cls = reg["class"]
                    sig = inspect.signature(cls.__init__)
                    # Skip the 'self' parameter
                    parameters = list(sig.parameters.values())[1:]
                    # Standardize constructor signature: prefer (font, config)
                    if len(parameters) >= 2:
                        instance = cls(font, config)
                    elif len(parameters) == 1:
                        instance = cls(config)
                    else:
                        instance = cls()
                    layers.append(instance)
        return layers