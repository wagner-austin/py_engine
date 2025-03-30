"""
managers/input_manager.py - Provides a dedicated InputManager for handling and dispatching mouse/touch events using a clean pipeline.
Version: 1.4.2
Summary: Processes events by dispatching only mouse events (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION).
"""

import pygame
from typing import List
from pygame.event import Event
from core.interfaces import IInputHandler  # Removed IGlobalInputHandler as it does not exist.
from core.config import Config

# Define the input handler type using only IInputHandler.
InputHandlerType = IInputHandler

class InputManager:
    def __init__(self, config: Config) -> None:
        """
        managers/input_manager.py - Initializes the InputManager with a configuration and an empty list of handlers.
        Version: 1.4.2
        Parameters:
            config: Global configuration object.
        """
        self.config = config
        self.handlers: List[InputHandlerType] = []

    def register_handler(self, handler: InputHandlerType) -> None:
        """
        Registers an event handler if not already registered.
        """
        if handler not in self.handlers:
            self.handlers.append(handler)

    def unregister_handler(self, handler: InputHandlerType) -> None:
        """
        Unregisters an event handler.
        """
        if handler in self.handlers:
            self.handlers.remove(handler)

    def process_event(self, event: Event) -> None:
        """
        Processes a single pygame event using a simplified pipeline:
          - Only mouse events (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION) are processed.
        Version: 1.4.2
        Parameters:
            event: The pygame event to process.
        """
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            for handler in self.handlers:
                if hasattr(handler, "on_input") and handler.on_input(event):
                    return

# End of managers/input_manager.py