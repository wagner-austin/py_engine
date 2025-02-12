"""
layer_manager.py - Provides a LayerManager for managing scene layers.

Version: 1.2
"""

class LayerManager:
    def __init__(self, layers=None):
        self.layers = layers or []
        self._sorted_layers = []
        self._dirty = True  # Indicates that the sorted list needs to be refreshed.

    def _sort_layers(self):
        if self._dirty:
            self._sorted_layers = sorted(self.layers, key=lambda l: l.z)
            self._dirty = False

    def add_layer(self, layer):
        self.layers.append(layer)
        self._dirty = True

    def remove_layer(self, layer):
        if layer in self.layers:
            self.layers.remove(layer)
            self._dirty = True

    def mark_dirty(self):
        self._dirty = True

    def clear(self):
        """Clears all layers from the manager."""
        self.layers = []
        self._sorted_layers = []
        self._dirty = True

    def update(self):
        self._sort_layers()
        for layer in self._sorted_layers:
            layer.update()

    def draw(self, screen):
        self._sort_layers()
        for layer in self._sorted_layers:
            layer.draw(screen)

    def get_sorted_layers(self, reverse=False):
        self._sort_layers()
        return self._sorted_layers[::-1] if reverse else self._sorted_layers