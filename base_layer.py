"""
base_layer.py - Abstract base class for all layers.

Version: 1.0
"""

from abc import ABC, abstractmethod
import pygame

class BaseLayer(ABC):
    z: int

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass