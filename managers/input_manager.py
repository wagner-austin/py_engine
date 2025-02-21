"""
input_manager.py - Provides a dedicated InputManager for handling and dispatching input events.
Version: 1.4.1
"""

import pygame
from typing import List, Union
from pygame.event import Event
from core.interfaces import IInputHandler, IGlobalInputHandler
from core.config import Config

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
        
        This method now processes KEYDOWN and mouse events (MOUSEBUTTONDOWN, MOUSEBUTTONUP, and MOUSEMOTION)
        for input dispatch. Global key events (such as Escape or Q) are processed and dispatched exclusively to
        handlers implementing IGlobalInputHandler. All other events are dispatched to handlers implementing IInputHandler.
        
        Parameters:
            event: The pygame event to process.
        """
        # Do not automatically re-enable text input on MOUSEBUTTONDOWN to prevent keyboard popup.
        # Dispatch KEYDOWN events.
        if event.type == pygame.KEYDOWN:
            if event.key in self.config.global_input_keys:
                for handler in self.handlers:
                    if isinstance(handler, IGlobalInputHandler):
                        handler.on_global_input(event)
                return
            for handler in self.handlers:
                if isinstance(handler, IInputHandler):
                    handler.on_input(event)
        # Dispatch mouse events.
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            for handler in self.handlers:
                if isinstance(handler, IInputHandler):
                    handler.on_input(event)