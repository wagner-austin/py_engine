"""
transitions/transitions.py - Plugin-based transitions for scene changes.
Version: 1.3.3
Summary: Updated SimpleTransition to use the target scene's theme background color instead of black.
"""

import pygame
from abc import ABC, abstractmethod
from core.config import Config
from scenes.base_scene import BaseScene
from plugins.plugins import register_transition

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
        transitions/transitions.py - Initializes a transition between scenes.
        Version: 1.3.3
        """
        self.from_scene = from_scene
        self.to_scene = to_scene
        self.config = config
        self.duration = duration
        self.elapsed = 0.0

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        transitions/transitions.py - Update the transition's progress.
        Version: 1.3.3
        """
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        transitions/transitions.py - Draw the transition effect on the screen.
        Version: 1.3.3
        """
        pass

    def is_complete(self) -> bool:
        """
        transitions/transitions.py - Check if the transition has finished.
        Version: 1.3.3
        """
        return self.elapsed >= self.duration

@register_transition('simple')
def create_simple_transition(from_scene: BaseScene, to_scene: BaseScene, config: Config, duration: float = 1.0) -> Transition:
    """
    transitions/transitions.py - Factory function for creating a simple fade transition.
    Version: 1.3.3
    """
    return SimpleTransition(from_scene, to_scene, config, duration)

class SimpleTransition(Transition):
    def __init__(self, from_scene: BaseScene, to_scene: BaseScene, config: Config, duration: float = 1.0):
        """
        transitions/transitions.py - Creates a simple fade transition overlay using the target scene's theme background color.
        Version: 1.3.3
        """
        super().__init__(from_scene, to_scene, config, duration)
        self.fade_surface = pygame.Surface((config.screen_width, config.screen_height))
        # Use the target scene's theme background color for the fade overlay.
        self.fade_surface.fill(to_scene.config.theme.background_color)

    def update(self, dt: float) -> None:
        """
        transitions/transitions.py - Updates the transition's progress and updates the incoming scene.
        Version: 1.3.3
        """
        self.elapsed += dt
        self.to_scene.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """
        transitions/transitions.py - Draws the transition effect on the screen.
        The screen is first filled with the target scene's background color, then dynamic layers are drawn,
        followed by the fade overlay (whose alpha decreases over time), and finally persistent layers.
        Version: 1.3.3
        """
        # Fill with the target scene's background color.
        screen.fill(self.to_scene.config.theme.background_color)
        # Draw dynamic (non-persistent) layers of the incoming scene.
        self.to_scene.draw_dynamic(screen)
        # Compute fade progress: alpha decreases from 255 to 0.
        progress = min(self.elapsed / self.duration, 1.0)
        alpha = int((1 - progress) * 255)
        self.fade_surface.set_alpha(alpha)
        screen.blit(self.fade_surface, (0, 0))
        # Draw persistent layers on top.
        self.to_scene.draw_persistent(screen)