"""
layer_manager.py - Provides a LayerManager for managing scene layers.

Version: 1.2 (updated with refined type hints)
"""

from typing import List
import pygame
from layers.base_layer import BaseLayer

class LayerManager:
    def __init__(self, layers: List[BaseLayer] = None) -> None:
        self.layers: List[BaseLayer] = layers or []
        self._sorted_layers: List[BaseLayer] = []
        self._dirty: bool = True

    def _sort_layers(self) -> None:
        if self._dirty:
            self._sorted_layers = sorted(self.layers, key=lambda l: l.z)
            self._dirty = False

    def add_layer(self, layer: BaseLayer) -> None:
        self.layers.append(layer)
        self._dirty = True

    def remove_layer(self, layer: BaseLayer) -> None:
        if layer in self.layers:
            self.layers.remove(layer)
            self._dirty = True

    def mark_dirty(self) -> None:
        self._dirty = True

    def clear(self) -> None:
        """Clears all layers from the manager."""
        self.layers = []
        self._sorted_layers = []
        self._dirty = True

    def update(self) -> None:
        self._sort_layers()
        for layer in self._sorted_layers:
            layer.update()

    def draw(self, screen: pygame.Surface) -> None:
        self._sort_layers()
        for layer in self._sorted_layers:
            layer.draw(screen)

    def get_sorted_layers(self, reverse: bool = False) -> List[BaseLayer]:
        self._sort_layers()
        return self._sorted_layers[::-1] if reverse else self._sorted_layers