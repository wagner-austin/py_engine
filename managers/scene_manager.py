"""
scene_manager.py - Scene manager for handling scene transitions, maintaining history for back navigation, and centralized input.
Version: 1.1.4
Summary: Manages scenes, handles transitions, maintains a scene history for back navigation, and centralizes input dispatch.
         Now pressing Q/Esc will return to the previous scene (if available) rather than always going to the home scene.
         Back navigation is implemented using a push_history parameter to prevent cycling back to the same scene.
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
    Manages scenes, handles transitions, maintains a scene history for back navigation, and centralizes input dispatch.
    """
    def __init__(self, config: Config, input_manager: InputManager) -> None:
        """
        Initializes the SceneManager with the provided configuration and input manager.
        Version: 1.1.4
        """
        self.config: Config = config
        self.input_manager: InputManager = input_manager
        self.scenes: Dict[str, BaseScene] = {}
        self.current_scene: Optional[BaseScene] = None
        self.current_scene_key: Optional[str] = None
        self.history: list[str] = []  # History of scene keys for back navigation
        self.transition: Optional[Transition] = None  # Active transition instance (if any)
        self.input_manager.register_handler(self)

    def add_scene(self, name: str, scene: BaseScene) -> None:
        """
        Registers a scene with a given name.
        Version: 1.1.4
        """
        self.scenes[name] = scene

    def set_scene(self, name: str, transition_type: Optional[str] = None, duration: float = 1.0, push_history: bool = True) -> None:
        """
        Sets the active scene. Relies on the scene's on_enter() method to populate layers dynamically.
        Version: 1.1.4
        Summary: When switching scenes normally, pushes the current scene key to history. When back navigating,
                 push_history should be False so that the current scene is not re-added.
        """
        if name not in self.scenes:
            return

        new_scene = self.scenes[name]
        new_scene.on_enter()  # on_enter() will perform dynamic initialization (including populate_layers)

        # Only push current scene key if desired.
        if push_history and self.current_scene_key is not None:
            self.history.append(self.current_scene_key)

        if self.current_scene is not None:
            if transition_type is None:
                from transitions.transitions import ACTIVE_TRANSITION
                transition_type = ACTIVE_TRANSITION
            transition_creator = transition_registry.get(transition_type.lower())
            if transition_creator:
                self.transition = transition_creator(self.current_scene, new_scene, self.config, duration)
                self.current_scene = new_scene
                self.current_scene_key = name
            else:
                self.current_scene = new_scene
                self.current_scene_key = name
        else:
            self.current_scene = new_scene
            self.current_scene_key = name

    def update(self, dt: float = None) -> None:
        """
        Updates the current scene or active transition based on the elapsed time.
        Version: 1.1.4
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
        Version: 1.1.4
        """
        if self.transition:
            self.transition.draw(screen)
        elif self.current_scene:
            self.current_scene.draw(screen)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Forwards input events to the current scene regardless of an active transition.
        Version: 1.1.4
        """
        if self.current_scene:
            self.current_scene.on_input(event)

    def on_global_input(self, event: pygame.event.Event) -> None:
        """
        Handles global input events by returning to the previous scene if available.
        Version: 1.1.4
        Summary: Pressing Q/Esc will pop the last scene from history and set it as current without pushing the current scene onto history.
                 For example, if in Play scene, pressing Q goes to Game Mode Selection; pressing Q again goes to Home.
        """
        if self.history:
            previous_scene = self.history.pop()
            self.set_scene(previous_scene, push_history=False)
        else:
            # Fallback if no history, return to home scene.
            self.set_scene("menu", push_history=False)