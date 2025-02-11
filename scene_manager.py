# FileName: scene_manager.py
# version: 2.1
# Summary: Scene manager for handling scene transitions and centralized input handling.
#          Any KEYDOWN event for Q or Escape immediately returns to the main menu.
# Tags: scene management, modular, central input handling, on_enter, text input, mobile, desktop

import pygame

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
        if name in self.scenes:
            self.current_scene = self.scenes[name]
            if hasattr(self.current_scene, "on_enter"):
                self.current_scene.on_enter()

    def handle_event(self, event):
        # Centralized input: Q or Escape returns to the main menu.
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
            self.set_scene("menu")
            return  # Do not process further.
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)