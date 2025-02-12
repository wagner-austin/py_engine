"""
input_manager.py - Provides a dedicated InputManager for handling and dispatching input events.

Version: 1.1
"""

import pygame
from typing import Any, List
from pygame.event import Event

class InputManager:
    def __init__(self) -> None:
        self.handlers: List[Any] = []  # Registered event handlers

    def register_handler(self, handler: Any) -> None:
        if handler not in self.handlers:
            self.handlers.append(handler)

    def unregister_handler(self, handler: Any) -> None:
        if handler in self.handlers:
            self.handlers.remove(handler)

    def process_event(self, event: Event) -> None:
        # For touchscreen: re-enable text input on mouse click.
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.key.start_text_input()

        # Global events: Q or Escape returns to main menu.
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
            for handler in self.handlers:
                if hasattr(handler, "on_global_input"):
                    handler.on_global_input(event)
            return

        for handler in self.handlers:
            if hasattr(handler, "on_input"):
                handler.on_input(event)