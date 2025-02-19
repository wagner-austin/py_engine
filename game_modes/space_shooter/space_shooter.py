"""
space_shooter.py
--------------------------------------------------------------------------------
A modular Space Shooter game mode with independent effects, adapted for short 
thrust impulses and correct rotation directions on Android (KEYDOWN-only).
Version: 1.4.0
Summary: 
  1) Applies a short forward/reverse thrust impulse on W/S key presses. 
  2) Adds the ship's velocity to projectile velocity on firing. 
  3) Reverses rotation logic so A rotates left, D rotates right.
"""

import math
import pygame
from core.config import Config
from managers.layer_manager import LayerManager
from plugins.plugins import register_play_mode

@register_play_mode("Space Shooter")
class SpaceShooter:
    """
    A plug-and-play "Space Shooter" mode adapted for KEYDOWN-only environments 
    (e.g. Android). Press W or S to get a short thrust impulse forward or in reverse, 
    press A/D to toggle rotation, and SPACE to fire projectiles inheriting current 
    ship velocity.
    """

    # Unique dictionary of controls for Space Shooter (defined here for modularity)
    SPACE_SHOOTER_KEYS = {
        "rotate_left": pygame.K_a,
        "rotate_right": pygame.K_d,
        "thrust_forward": pygame.K_w,
        "thrust_reverse": pygame.K_s,
        "fire": pygame.K_SPACE,
    }

    def __init__(self, font: pygame.font.Font, config: Config, layer_manager: LayerManager) -> None:
        """
        Initializes the SpaceShooter game mode with short thrust impulses.

        Parameters:
            font (pygame.font.Font): The font used to render on-screen text.
            config (Config): Global configuration object.
            layer_manager (LayerManager): Manager for layered drawing (unused here but required).
        """
        self.font = font
        self.config = config
        self.layer_manager = layer_manager

        # Ship position (center of screen), velocity, and orientation
        self.spaceship_pos = [config.screen_width // 2, config.screen_height // 2]
        self.spaceship_vel = [0.0, 0.0]
        self.spaceship_angle = 0.0

        # Toggle booleans for rotation
        self.rotating_left = False
        self.rotating_right = False

        # Timers for short thrust impulses
        self.THURST_DURATION = 0.5  # seconds
        self.thrust_timer_forward = 0.0
        self.thrust_timer_reverse = 0.0

        # Drawing and movement constants
        self.ROTATION_SPEED = 120.0     # degrees per second
        self.ACCELERATION = 200.0       # px/sec^2
        self.FRICTION_FACTOR = 0.995    # velocity multiplier

        # Prepare the spaceship graphic (triangle)
        self.spaceship_surface = self.create_spaceship_surface()

        # Track bullets in-flight
        self.bullets = []
        self.BULLET_SPEED = 300.0

    def create_spaceship_surface(self) -> pygame.Surface:
        """
        Creates and returns a small triangular surface representing the spaceship.

        Returns:
            pygame.Surface: A surface with a yellow triangle (tip at the right).
        """
        width, height = 40, 30
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        points = [(width, height // 2), (0, 0), (0, height)]
        pygame.draw.polygon(surf, (255, 255, 0), points)
        return surf

    def on_enter(self) -> None:
        """
        Called when this game mode starts. Currently does nothing.
        """
        pass

    def update(self, dt: float) -> None:
        """
        Updates the ship's position, handles continuous rotation, applies short thrust 
        while timers last, and updates bullets.

        Parameters:
            dt (float): Delta time in seconds since the last frame.
        """
        # Rotation toggles: A => increase angle (turn left), D => decrease angle (turn right).
        if self.rotating_left and not self.rotating_right:
            self.spaceship_angle += self.ROTATION_SPEED * dt
        elif self.rotating_right and not self.rotating_left:
            self.spaceship_angle -= self.ROTATION_SPEED * dt

        # Apply short forward thrust if timer is active
        if self.thrust_timer_forward > 0:
            rad = math.radians(self.spaceship_angle)
            self.spaceship_vel[0] += math.cos(rad) * self.ACCELERATION * dt
            self.spaceship_vel[1] -= math.sin(rad) * self.ACCELERATION * dt
            self.thrust_timer_forward -= dt

        # Apply short reverse thrust if timer is active
        if self.thrust_timer_reverse > 0:
            rad = math.radians(self.spaceship_angle)
            self.spaceship_vel[0] -= math.cos(rad) * self.ACCELERATION * dt
            self.spaceship_vel[1] += math.sin(rad) * self.ACCELERATION * dt
            self.thrust_timer_reverse -= dt

        # Apply friction
        self.spaceship_vel[0] *= self.FRICTION_FACTOR
        self.spaceship_vel[1] *= self.FRICTION_FACTOR

        # Update position
        self.spaceship_pos[0] += self.spaceship_vel[0] * dt
        self.spaceship_pos[1] += self.spaceship_vel[1] * dt

        # Screen wrap
        if self.spaceship_pos[0] > self.config.screen_width:
            self.spaceship_pos[0] = 0
        elif self.spaceship_pos[0] < 0:
            self.spaceship_pos[0] = self.config.screen_width
        if self.spaceship_pos[1] > self.config.screen_height:
            self.spaceship_pos[1] = 0
        elif self.spaceship_pos[1] < 0:
            self.spaceship_pos[1] = self.config.screen_height

        # Update bullets
        for bullet in self.bullets:
            bullet["pos"][0] += bullet["vel"][0] * dt
            bullet["pos"][1] += bullet["vel"][1] * dt
        # Remove bullets that leave the screen
        self.bullets = [
            b for b in self.bullets
            if 0 <= b["pos"][0] <= self.config.screen_width
               and 0 <= b["pos"][1] <= self.config.screen_height
        ]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the rotated spaceship and active bullets, plus a mode label.

        Parameters:
            screen (pygame.Surface): The surface on which to draw.
        """
        # Rotate the ship to the current angle
        rotated_ship = pygame.transform.rotate(self.spaceship_surface, self.spaceship_angle)
        ship_rect = rotated_ship.get_rect(center=(int(self.spaceship_pos[0]), int(self.spaceship_pos[1])))
        screen.blit(rotated_ship, ship_rect)

        # Bullets (red circles)
        for bullet in self.bullets:
            px, py = int(bullet["pos"][0]), int(bullet["pos"][1])
            pygame.draw.circle(screen, (255, 0, 0), (px, py), 5)

        # Label the mode at top-left
        label = self.font.render("Space Shooter Mode", True, self.config.theme.font_color)
        screen.blit(label, (10, 10))

    def fire(self) -> None:
        """
        Spawns a new bullet whose velocity is the sum of ship velocity and bullet speed 
        in the facing direction.
        """
        rad = math.radians(self.spaceship_angle)
        vx = self.BULLET_SPEED * math.cos(rad)
        vy = -self.BULLET_SPEED * math.sin(rad)

        # Inherit current ship velocity
        vx += self.spaceship_vel[0]
        vy += self.spaceship_vel[1]

        bullet = {
            "pos": [self.spaceship_pos[0], self.spaceship_pos[1]],
            "vel": [vx, vy]
        }
        self.bullets.append(bullet)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Handles KEYDOWN events for toggling rotation (A/D) or applying short thrust (W/S), 
        or firing a bullet.

        Parameters:
            event (pygame.event.Event): A Pygame event, dispatched by the InputManager.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == self.SPACE_SHOOTER_KEYS["fire"]:
                self.fire()

            elif event.key == self.SPACE_SHOOTER_KEYS["rotate_left"]:
                # Toggle rotating left
                if self.rotating_left:
                    self.rotating_left = False
                else:
                    # Ensure rotating_right is off if we switch direction
                    self.rotating_right = False
                    self.rotating_left = True

            elif event.key == self.SPACE_SHOOTER_KEYS["rotate_right"]:
                # Toggle rotating right
                if self.rotating_right:
                    self.rotating_right = False
                else:
                    self.rotating_left = False
                    self.rotating_right = True

            elif event.key == self.SPACE_SHOOTER_KEYS["thrust_forward"]:
                # Apply a short forward impulse
                self.thrust_timer_forward = self.THURST_DURATION

            elif event.key == self.SPACE_SHOOTER_KEYS["thrust_reverse"]:
                # Apply a short reverse impulse
                self.thrust_timer_reverse = self.THURST_DURATION