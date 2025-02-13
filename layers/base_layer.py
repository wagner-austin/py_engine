"""
base_layer.py - Abstract base class for all layers.
"""

from abc import ABC, abstractmethod
import pygame

class BaseLayer(ABC):
    z: int
    persistent: bool = False  # New attribute to mark persistent layers

    def update(self, dt: float) -> None:
        # Default no-op update method. Subclasses can override this if dynamic behavior is needed.
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass