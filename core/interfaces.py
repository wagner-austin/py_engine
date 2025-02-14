"""
interfaces.py - Defines explicit interfaces for event handlers.

Version: 1.0
"""

from typing import Protocol, runtime_checkable
import pygame

@runtime_checkable
class IInputHandler(Protocol):
    def on_input(self, event: pygame.event.Event) -> None:
        """
        Handle a general input event.
        """
        ...

@runtime_checkable
class IGlobalInputHandler(Protocol):
    def on_global_input(self, event: pygame.event.Event) -> None:
        """
        Handle global input events (e.g. Escape or Q) that should be caught
        regardless of the current context.
        """
        ...
