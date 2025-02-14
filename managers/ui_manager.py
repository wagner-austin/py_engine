"""
ui_manager.py - Provides a UIManager for managing UI elements.

Version: 1.1 (updated - UI elements moved to ui_elements.py)
"""

import pygame
from typing import List
from ui.ui_elements import IUIElement

class UIManager:
    """
    Manages a collection of UI elements, handling rendering and event dispatch.
    """

    def __init__(self) -> None:
        """Initializes the UIManager with an empty list of UI elements."""
        self.ui_elements: List[IUIElement] = []  # List of UI components

    def register(self, element: IUIElement) -> None:
        """
        Registers a UI element with the manager.
        
        Parameters:
            element: The UI component to register.
        """
        if element not in self.ui_elements:
            self.ui_elements.append(element)

    def unregister(self, element: IUIElement) -> None:
        """
        Unregisters a UI element from the manager.
        
        Parameters:
            element: The UI component to unregister.
        """
        if element in self.ui_elements:
            self.ui_elements.remove(element)

    def update(self) -> None:
        """
        Updates all registered UI elements.
        """
        for element in self.ui_elements:
            element.update()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws all registered UI elements onto the provided screen.
        
        Parameters:
            screen: The pygame Surface on which to draw the UI elements.
        """
        for element in self.ui_elements:
            element.draw(screen)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Dispatches an event to all registered UI elements.
        
        Parameters:
            event: A pygame event.
        """
        for element in self.ui_elements:
            element.handle_event(event)