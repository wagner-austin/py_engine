"""
scene_manager.py - Scene manager for handling scene transitions and centralized input.
Version: 1.1.2
"""

import pygame
from typing import Dict, Optional
from core.config import Config
from managers.input_manager import InputManager
from scenes.base_scene import BaseScene
from plugins.plugins import transition_registry
from transitions.transitions import Transition  # For proper type annotation

class SceneManager:
    """
    Manages scenes, handles transitions, and centralizes input dispatch.
    """
    def __init__(self, config: Config, input_manager: InputManager) -> None:
        """
        Initializes the SceneManager with the provided configuration and input manager.

        Parameters:  
            config (Config): The global configuration object.  
            input_manager (InputManager): The input manager responsible for event handling.  
        """
        self.config: Config = config
        self.input_manager: InputManager = input_manager
        self.scenes: Dict[str, BaseScene] = {}
        self.current_scene: Optional[BaseScene] = None
        self.transition: Optional[Transition] = None  # Active transition instance (if any)
        self.input_manager.register_handler(self)

    def add_scene(self, name: str, scene: BaseScene) -> None:
        """
        Registers a scene with a given name.

        Parameters:  
            name (str): The key for the scene.
            scene (BaseScene): The scene instance.
        """
        self.scenes[name] = scene

    def set_scene(self, name: str, transition_type: Optional[str] = None, duration: float = 1.0) -> None:
        """
        Sets the active scene. Relies on the scene's on_enter() method to populate layers dynamically.

        Parameters:  
            name (str): The key of the scene to activate.
            transition_type (Optional[str]): The type of transition to use (default is ACTIVE_TRANSITION).
            duration (float): The duration of the transition in seconds.
        """
        if name not in self.scenes:
            return

        new_scene = self.scenes[name]
        new_scene.on_enter()  # on_enter() will perform dynamic initialization (including populate_layers)

        if self.current_scene is not None:
            if transition_type is None:
                from transitions.transitions import ACTIVE_TRANSITION
                transition_type = ACTIVE_TRANSITION
            transition_creator = transition_registry.get(transition_type.lower())
            if transition_creator:
                self.transition = transition_creator(self.current_scene, new_scene, self.config, duration)
                self.current_scene = new_scene
            else:
                self.current_scene = new_scene
        else:
            self.current_scene = new_scene

    def update(self, dt: float = None) -> None:
        """
        Updates the current scene or active transition based on the elapsed time.

        Parameters:  
            dt (float): Delta time in seconds. Defaults to 1.0 / fps if not provided.
        """
        if dt is None:
            dt = 1.0 / self.config.fps

        if self.transition:
            self.transition.update(dt)
            if self.transition.is_complete():
                self.transition = None
        elif self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the current scene or active transition onto the provided screen.

        Parameters:  
            screen (pygame.Surface): The surface on which to draw the scene.
        """
        if self.transition:
            self.transition.draw(screen)
        elif self.current_scene:
            self.current_scene.draw(screen)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Forwards input events to the current scene regardless of an active transition.

        Parameters:  
            event (pygame.event.Event): The input event to process.
        """
        if self.current_scene:
            self.current_scene.on_input(event)

    def on_global_input(self, event: pygame.event.Event) -> None:
        """
        Handles global input events by switching to the main menu.

        Parameters:  
            event (pygame.event.Event): The global input event.
        """
        self.set_scene("menu")