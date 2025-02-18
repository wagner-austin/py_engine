"""
effects/particle_effect.py - Implements a basic particle effect system.
Version: 1.2.3
Summary: Updated to use a gradually updated particle color palette so that theme changes do not reset the particle animation.
"""

import pygame
import random
from typing import Tuple, List
from core.config import Config

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

def interpolate_color(color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    """
    Interpolates between two colors.
    Version: 1.2.3
    """
    return (
        int(color1[0] + (color2[0] - color1[0]) * t),
        int(color1[1] + (color2[1] - color1[1]) * t),
        int(color1[2] + (color2[2] - color1[2]) * t)
    )

def blend_palette(palette1: Tuple[Tuple[int,int,int], ...], palette2: Tuple[Tuple[int,int,int], ...], t: float) -> Tuple[Tuple[int,int,int], ...]:
    """
    Blends two palettes (tuples of color tuples) based on t (0.0 to 1.0).
    Version: 1.2.3
    """
    if len(palette1) == len(palette2):
        return tuple(interpolate_color(c1, c2, t) for c1, c2 in zip(palette1, palette2))
    else:
        return palette2

class Particle:
    def __init__(self, position: Tuple[int, int], velocity: Tuple[float, float],
                 lifetime: float, color: Tuple[int, int, int], radius: int, shape: str = "circle") -> None:
        self.position = list(position)
        self.velocity = list(velocity)
        self.lifetime = lifetime
        self.initial_lifetime = lifetime  # store original lifetime for fade calculation
        self.color = color
        self.radius = radius
        self.shape = shape

    def update(self, dt: float) -> None:
        self.velocity[1] += PARTICLE_CONFIG["gravity"] * dt
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.lifetime -= dt

    def draw(self, screen: pygame.Surface) -> None:
        fade_factor = max(0, min(1, self.lifetime / self.initial_lifetime))
        alpha = int(255 * fade_factor)
        if self.shape == "circle":
            diameter = self.radius * 2
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

class ParticleEffect:
    def __init__(self, config: Config, color: Tuple[int, int, int], radius: int, shape: str, particle_count: int,
                 lifetime: float, spawn_rect: pygame.Rect = None) -> None:
        """
        effects/particle_effect.py - Initializes the ParticleEffect.
        Version: 1.2.3
        Summary: Uses a dynamic particle color palette that updates gradually.
        """
        self.config = config
        self.color = color  # Fallback color (unused in spawn; color is chosen from current_palette)
        self.radius = radius
        self.shape = shape
        self.particle_count = particle_count  # Deprecated – use config if needed.
        self.lifetime = lifetime
        self.particles: List[Particle] = []
        self.spawn_rect = spawn_rect
        self.spawn_timer = 0.0
        # Initialize current_palette from the active theme's particle_color_palette
        self.current_palette = self.config.theme.particle_color_palette
        self.palette_transition_duration = 1.0  # seconds

    def spawn_continuous_from_rect(self, rect: pygame.Rect) -> None:
        count = PARTICLE_CONFIG.get("particles_per_spawn", 10)
        center_x = (rect.left + rect.right) / 2
        center_y = (rect.top + rect.bottom) / 2
        sigma_x = (rect.right - rect.left) / 4
        sigma_y = (rect.bottom - rect.top) / 4

        for _ in range(count):
            x = random.gauss(center_x, sigma_x)
            y = random.gauss(center_y, sigma_y)
            x = max(rect.left, min(x, rect.right))
            y = max(rect.top, min(y, rect.bottom))
            position = (x, y)
            angle = random.uniform(80, 100)
            speed = random.uniform(*PARTICLE_CONFIG["gentle_speed_range"])
            velocity_vector = pygame.math.Vector2(1, 0).rotate(angle) * speed
            # Use the gradually updated current_palette for particle color
            color = random.choice(self.current_palette)
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
        # Gradually update current_palette toward the active theme's particle_color_palette
        t = min(1.0, dt / self.palette_transition_duration)
        self.current_palette = blend_palette(self.current_palette, self.config.theme.particle_color_palette, t)

        self.spawn_timer += dt
        if self.spawn_timer >= PARTICLE_CONFIG["continuous_spawn_interval"]:
            if self.spawn_rect is not None:
                self.spawn_continuous_from_rect(self.spawn_rect)
            self.spawn_timer = 0.0
        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.lifetime > 0]

    def draw(self, screen: pygame.Surface) -> None:
        for particle in self.particles:
            particle.draw(screen)

def create_default_continuous_effect(config: Config, spawn_rect: pygame.Rect = None) -> ParticleEffect:
    """
    effects/particle_effect.py - Factory function for creating a ParticleEffect.
    Version: 1.2.3
    """
    return ParticleEffect(
        config,
        color=(150, 200, 255),  # Fallback color; actual colors are chosen from current_palette.
        radius=PARTICLE_CONFIG["particle_size"],
        shape="circle",
        particle_count=0,  # Deprecated – number of particles per spawn is now in the config.
        lifetime=PARTICLE_CONFIG["default_lifetime"],
        spawn_rect=spawn_rect
    )