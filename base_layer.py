"""
base_layer.py - Abstract base class for all layers.

Version: 1.0
"""

from abc import ABC, abstractmethod

class BaseLayer(ABC):
    z: int

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass