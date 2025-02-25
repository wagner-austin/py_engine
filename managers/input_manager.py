"""
input_manager.py - Provides a dedicated InputManager for handling and dispatching input events using a clean pipeline.
Version: 1.4.2
Summary: Processes events in a prioritized order:
         1. Global input handlers (IGlobalInputHandler) are given first chance.
         2. Then, regular input handlers (IInputHandler) are invoked.
         If any handler returns True (indicating the event is consumed), further processing is halted.
"""

import pygame
from typing import List, Union
from pygame.event import Event
from core.interfaces import IInputHandler, IGlobalInputHandler
from core.config import Config

# Union type for handlers that may implement either interface.
InputHandlerType = Union[IInputHandler, IGlobalInputHandler]

class InputManager:
    def __init__(self, config: Config) -> None:
        """
        Initializes the InputManager with a configuration and an empty list of handlers.
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
        Processes a single pygame event using a prioritized pipeline:
          1. For KEYDOWN events, dispatch to global input handlers (IGlobalInputHandler) first.
             If any handler returns True, the event is consumed.
          2. Then dispatch to regular input handlers (IInputHandler) until one consumes it.
          3. For mouse events (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION), dispatch similarly.
        Version: 1.4.2
        Parameters:
            event: The pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            # First, try global input handlers.
            for handler in self.handlers:
                if isinstance(handler, IGlobalInputHandler):
                    if handler.on_global_input(event):
                        return
            # Then, try regular input handlers.
            for handler in self.handlers:
                if isinstance(handler, IInputHandler):
                    if handler.on_input(event):
                        return
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            for handler in self.handlers:
                if isinstance(handler, IInputHandler):
                    if handler.on_input(event):
                        return