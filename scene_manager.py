# File: scene_manager.py
# Version: 2.2 (modified)
# Summary: Scene manager for handling scene transitions and centralized input.
#          Now uses dependency injection (receiving config and InputManager) and registers as an input handler.
# Tags: scene management, modular, input, dependency injection

import pygame

class SceneManager:
    def __init__(self, config, input_manager):
        self.config = config
        self.input_manager = input_manager
        self.scenes = {}
        self.current_scene = None
        # Register self with the input manager.
        self.input_manager.register_handler(self)

    def add_scene(self, name, scene):
        self.scenes[name] = scene
        # Optionally register the scene with the input manager.
        self.input_manager.register_handler(scene)

    def set_scene(self, name):
        if name in self.scenes:
            if self.current_scene:
                self.input_manager.unregister_handler(self.current_scene)
            self.current_scene = self.scenes[name]
            self.input_manager.register_handler(self.current_scene)
            if hasattr(self.current_scene, "on_enter"):
                self.current_scene.on_enter()

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)

    def on_global_input(self, event):
        # When a global input occurs (e.g., Q or Escape), return to the main menu.
        self.set_scene("menu")