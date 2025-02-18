"""
space_shooter.py - A modular Space Shooter game mode with independent effects.
Version: 1.1.2
Summary: Implements WASD/arrow-key movement with directional rotation, spacebar firing with bullet effects,
         and isolates game logic (including effects) within its own folder for plug-and-play flexibility.
"""

import math
import pygame
from core.config import Config
from managers.layer_manager import LayerManager
from plugins.plugins import register_play_mode

@register_play_mode("Space Shooter")
class SpaceShooter:
    def __init__(self, font: pygame.font.Font, config: Config, layer_manager: LayerManager) -> None:
        """
        Initializes the Space Shooter mode.
        Version: 1.1.2
        Summary: Sets up the spaceship, its effect (bullets), and initial properties.
        """
        self.font = font
        self.config = config
        self.layer_manager = layer_manager
        # Initialize spaceship position at the center of the screen.
        self.spaceship_pos = [config.screen_width // 2, config.screen_height // 2]
        # Velocity in pixels per second.
        self.spaceship_vel = [0, 0]
        # Initial facing angle (in degrees).
        self.spaceship_angle = 0
        # Create a dedicated spaceship surface with a drawn triangle.
        self.spaceship_surface = self.create_spaceship_surface()
        # List to manage bullet effects.
        self.bullets = []

    def create_spaceship_surface(self) -> pygame.Surface:
        """
        Creates and returns a surface with a drawn spaceship.
        Version: 1.1.2
        Summary: The spaceship is represented as a yellow triangle.
        """
        width, height = 40, 30
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        # Draw a triangle: tip at the right center, base at the left.
        points = [(width, height // 2), (0, 0), (0, height)]
        pygame.draw.polygon(surf, (255, 255, 0), points)
        return surf

    def on_enter(self) -> None:
        """
        Called when the game mode starts.
        Version: 1.1.2
        """
        # (Optional logging or initialization can be added here.)
        pass

    def update(self, dt: float) -> None:
        """
        Updates the spaceship position, rotation, and active bullet effects.
        Version: 1.1.2
        """
        # Update spaceship position.
        self.spaceship_pos[0] += self.spaceship_vel[0] * dt
        self.spaceship_pos[1] += self.spaceship_vel[1] * dt

        # Wrap around the screen boundaries.
        if self.spaceship_pos[0] > self.config.screen_width:
            self.spaceship_pos[0] = 0
        elif self.spaceship_pos[0] < 0:
            self.spaceship_pos[0] = self.config.screen_width

        if self.spaceship_pos[1] > self.config.screen_height:
            self.spaceship_pos[1] = 0
        elif self.spaceship_pos[1] < 0:
            self.spaceship_pos[1] = self.config.screen_height

        # Update spaceship rotation based on velocity.
        vx, vy = self.spaceship_vel
        if vx != 0 or vy != 0:
            # Compute angle so that 0 degrees faces right.
            self.spaceship_angle = math.degrees(math.atan2(-vy, vx))

        # Update bullets.
        for bullet in self.bullets:
            bullet['pos'][0] += bullet['vel'][0] * dt
            bullet['pos'][1] += bullet['vel'][1] * dt

        # Remove bullets that have left the screen.
        self.bullets = [
            b for b in self.bullets
            if 0 <= b['pos'][0] <= self.config.screen_width and 0 <= b['pos'][1] <= self.config.screen_height
        ]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the rotated spaceship and active bullet effects.
        Version: 1.1.2
        """
        # Rotate the spaceship surface according to the current angle.
        rotated_surface = pygame.transform.rotate(self.spaceship_surface, self.spaceship_angle)
        rotated_rect = rotated_surface.get_rect(center=(int(self.spaceship_pos[0]), int(self.spaceship_pos[1])))
        screen.blit(rotated_surface, rotated_rect)

        # Draw bullets (as red circles).
        for bullet in self.bullets:
            pos = bullet['pos']
            pygame.draw.circle(screen, (255, 0, 0), (int(pos[0]), int(pos[1])), 5)

        # Draw a label to indicate the mode.
        label = self.font.render("Space Shooter Mode", True, self.config.theme.font_color)
        screen.blit(label, (10, 10))

    def fire(self) -> None:
        """
        Fires a bullet effect from the spaceship.
        Version: 1.1.2
        Summary: Creates a bullet that travels in the direction the spaceship is facing.
        """
        bullet_speed = 300  # Pixels per second.
        # Convert the current angle to a direction vector.
        rad = math.radians(self.spaceship_angle)
        dir_x = math.cos(rad)
        dir_y = -math.sin(rad)
        bullet = {
            'pos': self.spaceship_pos.copy(),
            'vel': [bullet_speed * dir_x, bullet_speed * dir_y]
        }
        self.bullets.append(bullet)
        # In the future, this firing action can trigger additional effects (damage, particles, etc.) via a dedicated effects layer.

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Handles input for movement and firing.
        Version: 1.1.2
        Summary: Supports both arrow keys and WASD for movement, with spacebar triggering firing.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.spaceship_vel[0] = -100
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.spaceship_vel[0] = 100
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.spaceship_vel[1] = -100
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.spaceship_vel[1] = 100
            elif event.key == pygame.K_SPACE:
                self.fire()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
                self.spaceship_vel[0] = 0
            elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s):
                self.spaceship_vel[1] = 0