# File: layers/directional_button_layer.py

"""
layers/directional_button_layer.py - Provides a directional button layer for game area control.
--------------------------------------------------------------------------------
Version: 1.3.14
Summary:
  - All buttons (directional + A/B) now highlight on mouse-down, then call callback on mouse-up if still inside.
  - Ensures the user actually sees the highlight for the B button, even if it triggers a scene change.
"""

import pygame
import math
from typing import Callable
from layers.base_layer import BaseLayer
from core.config import Config
from plugins.plugins import register_layer

@register_layer("directional_button_layer", "game_controls")
class DirectionalButtonLayer(BaseLayer):
    def __init__(self, font: pygame.font.Font, config: Config, callback: Callable[[str, bool], None]) -> None:
        """
        Initializes the DirectionalButtonLayer.
        Provides on-screen directional and action buttons with unified mouse/touch input handling.
        Version: 1.3.14

        Parameters:
            font (pygame.font.Font): The font used for rendering labels on buttons.
            config (Config): The global configuration object.
            callback (Callable[[str, bool], None]): A function called when a button is clicked.
        """
        self.font = font
        self.config = config
        self.callback = callback
        self.persistent = True  # Remain visible through transitions

        # Increase directional button size for a larger pad.
        self.button_size = self.config.scale_value(100)
        self.margin = self.config.scale_value(20)

        # Set a fixed left margin for the directional pad.
        self.pad_left_margin = self.config.scale_value(30)

        # Calculate offset for directional button placement (distance between centers).
        offset = self.button_size + self.margin

        # Compute the pad center x based on the fixed left margin.
        self.pad_center_x = self.pad_left_margin + offset + self.button_size // 2

        # Position the directional pad so its center is 70% down the screen.
        self.pad_center_y = int(self.config.screen_height * 0.7)

        # Arrange the directional buttons in a diamond formation.
        self.buttons = {
            "up": pygame.Rect(
                self.pad_center_x - self.button_size // 2,
                self.pad_center_y - offset - self.button_size // 2,
                self.button_size, self.button_size
            ),
            "down": pygame.Rect(
                self.pad_center_x - self.button_size // 2,
                self.pad_center_y + offset - self.button_size // 2,
                self.button_size, self.button_size
            ),
            "left": pygame.Rect(
                self.pad_center_x - offset - self.button_size // 2,
                self.pad_center_y - self.button_size // 2,
                self.button_size, self.button_size
            ),
            "right": pygame.Rect(
                self.pad_center_x + offset - self.button_size // 2,
                self.pad_center_y - self.button_size // 2,
                self.button_size, self.button_size
            ),
        }

        # Track pressed state for directional buttons.
        self.pressed = {"up": False, "down": False, "left": False, "right": False}

        # Add two large circular action buttons ("A" and "B").
        self.pad_right_margin = self.config.scale_value(30)
        self.action_button_size = self.config.scale_value(120)

        # Compute original center for button A.
        orig_a_center_x = self.config.screen_width - self.pad_right_margin - self.action_button_size / 2
        orig_a_center_y = self.pad_center_y - self.action_button_size / 2
        # Adjust button A's center: move a bit higher and to the left.
        a_offset_x = self.config.scale_value(10)
        a_offset_y = self.config.scale_value(10)
        a_center_x = orig_a_center_x - a_offset_x
        a_center_y = orig_a_center_y - a_offset_y

        # Button B's center.
        b_center_x = orig_a_center_x - self.action_button_size
        b_center_y = orig_a_center_y + self.action_button_size + self.margin

        self.action_buttons = {
            "A": {
                "rect": pygame.Rect(
                    int(a_center_x - self.action_button_size / 2),
                    int(a_center_y - self.action_button_size / 2),
                    self.action_button_size, self.action_button_size
                ),
                "center": (a_center_x, a_center_y)
            },
            "B": {
                "rect": pygame.Rect(
                    int(b_center_x - self.action_button_size / 2),
                    int(b_center_y - self.action_button_size / 2),
                    self.action_button_size, self.action_button_size
                ),
                "center": (b_center_x, b_center_y)
            }
        }
        self.action_pressed = {"A": False, "B": False}

        # Define hit inflation factor (20% larger hit area).
        self.hit_inflation = 0.2

    def update(self, dt: float) -> None:
        """
        Update method (no periodic updates needed for static pad).
        Version: 1.3.14
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the directional and action buttons.
        Version: 1.3.14
        """
        # Directional buttons
        for direction, rect in self.buttons.items():
            color = (
                self.config.theme.button_selected_color
                if self.pressed[direction]
                else self.config.theme.button_normal_color
            )
            pygame.draw.rect(screen, color, rect, border_radius=8)

        # Action buttons (circular)
        for key, info in self.action_buttons.items():
            color = (
                self.config.theme.button_selected_color
                if self.action_pressed[key]
                else self.config.theme.button_normal_color
            )
            center = info["center"]
            radius = int(self.action_button_size / 2)
            pygame.draw.circle(screen, color, (int(center[0]), int(center[1])), radius)

    def on_input(self, event: pygame.event.Event) -> bool:
        """
        Handles mouse/touch events for directional and action buttons.
        Version: 1.3.14
        Returns True if the event was handled, False otherwise.
        """
        handled = False
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            pos = event.pos

            # 1) Directional buttons: highlight on down, callback on up (if still inside).
            for direction, rect in self.buttons.items():
                inflated_rect = rect.inflate(
                    self.button_size * self.hit_inflation,
                    self.button_size * self.hit_inflation
                )

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if inflated_rect.collidepoint(pos):
                        self.pressed[direction] = True
                        handled = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    # If we were pressed, check if we're still inside
                    if self.pressed[direction]:
                        self.pressed[direction] = False
                        if inflated_rect.collidepoint(pos):
                            self.callback(direction, True)  # Callback on release
                        handled = True

            # 2) Action buttons (A/B): same "highlight on down, fire callback on up if still inside".
            for key, info in self.action_buttons.items():
                center = info["center"]
                dx = pos[0] - center[0]
                dy = pos[1] - center[1]
                distance = math.hypot(dx, dy)
                effective_radius = (self.action_button_size / 2) * (1 + self.hit_inflation)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if distance <= effective_radius:
                        self.action_pressed[key] = True
                        handled = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.action_pressed[key]:
                        self.action_pressed[key] = False
                        if distance <= effective_radius:
                            self.callback(key, True)
                        handled = True

            if handled:
                return True

        return False

# End of layers/directional_button_layer.py