"""
layer_manager.py - Provides a LayerManager for managing scene layers.
Version: 1.1.0
"""

from typing import List
import pygame
from layers.base_layer import BaseLayer

class LayerManager:
    def __init__(self, layers: List[BaseLayer] = None) -> None:
        """
        Initializes the LayerManager with an optional list of layers.

        Parameters:
            layers (List[BaseLayer], optional): Initial list of layers. Defaults to None.
        """
        self.layers: List[BaseLayer] = layers or []
        self._sorted_layers: List[BaseLayer] = []
        self._dirty: bool = True

    def _sort_layers(self) -> None:
        """
        Sorts layers based on their z-index if marked as dirty.
        """
        if self._dirty:
            self._sorted_layers = sorted(self.layers, key=lambda l: l.z)
            self._dirty = False

    def add_layer(self, layer: BaseLayer) -> None:
        """
        Adds a layer to the manager.

        Parameters:
            layer (BaseLayer): The layer to add.
        """
        self.layers.append(layer)
        self._dirty = True

    def remove_layer(self, layer: BaseLayer) -> None:
        """
        Removes a layer from the manager if it exists.

        Parameters:
            layer (BaseLayer): The layer to remove.
        """
        if layer in self.layers:
            self.layers.remove(layer)
            self._dirty = True

    def mark_dirty(self) -> None:
        """
        Marks the layer list as dirty to force re-sorting.
        """
        self._dirty = True

    def clear(self) -> None:
        """
        Clears all non‑persistent layers from the manager.
        Persistent layers remain.
        """
        self.layers = [layer for layer in self.layers if getattr(layer, "persistent", False)]
        self._sorted_layers = []
        self._dirty = True

    def update(self, dt: float) -> None:
        """
        Updates all layers.

        Parameters:
            dt (float): Delta time in seconds.
        """
        self._sort_layers()
        for layer in self._sorted_layers:
            layer.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws all layers onto the provided screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the layers.
        """
        self._sort_layers()
        for layer in self._sorted_layers:
            layer.draw(screen)

    def get_sorted_layers(self, reverse: bool = False) -> List[BaseLayer]:
        """
        Returns the sorted list of layers.

        Parameters:
            reverse (bool, optional): Whether to reverse the order. Defaults to False.

        Returns:
            List[BaseLayer]: The sorted list of layers.
        """
        self._sort_layers()
        return self._sorted_layers[::-1] if reverse else self._sorted_layers