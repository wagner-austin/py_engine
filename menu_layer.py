# File: menu_layer.py
# Version: 1.1 (modified)
# Summary: Provides the interactive menu layer (title and buttons) for the main menu.
# Tags: layers, menu, UI, modular

import pygame
from ui_manager import Button
from base_layer import BaseLayer

class MenuLayer(BaseLayer):
    def __init__(self, scene_manager, font, menu_items, config):
        self.z = 4
        self.scene_manager = scene_manager
        self.font = font
        self.config = config
        self.menu_items = menu_items  # List of (label, scene_key) tuples.
        self.selected_index = 0
        self.last_nav_time = 0
        self.debounce_interval = 100  # milliseconds
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        button_width = int(300 * self.config.scale)
        button_height = int(70 * self.config.scale)
        margin = int(30 * self.config.scale)
        start_y = int(150 * self.config.scale)
        x = (self.config.screen_width - button_width) // 2
        self.buttons = []
        for i, (label, scene_key) in enumerate(self.menu_items):
            y = start_y + i * (button_height + margin)
            rect = (x, y, button_width, button_height)
            button = Button(
                rect,
                label,
                self.make_callback(scene_key),  # Helper to capture scene_key.
                self.font,
                normal_color=self.config.theme["button_normal_color"],
                selected_color=self.config.theme["button_selected_color"],
            )
            self.buttons.append(button)

    def make_callback(self, scene_key):
        """
        Helper function to create a callback that sets the scene.
        Using a default argument to capture the current value of scene_key.
        """
        return lambda sk=scene_key: self.scene_manager.set_scene(sk)

    def _process_navigation(self, key):
        if key in (pygame.K_w,):
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
        elif key in (pygame.K_s,):
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            self.buttons[self.selected_index].callback()

    def update(self):
        pass

    def draw(self, screen):
        title_text = "MAIN MENU"
        title_surface = self.font.render(
            title_text, True, self.config.theme["title_color"]
        )
        title_x = (self.config.screen_width - title_surface.get_width()) // 2
        screen.blit(title_surface, (title_x, int(40 * self.config.scale)))
        for i, button in enumerate(self.buttons):
            selected = i == self.selected_index
            button.draw(screen, selected)
            if selected:
                pygame.draw.rect(
                    screen, self.config.theme["highlight_color"], button.rect, 3
                )

    def on_input(self, event):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_nav_time < self.debounce_interval:
            return
        if event.type == pygame.KEYDOWN:
            self._process_navigation(event.key)
            self.last_nav_time = current_time
        elif event.type == pygame.TEXTINPUT:
            # TEXTINPUT events are ignored in favor of KEYDOWN navigation.
            pass