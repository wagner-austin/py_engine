"""
universal_layers.py - Aggregates universal layers for scenes by instantiating new layer objects based on
the current font and configuration. Caches static layers to avoid unnecessary reinitialization.

Version: 1.4 (updated caching strategy for granular invalidation)
"""

from typing import List, Dict, Tuple
import pygame
from .art_layers import StarArtLayer, BackGroundArtLayer
from .instruction_layer import InstructionLayer
from .border_layer import BorderLayer
from .effect_layers import RainEffectLayer
from .base_layer import BaseLayer
from config import Config
from plugins import effect_registry  # Import plugin effect registry

class UniversalLayerFactory:
    """
    Factory for universal layers.

    Caches static layers so that they are reinitialized only when configuration or font changes.
    The persistent rain effect is reinitialized if the configuration changes.
    This implementation now supports multiple configurations concurrently by only adding missing entries
    instead of clearing the entire cache.
    """

    def __init__(self) -> None:
        """
        Initializes the UniversalLayerFactory with empty caches.
        """
        # Cache for static layers keyed by (font id, scale, screen_width, screen_height)
        self._static_cache: Dict[Tuple[int, float, int, int], Dict[str, BaseLayer]] = {}
        # Cache for the rain effect layer keyed by (scale, screen_width, screen_height)
        self._rain_cache: Dict[Tuple[float, int, int], RainEffectLayer] = {}

    def _get_static_key(self, font: pygame.font.Font, config: Config) -> Tuple[int, float, int, int]:
        """
        Creates a cache key for static layers based on the provided font and configuration.
        
        Parameters:
            font: The pygame font used for rendering text.
            config: The configuration object.
        
        Returns:
            A tuple that uniquely identifies the static layer configuration.
        """
        return (id(font), config.scale, config.screen_width, config.screen_height)

    def _get_rain_key(self, config: Config) -> Tuple[float, int, int]:
        """
        Creates a cache key for the rain effect layer based on the provided configuration.
        
        Parameters:
            config: The configuration object.
        
        Returns:
            A tuple that uniquely identifies the rain effect configuration.
        """
        return (config.scale, config.screen_width, config.screen_height)

    def refresh_universal_layers(self, font: pygame.font.Font, config: Config) -> None:
        """
        Reinitializes cached layers if the configuration or font has changed.
        Implements a more granular cache invalidation strategy by adding new entries only when needed.

        Parameters:
            font: The pygame font to be used for rendering text.
            config: The configuration object containing theme and scaling information.
        """
        static_key = self._get_static_key(font, config)
        rain_key = self._get_rain_key(config)

        # Add a new static cache entry if one doesn't exist for the current key.
        if static_key not in self._static_cache:
            self._static_cache[static_key] = {
                "star": StarArtLayer(font, config),
                "background": BackGroundArtLayer(font, config),
                "instruction": InstructionLayer(font, config),
                "border": BorderLayer(config)
            }

        # Add a new rain cache entry if one doesn't exist for the current key.
        if rain_key not in self._rain_cache:
            self._rain_cache[rain_key] = RainEffectLayer(config)

    def get_universal_layers(self, font: pygame.font.Font, config: Config) -> List[BaseLayer]:
        """
        Returns a list of universal layer instances based on the current font and configuration.
        Cached static layers are returned if available, and plugin-registered effect layers are added.

        Parameters:
            font: The pygame font to be used for rendering text.
            config: The configuration object containing theme and scaling information.

        Returns:
            A list of universal layer instances.
        """
        self.refresh_universal_layers(font, config)
        static_key = self._get_static_key(font, config)
        rain_key = self._get_rain_key(config)
        cache = self._static_cache[static_key]
        layers = [
            cache["star"],
            self._rain_cache[rain_key],
            cache["background"],
            cache["instruction"],
            cache["border"],
        ]
        # Append any plugin-registered effect layers that are not already present.
        for key, effect_cls in effect_registry.items():
            instance = effect_cls(config)
            if not any(isinstance(layer, effect_cls) for layer in layers):
                layers.append(instance)
        return layers