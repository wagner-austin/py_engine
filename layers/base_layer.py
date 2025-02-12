"""
base_layer.py - Abstract base class for all layers.

Version: 1.1 (updated)
"""

from abc import ABC, abstractmethod
import pygame

class BaseLayer(ABC):
    z: int

    def update(self) -> None:
        # Default no-op update method. Subclasses can override this if dynamic behavior is needed.
        pass

    # Legacy abstract update method (now replaced by the default implementation)
    # @abstractmethod
    # def update(self) -> None:
    #     pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass