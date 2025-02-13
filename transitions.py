"""
transitions.py - Plugin-based transitions for scene changes.

This file implements a very simple transition that overlays a black rectangle for a fade effect.
"""

import pygame
from abc import ABC, abstractmethod
from typing import Optional
from config import Config
from scenes.base_scene import BaseScene
from plugins import register_transition

# Global transition configuration parameters.
TRANSITION_CONFIG = {
    "default_duration": 1.0,             # Default transition duration in seconds
    "ease_function": lambda t: t,        # Linear easing function
}

# Active transition constant: change this value to select the active transition.
ACTIVE_TRANSITION = 'simple'

class Transition(ABC):
    def __init__(self, from_scene: BaseScene, to_scene: BaseScene, config: Config, duration: float = 1.0):
        """
        Initializes the transition.

        Parameters:
            from_scene: The outgoing scene.
            to_scene: The incoming scene.
            config: The global configuration (used for screen dimensions).
            duration: Transition duration in seconds.
        """
        self.from_scene = from_scene
        self.to_scene = to_scene
        self.config = config
        self.duration = duration
        self.elapsed = 0.0

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update the transition's progress."""
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the transition effect on the given screen."""
        pass

    def is_complete(self) -> bool:
        """Returns True when the transition has finished."""
        return self.elapsed >= self.duration

@register_transition('simple')
def create_simple_transition(from_scene: BaseScene, to_scene: BaseScene, config: Config, duration: float = 1.0) -> Transition:
    """
    Factory function for creating a simple fade transition.
    """
    return SimpleTransition(from_scene, to_scene, config, duration)

class SimpleTransition(Transition):
    def __init__(self, from_scene: BaseScene, to_scene: BaseScene, config: Config, duration: float = 1.0):
        """
        Creates a simple transition that overlays a black rectangle.
        The overlay starts fully opaque and fades out over the transition duration.
        """
        super().__init__(from_scene, to_scene, config, duration)
        self.fade_surface = pygame.Surface((config.screen_width, config.screen_height))
        self.fade_surface.fill((0, 0, 0))  # Black color

    def update(self, dt: float) -> None:
        self.elapsed += dt
        # Update the incoming scene so dynamic elements remain active.
        self.to_scene.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        # First, draw the live incoming scene.
        self.to_scene.draw(screen)
        # Compute fade progress: alpha decreases from 255 to 0.
        progress = min(self.elapsed / self.duration, 1.0)
        alpha = int((1 - progress) * 255)
        self.fade_surface.set_alpha(alpha)
        screen.blit(self.fade_surface, (0, 0))