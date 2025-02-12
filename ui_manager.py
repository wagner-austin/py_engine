"""
ui_manager.py - Provides UI components (such as Button) and a UIManager for managing UI elements.

Version: 1.0
"""

import pygame
from typing import Any, Callable, List, Tuple

class Button:
    """
    Represents a clickable UI button.
    """

    def __init__(self, rect: Tuple[int, int, int, int], label: str, callback: Callable[[], None], font: pygame.font.Font,
                 normal_color: Tuple[int, int, int]=(200, 0, 200),
                 selected_color: Tuple[int, int, int]=(57, 255, 20),
                 background_color: Any=None) -> None:
        """
        Initializes the Button with the provided rectangle, label, callback, and font.
        
        Parameters:
            rect: A tuple defining the button's rectangle (x, y, width, height).
            label: The text label of the button.
            callback: The function to call when the button is clicked.
            font: The pygame font used to render the label.
            normal_color: The color of the text when not selected.
            selected_color: The color of the text when selected.
            background_color: Optional background color for the button.
        """
        self.rect = pygame.Rect(rect)
        self.label: str = label
        self.callback: Callable[[], None] = callback
        self.font: pygame.font.Font = font
        self.normal_color: Tuple[int, int, int] = normal_color
        self.selected_color: Tuple[int, int, int] = selected_color
        self.background_color: Any = background_color  # Optional fill color.
        self.text_surface_normal: Any = None
        self.text_surface_selected: Any = None
        self._cached_state: Any = None
        self.update_surfaces()

    def update_surfaces(self) -> None:
        """
        Re-renders the text surfaces using the current font and colors if properties have changed.
        """
        current_state = (self.label, id(self.font), self.font.get_height(), self.normal_color, self.selected_color)
        if self._cached_state == current_state:
            return
        self.text_surface_normal = self.font.render(self.label, True, self.normal_color)
        self.text_surface_selected = self.font.render(self.label, True, self.selected_color)
        self._cached_state = current_state

    def update(self) -> None:
        """
        Updates the button.
        
        Recalculates text surfaces if the button properties have changed.
        """
        self.update_surfaces()

    def draw(self, screen: pygame.Surface, selected: bool=False) -> None:
        """
        Draws the button onto the provided screen.
        
        Parameters:
            screen: The pygame Surface on which to draw the button.
            selected: A boolean indicating if the button is selected.
        """
        if self.background_color:
            pygame.draw.rect(screen, self.background_color, self.rect)
        text_surface = self.text_surface_selected if selected else self.text_surface_normal
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles input events for the button.
        
        Parameters:
            event: A pygame event.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

class UIManager:
    """
    Manages a collection of UI elements, handling rendering and event dispatch.
    """

    def __init__(self) -> None:
        """Initializes the UIManager with an empty list of UI elements."""
        self.ui_elements: List[Any] = []  # List of UI components

    def register(self, element: Any) -> None:
        """
        Registers a UI element with the manager.
        
        Parameters:
            element: The UI component to register.
        """
        if element not in self.ui_elements:
            self.ui_elements.append(element)

    def unregister(self, element: Any) -> None:
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
            if hasattr(element, "update"):
                element.update()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws all registered UI elements onto the provided screen.
        
        Parameters:
            screen: The pygame Surface on which to draw the UI elements.
        """
        for element in self.ui_elements:
            if hasattr(element, "draw"):
                element.draw(screen)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Dispatches an event to all registered UI elements.
        
        Parameters:
            event: A pygame event.
        """
        for element in self.ui_elements:
            if hasattr(element, "handle_event"):
                element.handle_event(event)