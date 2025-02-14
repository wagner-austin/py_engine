"""
particle_effect_layer.py
------------------------
Implements a plugin-based layer for spawning particles around the menu's selected button.
Version: 2.0.0
"""

import pygame
from typing import Optional
from plugins import register_layer
from layers.base_layer import BaseLayer
from config import Config

# We'll re‑use the default continuous effect factory.
from effects.particle_effect import create_default_continuous_effect
from layers.menu_layer import MenuLayer

@register_layer("menu_particle_effect", "menu_only")
class MenuParticleEffectLayer(BaseLayer):
    """
    A plugin-based layer that replicates the old MenuLayer's embedded particle logic.
    It spawns and draws gentle falling particles around whichever button is selected.
    """

    def __init__(self, config: Config, menu_layer: MenuLayer) -> None:
        """
        Initializes the MenuParticleEffectLayer with the provided configuration and reference
        to the MenuLayer, so we can know which button is selected.

        Parameters:
            config (Config): The configuration object for application settings.
            menu_layer (MenuLayer): The menu layer whose selected_index and buttons we'll track.
        """
        self.config: Config = config
        self.menu_layer: MenuLayer = menu_layer

        # Z-index: place it above the star_art but below borders, typically.
        self.z = 2  
        self.persistent = False

        # Create the continuous particle effect (same as old menu code).
        self.continuous_effect = create_default_continuous_effect()
        self.continuous_spawn_timer = 0.0
        self.continuous_spawn_interval = 0.2  # spawn interval in seconds

        # Track the last known selected_index, so we can detect selection changes.
        self.last_selected_index: Optional[int] = self.menu_layer.selected_index

    def update(self, dt: float) -> None:
        """
        Updates the continuous particle effect and spawns new particles.

        - If the user has moved the selection from one button to another, spawn an immediate
          burst of particles around the newly selected button.
        - Every 0.2 seconds, spawn a gentle group of particles around the current button rect.
        - Update the internal particle system's states and lifetimes.
        """
        self.continuous_effect.update(dt)

        current_index = self.menu_layer.selected_index
        if current_index != self.last_selected_index:
            # The user just changed selection, so spawn extra particles around the new button.
            new_button = self.menu_layer.buttons[current_index]
            self.continuous_effect.spawn_continuous_from_rect(new_button.rect)
            self.last_selected_index = current_index

        self.continuous_spawn_timer += dt
        if self.continuous_spawn_timer >= self.continuous_spawn_interval:
            # Spawn more particles around the currently selected button.
            current_button = self.menu_layer.buttons[self.last_selected_index]
            self.continuous_effect.spawn_continuous_from_rect(current_button.rect)
            self.continuous_spawn_timer = 0.0

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the particle effect onto the provided screen.

        Parameters:
            screen (pygame.Surface): The pygame surface on which to render the effect.
        """
        self.continuous_effect.draw(screen)

    def on_input(self, event: pygame.event.Event) -> None:
        """
        Processes input events. Currently, this particle layer doesn't handle input.

        Parameters:
            event (pygame.event.Event): The input event to process.
        """
        pass