# FileName: layer_manager.py
# version: 1.0
# Summary: Provides a LayerManager for managing scene layers. It sorts, updates, and draws layers in order.
# Tags: layers, manager, modular

class LayerManager:
    def __init__(self, layers=None):
        self.layers = layers or []

    def add_layer(self, layer):
        self.layers.append(layer)

    def remove_layer(self, layer):
        if layer in self.layers:
            self.layers.remove(layer)

    def update(self):
        for layer in sorted(self.layers, key=lambda l: l.z):
            if hasattr(layer, "update"):
                layer.update()

    def draw(self, screen):
        for layer in sorted(self.layers, key=lambda l: l.z):
            if hasattr(layer, "draw"):
                layer.draw(screen)
