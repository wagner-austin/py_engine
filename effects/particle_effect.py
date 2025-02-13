"""
particle_effect.py - Implements a basic particle effect system.

This module provides:
  - Particle: A simple particle with position, velocity, lifetime, color, and shape.
  - ParticleEffect: A manager class that spawns, updates, and draws particles.

All particle-related parameters (size, density, lifetime, etc.) are defined in
the PARTICLE_CONFIG dictionary. To change particle behavior, modify only this file.
Particle colors are now determined by the active theme in themes.py.
"""

import pygame
import random
from typing import Tuple, List
from themes.themes import ACTIVE_THEME  # Moved import to the top for efficiency

# CONFIG AREA: Modify these parameters to change particle behavior.
PARTICLE_CONFIG = {
    "gravity": 500,  # pixels per second²
    "gentle_speed_range": (20, 50),    # speed range for gentle particles
    "gentle_lifetime_multiplier": 1.0, # gentle particles live 1.0 * default_lifetime
    "default_lifetime": 1.0,           # default lifetime for particles (in seconds)
    "particle_size": 6,              # default particle radius
    "particles_per_spawn": 5,       # number of particles to spawn per interval
    "continuous_spawn_interval": 0.02 # time in seconds between spawns
}

class Particle:
    def __init__(self, position: Tuple[int, int], velocity: Tuple[float, float],
                 lifetime: float, color: Tuple[int, int, int], radius: int, shape: str = "circle") -> None:
        self.position = list(position)
        self.velocity = list(velocity)
        self.lifetime = lifetime
        self.initial_lifetime = lifetime  # store the original lifetime for fade calculation
        self.color = color
        self.radius = radius
        self.shape = shape

    def update(self, dt: float) -> None:
        # Apply gravity so particles fall quicker.
        self.velocity[1] += PARTICLE_CONFIG["gravity"] * dt
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.lifetime -= dt

    def draw(self, screen: pygame.Surface) -> None:
        # Calculate fade factor (from 1.0 to 0.0) and corresponding alpha value.
        fade_factor = max(0, min(1, self.lifetime / self.initial_lifetime))
        alpha = int(255 * fade_factor)
        if self.shape == "circle":
            diameter = self.radius * 2
            # Create a temporary surface with per-pixel alpha.
            temp_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
            draw_color = self.color + (alpha,)
            pygame.draw.circle(temp_surface, draw_color, (self.radius, self.radius), self.radius)
            screen.blit(temp_surface, (int(self.position[0] - self.radius), int(self.position[1] - self.radius)))
        elif self.shape == "square":
            diameter = self.radius * 2
            temp_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
            draw_color = self.color + (alpha,)
            pygame.draw.rect(temp_surface, draw_color, pygame.Rect(0, 0, diameter, diameter))
            screen.blit(temp_surface, (int(self.position[0] - self.radius), int(self.position[1] - self.radius)))
        # Additional shapes can be added here.

class ParticleEffect:
    def __init__(self, color: Tuple[int, int, int],
                 radius: int, shape: str, particle_count: int,
                 lifetime: float, spawn_rect: pygame.Rect = None) -> None:
        """
        Initializes the particle effect with configurable parameters.

        Parameters:
            color: The default color of particles.
            radius: The radius (or half-size for squares) of particles.
            shape: The shape of particles ('circle' or 'square').
            particle_count: (Deprecated) Number of particles to spawn per trigger. Use PARTICLE_CONFIG["particles_per_spawn"] instead.
            lifetime: Lifetime (in seconds) of each particle.
            spawn_rect: A pygame.Rect representing the area within which particles will be spawned.
        """
        self.color = color
        self.radius = radius
        self.shape = shape
        self.particle_count = particle_count  # Deprecated – number of particles per spawn is now in the config.
        self.lifetime = lifetime
        self.particles: List[Particle] = []
        self.spawn_rect = spawn_rect  # Required for timed spawns.
        self.spawn_timer = 0.0  # Timer to track time between spawns.

    def spawn_continuous_from_rect(self, rect: pygame.Rect) -> None:
        """
        Spawns a number of gentle, softly falling particles from within the rectangle.
        These particles have a low initial velocity with a slight downward bias,
        a lifetime based on the gentle multiplier, and are more densely packed.
        Their positions are generated using a Gaussian distribution centered on the rectangle.

        All particle settings (except color) can be modified in this file by adjusting PARTICLE_CONFIG.
        Particle color is now determined by the active theme from themes.py.

        Parameters:
            rect: A pygame.Rect representing the area within which particles will be spawned.
        """
        # Use the new config key for number of particles per spawn.
        count = PARTICLE_CONFIG.get("particles_per_spawn", 10)
        
        center_x = (rect.left + rect.right) / 2
        center_y = (rect.top + rect.bottom) / 2
        sigma_x = (rect.right - rect.left) / 4  # standard deviation for x
        sigma_y = (rect.bottom - rect.top) / 4  # standard deviation for y

        for _ in range(count):
            # Use Gaussian distribution centered on the rectangle's center.
            x = random.gauss(center_x, sigma_x)
            y = random.gauss(center_y, sigma_y)
            # Clamp the values to remain within the rectangle.
            x = max(rect.left, min(x, rect.right))
            y = max(rect.top, min(y, rect.bottom))
            position = (x, y)
            # Gentle downward bias: angle around 90° with slight variation.
            angle = random.uniform(80, 100)
            speed = random.uniform(*PARTICLE_CONFIG["gentle_speed_range"])
            velocity_vector = pygame.math.Vector2(1, 0).rotate(angle) * speed
            # Use ACTIVE_THEME from the top-level import to determine particle color palette.
            color = random.choice(ACTIVE_THEME.particle_color_palette)
            # Gentle lifetime is default_lifetime * gentle_lifetime_multiplier.
            lifetime = PARTICLE_CONFIG["default_lifetime"] * PARTICLE_CONFIG["gentle_lifetime_multiplier"]
            particle = Particle(
                position=position,
                velocity=(velocity_vector.x, velocity_vector.y),
                lifetime=lifetime,
                color=color,
                radius=self.radius,
                shape=self.shape
            )
            self.particles.append(particle)

    def update(self, dt: float) -> None:
        """
        Updates all particles, spawns new ones based solely on the interval timer,
        and removes those that have expired.

        Parameters:
            dt: Delta time in seconds.
        """
        # Spawn particles only when the interval timer is reached.
        self.spawn_timer += dt
        if self.spawn_timer >= PARTICLE_CONFIG["continuous_spawn_interval"]:
            if self.spawn_rect is not None:
                self.spawn_continuous_from_rect(self.spawn_rect)
            self.spawn_timer = 0.0  # Reset the spawn timer.

        # Update existing particles.
        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.lifetime > 0]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws all active particles onto the provided screen.

        Parameters:
            screen: The pygame Surface to draw on.
        """
        for particle in self.particles:
            particle.draw(screen)

# Factory function to create a pre-configured ParticleEffect instance.
def create_default_continuous_effect(spawn_rect: pygame.Rect = None) -> ParticleEffect:
    """
    Returns a ParticleEffect configured for timed spawns.
    Modify the parameters in PARTICLE_CONFIG to change the effect behavior.

    Parameters:
        spawn_rect: A pygame.Rect representing the area within which particles will be spawned.
    """
    return ParticleEffect(
        color=(150, 200, 255),  # Fallback color; actual colors are chosen from the active theme.
        radius=PARTICLE_CONFIG["particle_size"],
        shape="circle",
        particle_count=0,  # Deprecated – use PARTICLE_CONFIG["particles_per_spawn"] instead.
        lifetime=PARTICLE_CONFIG["default_lifetime"],
        spawn_rect=spawn_rect
    )