"""
scene_manager.py - Scene manager for handling scene transitions and centralized input.
"""

import pygame
from typing import Dict, Optional
from config import Config
from managers.input_manager import InputManager
from scenes.base_scene import BaseScene
from plugins import transition_registry
from transitions import Transition  # New import for proper type annotation

class SceneManager:
    """
    Manages scenes, handles transitions, and centralizes input dispatch.
    """
    def __init__(self, config: Config, input_manager: InputManager) -> None:
        self.config: Config = config
        self.input_manager: InputManager = input_manager
        self.scenes: Dict[str, BaseScene] = {}
        self.current_scene: Optional[BaseScene] = None
        self.transition: Optional[Transition] = None  # Now properly typed as a Transition instance
        self.input_manager.register_handler(self)

    def add_scene(self, name: str, scene: BaseScene) -> None:
        self.scenes[name] = scene

    def set_scene(self, name: str, transition_type: Optional[str] = None, duration: float = 1.0) -> None:
        if name not in self.scenes:
            return

        new_scene = self.scenes[name]
        new_scene.populate_layers()
        new_scene.on_enter()

        if self.current_scene is not None:
            # If no transition type is provided, use the active transition from transitions.py.
            if transition_type is None:
                from transitions import ACTIVE_TRANSITION
                transition_type = ACTIVE_TRANSITION
            # Look up the transition plugin from the central registry.
            transition_creator = transition_registry.get(transition_type.lower())
            if transition_creator:
                self.transition = transition_creator(self.current_scene, new_scene, self.config, duration)
                self.current_scene = new_scene
            else:
                self.current_scene = new_scene
        else:
            self.current_scene = new_scene

    def update(self, dt: float = None) -> None:
        if dt is None:
            dt = 1.0 / self.config.fps

        if self.transition:
            self.transition.update(dt)
            if self.transition.is_complete():
                self.transition = None
        elif self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        if self.transition:
            self.transition.draw(screen)
        elif self.current_scene:
            self.current_scene.draw(screen)

    def on_input(self, event: pygame.event.Event) -> None:
        if self.transition:
            # Optionally, handle input during a transition if desired.
            pass
        elif self.current_scene:
            self.current_scene.on_input(event)

    def on_global_input(self, event: pygame.event.Event) -> None:
        self.set_scene("menu")