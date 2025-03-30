"""
core/interfaces.py - Defines explicit interfaces for event handlers.
--------------------------------------------------------------------------------
Version: 1.0
Summary: Provides the input handler interface using mouse/touch events.
"""

from typing import Protocol, runtime_checkable
import pygame

@runtime_checkable
class IInputHandler(Protocol):
    def on_input(self, event: pygame.event.Event) -> None:
        """
        Handle a general input event via mouse/touch interactions.
        """
        ...

# End of core/interfaces.py