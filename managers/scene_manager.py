"""
managers/scene_manager.py - Scene manager for handling scene transitions, back navigation, and centralized mouse/touch input.
Version: 1.1.6
Summary: Manages scenes and transitions. Adds a global directional control layer via the plugin system,
         ensuring that all scenes use a unified mouse/touch-based input method.
"""

import pygame
from typing import Dict, Optional
from core.config import Config
from managers.input_manager import InputManager
from scenes.base_scene import BaseScene
from plugins.plugins import transition_registry, layer_registry
from transitions.transitions import Transition  # For proper type annotation

class SceneManager:
    def __init__(self, config: Config, input_manager: InputManager) -> None:
        """
        scene_manager.py - Initializes the SceneManager.
        Version: 1.1.6
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
        scene_manager.py - Registers a scene with a given name.
        Version: 1.1.5
        """
        self.scenes[name] = scene

    def set_scene(self, name: str, transition_type: Optional[str] = None, duration: float = 1.0, push_history: bool = True) -> None:
        """
        scene_manager.py - Sets the active scene.
        Version: 1.1.5
        Summary: Switches scenes (pushing the current scene key to history when appropriate) and populates the new scene.
                 Additionally, if global controls are enabled, adds the directional button layer via the plugin system.
        """
        if name not in self.scenes:
            return

        new_scene = self.scenes[name]
        new_scene.on_enter()  # Scene populates its layers

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

        # --- Add global directional control layer via plugin system if enabled ---
        if self.config.enable_global_controls:
            if "directional_button_layer" in layer_registry:
                directional_cls = layer_registry["directional_button_layer"]["class"]
                def global_callback(direction: str, pressed: bool):
                    # Directly handle directional input via mouse/touch
                    if direction == "B" and pressed:
                        # Handle back navigation directly using a visible on-screen control
                        if self.history:
                            previous_scene = self.history.pop()
                            self.set_scene(previous_scene, push_history=False)
                        else:
                            self.set_scene("menu", push_history=False)
                    else:
                        # Forward the directional input to the current scene if it implements on_directional_input
                        if self.current_scene and hasattr(self.current_scene, "on_directional_input"):
                            self.current_scene.on_directional_input(direction, pressed)
                global_layer = directional_cls(self.current_scene.font, self.config, global_callback)
                global_layer.z = 999  # Ensure the layer is drawn on top.
                self.current_scene.layer_manager.add_layer(global_layer)
            else:
                print("Global directional control layer plugin not registered; skipping global directional layer.")

    def update(self, dt: float = None) -> None:
        """
        scene_manager.py - Updates the current scene or active transition.
        Version: 1.1.5
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
        scene_manager.py - Draws the current scene or active transition.
        Version: 1.1.5
        """
        if self.transition:
            self.transition.draw(screen)
        elif self.current_scene:
            self.current_scene.draw(screen)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        scene_manager.py - Forwards input events to the current scene.
        Version: 1.1.5
        """
        if self.current_scene:
            self.current_scene.on_input(event)

# End of managers/scene_manager.py