"""
ui_elements.py - Provides UI element definitions such as the Button class and the IUIElement protocol.

Version: 1.1 (moved from ui_manager.py)
"""

import pygame
from typing import Callable, Tuple, Protocol

class IUIElement(Protocol):
    def update(self) -> None:
        ...

    def draw(self, screen: pygame.Surface) -> None:
        ...

    def handle_event(self, event: pygame.event.Event) -> None:
        ...

class Button:
    """
    Represents a clickable UI button.
    """

    def __init__(
        self,
        rect: Tuple[int, int, int, int],
        label: str,
        callback: Callable[[], None],
        font: pygame.font.Font,
        normal_color: Tuple[int, int, int] = (200, 0, 200),
        selected_color: Tuple[int, int, int] = (57, 255, 20),
        background_color: Tuple[int, int, int] = None
    ) -> None:
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
        self.background_color: Tuple[int, int, int] = background_color  # Optional fill color.
        self.text_surface_normal = None
        self.text_surface_selected = None
        self._cached_state = None
        self.update_surfaces()

    def update_surfaces(self) -> None:
        """
        Re-renders the text surfaces using the current font and colors if properties have changed.
        Simplified caching logic using join to build the label if extra spacing is required.
        """
        current_state = (
            self.label,
            id(self.font),
            self.font.get_height(),
            self.normal_color,
            self.selected_color
        )
        if self._cached_state == current_state:
            return
        extra_spaces = 0  # Set to a positive integer to add extra spacing between characters if needed.
        new_line = (" " * extra_spaces).join(list(self.label)) if extra_spaces > 0 else self.label
        self.text_surface_normal = self.font.render(new_line, True, self.normal_color)
        self.text_surface_selected = self.font.render(new_line, True, self.selected_color)
        self._cached_state = current_state

    def update(self) -> None:
        """
        Updates the button.
        
        Recalculates text surfaces if the button properties have changed.
        """
        self.update_surfaces()

    def draw(self, screen: pygame.Surface, selected: bool = False) -> None:
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
