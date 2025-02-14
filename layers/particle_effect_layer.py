"""
particle_effect_layer.py - A dedicated layer for continuous particle effects.
Version: 1.0
"""

from plugins import register_layer
from layers.base_layer import BaseLayer
from config import Config
import pygame

# If you comment out this decorator, the layer won't be added to the registry.
@register_layer("particle_effect", "effect")
class ParticleEffectLayer(BaseLayer):
    def __init__(self, config: Config) -> None:
        """
        Initializes a simple, continuous particle effect layer.

        Parameters:
            config (Config): Global configuration, used for screen size.
        """
        self.config = config
        self.z = 2  # Or whichever z-index you like for effect layers
        self.persistent = False

        # Borrow your existing code that sets up the continuous effect:
        from effects.particle_effect import create_default_continuous_effect
        self.continuous_effect = create_default_continuous_effect()

        # Timer if you still want intermittent spawns:
        self.spawn_timer = 0.0
        self.spawn_interval = 0.2

    def update(self, dt: float) -> None:
        """
        Updates the particle effect and spawns new particles intermittently.
        """
        self.continuous_effect.update(dt)
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            # Example: spawn new particles in a 100x50 rect near the center.
            screen_rect = pygame.Rect(
                self.config.screen_width // 2 - 50,
                self.config.screen_height // 2 - 25,
                100,
                50
            )
            self.continuous_effect.spawn_continuous_from_rect(screen_rect)
            self.spawn_timer = 0.0

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws all particles of this effect onto the screen.
        """
        self.continuous_effect.draw(screen)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Currently no input handling for this layer.
        """
        pass
