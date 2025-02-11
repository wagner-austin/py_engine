# FileName: ui_manager.py
# version: 1.1
# Summary: Provides UI components (like Button) and a UIManager for managing UI elements.
#          UIManager centralizes rendering and event dispatch for registered UI elements.
# Tags: UI, manager, modular

import pygame

class Button:
    def __init__(self, rect, label, callback, font,
                 normal_color=(200, 0, 200),
                 selected_color=(57, 255, 20),
                 background_color=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.callback = callback
        self.font = font
        self.normal_color = normal_color
        self.selected_color = selected_color
        self.background_color = background_color  # Optional fill color.
        self.text_surface_normal = self.font.render(self.label, True, self.normal_color)
        self.text_surface_selected = self.font.render(self.label, True, self.selected_color)

    def draw(self, screen, selected=False):
        if self.background_color:
            pygame.draw.rect(screen, self.background_color, self.rect)
        text_surface = self.text_surface_selected if selected else self.text_surface_normal
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

class UIManager:
    def __init__(self):
        self.ui_elements = []  # List of UI components

    def register(self, element):
        if element not in self.ui_elements:
            self.ui_elements.append(element)

    def unregister(self, element):
        if element in self.ui_elements:
            self.ui_elements.remove(element)

    def update(self):
        for element in self.ui_elements:
            if hasattr(element, "update"):
                element.update()

    def draw(self, screen):
        for element in self.ui_elements:
            if hasattr(element, "draw"):
                element.draw(screen)

    def handle_event(self, event):
        for element in self.ui_elements:
            if hasattr(element, "handle_event"):
                element.handle_event(event)