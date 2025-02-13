"""
input_manager.py - Provides a dedicated InputManager for handling and dispatching input events.
Version: 1.4 (updated to process only KEYDOWN events for phone keyboards)
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
        """
        Initializes the InputManager with a configuration and an empty list of handlers.

        Parameters:
            config: Global configuration object.
        """
        self.config = config
        self.handlers: List[InputHandlerType] = []  # Registered event handlers

    def register_handler(self, handler: InputHandlerType) -> None:
        """
        Registers an event handler if it is not already registered.

        Parameters:
            handler: An object implementing IInputHandler or IGlobalInputHandler.
        """
        if handler not in self.handlers:
            self.handlers.append(handler)

    def unregister_handler(self, handler: InputHandlerType) -> None:
        """
        Unregisters an event handler if it is currently registered.

        Parameters:
            handler: The event handler to unregister.
        """
        if handler in self.handlers:
            self.handlers.remove(handler)

    def process_event(self, event: Event) -> None:
        """
        Processes a single pygame event.

        This method now processes only KEYDOWN events for input dispatch, as phone keyboards will send
        navigation keys as KEYDOWN events. Global key events (such as Escape or Q) are processed and dispatched
        exclusively to handlers implementing IGlobalInputHandler. Non-global KEYDOWN events are dispatched to
        handlers implementing IInputHandler.

        Additionally, for touchscreen support, text input is re-enabled on MOUSEBUTTONDOWN events.

        Parameters:
            event: The pygame event to process.
        """
        # For touchscreen: re-enable text input on mouse click.
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.key.start_text_input()

        # Process KEYDOWN events exclusively.
        if event.type == pygame.KEYDOWN:
            # Global events: keys defined in config trigger global input.
            if event.key in self.config.global_input_keys:
                for handler in self.handlers:
                    if isinstance(handler, IGlobalInputHandler):
                        handler.on_global_input(event)
                return

            # Process non-global KEYDOWN events.
            for handler in self.handlers:
                if isinstance(handler, IInputHandler):
                    handler.on_input(event)