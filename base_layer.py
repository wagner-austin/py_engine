# File: base_layer.py
# Version: 1.0 (added)
# Summary: Abstract base class for all layers. Enforces implementation of update() and draw(screen).
# Tags: layers, base, abstraction

from abc import ABC, abstractmethod


class BaseLayer(ABC):
    z: int

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass