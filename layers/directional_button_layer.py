"""
directional_button_layer.py - Provides a directional button layer for game area control,
which maps directional input (up, down, left, right) and action buttons (A, B) to simulate
key down and key up events, similar to a Gameboy controller.
Version: 1.3.8
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
        directional_button_layer.py - Initializes the DirectionalButtonLayer.
        Provides on-screen directional and action buttons with unified input handling.
        Version: 1.3.8
        Parameters:
            font (pygame.font.Font): The font used for rendering labels on buttons.
            config (Config): The global configuration object.
            callback (Callable[[str, bool], None]): A function called when a button is pressed or released.
        """
        self.font = font
        self.config = config
        self.callback = callback
        self.persistent = True  # Mark as persistent so it is not affected by transitions

        # Increase directional button size for a larger pad.
        self.button_size = self.config.scale_value(100)  # Increased from 80 to 100
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

        # Add two large circular action buttons ("A" and "B") arranged diagonally with no overlap.
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
                "rect": pygame.Rect(int(a_center_x - self.action_button_size / 2),
                                      int(a_center_y - self.action_button_size / 2),
                                      self.action_button_size, self.action_button_size),
                "center": (a_center_x, a_center_y)
            },
            "B": {
                "rect": pygame.Rect(int(b_center_x - self.action_button_size / 2),
                                      int(b_center_y - self.action_button_size / 2),
                                      self.action_button_size, self.action_button_size),
                "center": (b_center_x, b_center_y)
            }
        }
        self.action_pressed = {"A": False, "B": False}

        # Define hit inflation factor (20% larger hit area).
        self.hit_inflation = 0.2

    def update(self, dt: float) -> None:
        """
        directional_button_layer.py - Update method (no periodic updates needed for static pad).
        Version: 1.3.8
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        directional_button_layer.py - Draws the directional and action buttons.
        Version: 1.3.8
        """
        for direction, rect in self.buttons.items():
            color = self.config.theme.button_selected_color if self.pressed[direction] else self.config.theme.button_normal_color
            pygame.draw.rect(screen, color, rect, border_radius=8)
        for key, info in self.action_buttons.items():
            color = self.config.theme.button_selected_color if self.action_pressed[key] else self.config.theme.button_normal_color
            center = info["center"]
            radius = int(self.action_button_size / 2)
            pygame.draw.circle(screen, color, (int(center[0]), int(center[1])), radius)

    def on_input(self, event: pygame.event.Event) -> bool:
        """
        directional_button_layer.py - Handles input events for touch and key interactions.
        Supports MOUSEBUTTON events as well as KEYDOWN/KEYUP for unified control.
        Version: 1.3.8
        Returns: True if the event was handled, False otherwise.
        """
        handled = False
        # Handle mouse/touch events
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            pos = event.pos
            # Process directional buttons with inflated hit area
            for direction, rect in self.buttons.items():
                inflated_rect = rect.inflate(self.button_size * self.hit_inflation, self.button_size * self.hit_inflation)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if inflated_rect.collidepoint(pos):
                        if not self.pressed[direction]:
                            self.pressed[direction] = True
                            self.callback(direction, True)
                            handled = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.pressed[direction]:
                        # Release regardless of pointer position
                        self.pressed[direction] = False
                        self.callback(direction, False)
                        handled = True
            # Process action buttons with increased effective radius
            for key, info in self.action_buttons.items():
                center = info["center"]
                dx = pos[0] - center[0]
                dy = pos[1] - center[1]
                distance = math.hypot(dx, dy)
                effective_radius = (self.action_button_size / 2) * (1 + self.hit_inflation)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if distance <= effective_radius:
                        if not self.action_pressed[key]:
                            self.action_pressed[key] = True
                            self.callback(key, True)
                            handled = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.action_pressed[key]:
                        # Unconditionally release the action button
                        self.action_pressed[key] = False
                        self.callback(key, False)
                        handled = True
            if handled:
                return True
        # Handle keyboard events for unified control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if not self.pressed["up"]:
                    self.pressed["up"] = True
                    self.callback("up", True)
                    handled = True
            if event.key == pygame.K_s:
                if not self.pressed["down"]:
                    self.pressed["down"] = True
                    self.callback("down", True)
                    handled = True
            if event.key == pygame.K_a:
                if not self.pressed["left"]:
                    self.pressed["left"] = True
                    self.callback("left", True)
                    handled = True
            if event.key == pygame.K_d:
                if not self.pressed["right"]:
                    self.pressed["right"] = True
                    self.callback("right", True)
                    handled = True
            if event.key == pygame.K_RETURN:
                if not self.action_pressed["A"]:
                    self.action_pressed["A"] = True
                    self.callback("A", True)
                    handled = True
            if event.key == pygame.K_q:
                if not self.action_pressed["B"]:
                    self.action_pressed["B"] = True
                    self.callback("B", True)
                    handled = True
            return handled
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                if self.pressed["up"]:
                    self.pressed["up"] = False
                    self.callback("up", False)
                    handled = True
            if event.key == pygame.K_s:
                if self.pressed["down"]:
                    self.pressed["down"] = False
                    self.callback("down", False)
                    handled = True
            if event.key == pygame.K_a:
                if self.pressed["left"]:
                    self.pressed["left"] = False
                    self.callback("left", False)
                    handled = True
            if event.key == pygame.K_d:
                if self.pressed["right"]:
                    self.pressed["right"] = False
                    self.callback("right", False)
                    handled = True
            if event.key == pygame.K_RETURN:
                if self.action_pressed["A"]:
                    self.action_pressed["A"] = False
                    self.callback("A", False)
                    handled = True
            if event.key == pygame.K_q:
                if self.action_pressed["B"]:
                    self.action_pressed["B"] = False
                    self.callback("B", False)
                    handled = True
            return handled
        return False