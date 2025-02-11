# FileName: input_manager.py
# version: 1.0
# Summary: Provides a dedicated InputManager for handling and dispatching input events.
#          Listens for common events (like Q/Escape to return to the main menu) and dispatches events
#          to registered handlers.
# Tags: input, manager, modular

import pygame

class InputManager:
    def __init__(self):
        self.handlers = []  # Registered event handlers

    def register_handler(self, handler):
        if handler not in self.handlers:
            self.handlers.append(handler)

    def unregister_handler(self, handler):
        if handler in self.handlers:
            self.handlers.remove(handler)

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            # Global events: Q or Escape returns to main menu.
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                # Dispatch global event to handlers that implement on_global_input.
                for handler in self.handlers:
                    if hasattr(handler, "on_global_input"):
                        handler.on_global_input(event)
                # Skip further processing for this event.
                continue
            # Dispatch event to all handlers that implement on_input.
            for handler in self.handlers:
                if hasattr(handler, "on_input"):
                    handler.on_input(event)
        return events
