"""
input_manager.py - Provides a dedicated InputManager for handling and dispatching input events.

Version: 1.2 (updated with explicit event handler interfaces and configurable global input keys)
"""

import pygame
from typing import List, Union
from pygame.event import Event
from interfaces import IInputHandler, IGlobalInputHandler
from config import Config

# Define a union type for handlers that might implement either or both interfaces.
InputHandlerType = Union[IInputHandler, IGlobalInputHandler]

class InputManager:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.handlers: List[InputHandlerType] = []  # Registered event handlers

    def register_handler(self, handler: InputHandlerType) -> None:
        if handler not in self.handlers:
            self.handlers.append(handler)

    def unregister_handler(self, handler: InputHandlerType) -> None:
        if handler in self.handlers:
            self.handlers.remove(handler)

    def process_event(self, event: Event) -> None:
        # For touchscreen: re-enable text input on mouse click.
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.key.start_text_input()

        # Global events: keys defined in config trigger global input.
        if event.type == pygame.KEYDOWN and event.key in self.config.global_input_keys:
            for handler in self.handlers:
                if isinstance(handler, IGlobalInputHandler):
                    handler.on_global_input(event)
            return

        for handler in self.handlers:
            if isinstance(handler, IInputHandler):
                handler.on_input(event)