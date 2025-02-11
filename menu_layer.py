# FileName: menu_layer.py
# version: 1.0 (modified)
# Summary: Provides the interactive menu layer (title and buttons) for the main menu.
# Tags: layers, menu, UI, modular

import pygame
import config  # Now using config.config
from ui_manager import Button

class MenuLayer:
    def __init__(self, scene_manager, font, menu_items):
        self.z = 4
        self.scene_manager = scene_manager
        self.font = font
        self.menu_items = menu_items  # List of (label, scene_key) tuples.
        self.selected_index = 0
        self.last_nav_time = 0
        self.debounce_interval = 100  # milliseconds
        self.buttons = []
        self.create_buttons()
    
    def create_buttons(self):
        button_width = int(300 * config.config.scale)
        button_height = int(70 * config.config.scale)
        margin = int(30 * config.config.scale)
        start_y = int(150 * config.config.scale)
        x = (config.config.screen_width - button_width) // 2
        self.buttons = []
        for i, (label, scene_key) in enumerate(self.menu_items):
            y = start_y + i * (button_height + margin)
            rect = (x, y, button_width, button_height)
            button = Button(
                rect,
                label,
                self.make_callback(scene_key),  # Using helper to capture scene_key.
                self.font,
                normal_color=config.config.theme["button_normal_color"],
                selected_color=config.config.theme["button_selected_color"]
            )
            self.buttons.append(button)
    
    def make_callback(self, scene_key):
        """
        Helper function to create a callback that sets the scene.
        Using a default argument to capture the current value of scene_key.
        """
        return lambda: self.scene_manager.set_scene(scene_key)
    
    def update(self):
        pass
    
    def draw(self, screen):
        title_text = "MAIN MENU"
        title_surface = self.font.render(title_text, True, config.config.theme["title_color"])
        title_x = (config.config.screen_width - title_surface.get_width()) // 2
        screen.blit(title_surface, (title_x, int(40 * config.config.scale)))
        for i, button in enumerate(self.buttons):
            selected = (i == self.selected_index)
            button.draw(screen, selected)
            if selected:
                pygame.draw.rect(screen, config.config.theme["highlight_color"], button.rect, 3)
    
    def on_input(self, event):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_nav_time < self.debounce_interval:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
                self.last_nav_time = current_time
            elif event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
                self.last_nav_time = current_time
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.buttons[self.selected_index].callback()
                self.last_nav_time = current_time
        elif event.type == pygame.TEXTINPUT:
            text = event.text.lower()
            if text == "w":
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
                self.last_nav_time = current_time
            elif text == "s":
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
                self.last_nav_time = current_time
            elif text in ("\r", "\n", " "):
                self.buttons[self.selected_index].callback()
                self.last_nav_time = current_time