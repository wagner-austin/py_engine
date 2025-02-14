"""
transitions.py - Plugin-based transitions for scene changes.
Version: 1.3.2 (Added screen.fill(...) in SimpleTransition.draw() 
                to avoid 'smearing' from old frame).
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
        Initializes the transition.

        Parameters:
            from_scene (BaseScene): The outgoing scene.
            to_scene (BaseScene): The incoming scene.
            config (Config): The global configuration (used for screen dimensions).
            duration (float): Transition duration in seconds.
        """
        self.from_scene = from_scene
        self.to_scene = to_scene
        self.config = config
        self.duration = duration
        self.elapsed = 0.0

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update the transition's progress.

        Parameters:
            dt (float): Delta time in seconds.
        """
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the transition effect on the given screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the transition.
        """
        pass

    def is_complete(self) -> bool:
        """
        Returns True when the transition has finished.
        """
        return self.elapsed >= self.duration

@register_transition('simple')
def create_simple_transition(from_scene: BaseScene, to_scene: BaseScene, config: Config, duration: float = 1.0) -> Transition:
    """
    Factory function for creating a simple fade transition.

    Parameters:
        from_scene (BaseScene): The outgoing scene.
        to_scene (BaseScene): The incoming scene.
        config (Config): The configuration object.
        duration (float): The duration of the transition in seconds.

    Returns:
        Transition: A SimpleTransition instance.
    """
    return SimpleTransition(from_scene, to_scene, config, duration)

class SimpleTransition(Transition):
    def __init__(self, from_scene: BaseScene, to_scene: BaseScene, config: Config, duration: float = 1.0):
        """
        Creates a simple transition that overlays a black rectangle.
        The overlay starts fully opaque and fades out over the transition duration.

        Parameters:
            from_scene (BaseScene): The outgoing scene.
            to_scene (BaseScene): The incoming scene.
            config (Config): The global configuration.
            duration (float): Transition duration in seconds.
        """
        super().__init__(from_scene, to_scene, config, duration)
        self.fade_surface = pygame.Surface((config.screen_width, config.screen_height))
        self.fade_surface.fill((0, 0, 0))  # Black color

    def update(self, dt: float) -> None:
        """
        Updates the transition's progress and updates the incoming scene.

        Parameters:
            dt (float): Delta time in seconds.
        """
        self.elapsed += dt
        # Update the incoming scene so dynamic elements remain active.
        self.to_scene.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the transition effect on the given screen.

        The fade overlay starts fully opaque and fades out, revealing the to_scene.
        This code first fills the entire screen with the to_scene's background color 
        to avoid leftover 'smears' from the old scene. Then it draws dynamic layers 
        of the new scene, applies a black overlay at decreasing alpha, and finally 
        draws the persistent layers of the new scene.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the transition.
        """
        # 1) Fill to ensure we don't see leftover pixels from old scene frames.
        screen.fill(self.to_scene.config.theme.background_color)

        # 2) Draw dynamic (non‑persistent) layers of the incoming scene.
        self.to_scene.draw_dynamic(screen)

        # 3) Compute fade progress: alpha decreases from 255 to 0.
        progress = min(self.elapsed / self.duration, 1.0)
        alpha = int((1 - progress) * 255)
        self.fade_surface.set_alpha(alpha)
        screen.blit(self.fade_surface, (0, 0))

        # 4) Draw persistent layers on top.
        self.to_scene.draw_persistent(screen)