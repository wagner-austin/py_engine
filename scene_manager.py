"""
scene_manager.py - Scene manager for handling scene transitions and centralized input.

Version: 1.0
"""

import pygame

class SceneManager:
    """
    Manages scenes, handles transitions, and dispatches input events.
    """

    def __init__(self, config, input_manager):
        """
        Initializes the SceneManager.

        Parameters:
            config: Global configuration object.
            input_manager: An InputManager instance responsible for dispatching events.
        """
        self.config = config
        self.input_manager = input_manager
        self.scenes = {}
        self.current_scene = None
        # Register self with the input manager.
        self.input_manager.register_handler(self)

    def add_scene(self, name, scene):
        """
        Adds a scene to the manager (scenes are not automatically registered).

        Parameters:
            name: The key under which to store the scene.
            scene: The scene instance.
        """
        self.scenes[name] = scene

    def _register_scene(self, scene):
        """
        Registers a scene with the input manager.
        If the scene has an on_enter() method, it is called before registration.

        Parameters:
            scene: The scene instance to register.
        """
        if hasattr(scene, "on_enter"):
            scene.on_enter()
        self.input_manager.register_handler(scene)

    def _unregister_scene(self, scene):
        """
        Unregisters a scene from the input manager.

        Parameters:
            scene: The scene instance to unregister.
        """
        self.input_manager.unregister_handler(scene)

    def set_scene(self, name):
        """
        Switches the active scene.
        Unregisters the old scene, repopulates layers for the new scene (if applicable),
        and registers the new scene using the helper methods.

        Parameters:
            name: The key of the scene to switch to.
        """
        if name in self.scenes:
            if self.current_scene:
                self._unregister_scene(self.current_scene)
            self.current_scene = self.scenes[name]
            if hasattr(self.current_scene, "populate_layers"):
                self.current_scene.populate_layers()
            self._register_scene(self.current_scene)

    def update(self) -> None:
        """
        Updates the currently active scene.
        """
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen) -> None:
        """
        Draws the currently active scene onto the provided screen.

        Parameters:
            screen: The pygame Surface on which to draw.
        """
        if self.current_scene:
            self.current_scene.draw(screen)

    def on_global_input(self, event) -> None:
        """
        Handles global input events (e.g., Escape or Q) by returning to the main menu.

        Parameters:
            event: The pygame event triggering the global input.
        """
        self.set_scene("menu")