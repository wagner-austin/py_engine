"""
particle_effect_layer.py - Implements a plugin-based layer for spawning particles around the menu's selected button.
Version: 2.0.2
"""

import pygame
from typing import Optional
from plugins.plugins import register_layer
from .base_layer import BaseLayer
from core.config import Config
from effects.particle_effect import create_default_continuous_effect
from layers.menu_layer import MenuLayer

@register_layer("menu_particle_effect", "menu_only")
class MenuParticleEffectLayer(BaseLayer):
    def __init__(self, font: pygame.font.Font, config: Config, menu_layer: MenuLayer) -> None:
        """
        Initializes the MenuParticleEffectLayer with standardized constructor signature.
        Version: 2.0.2

        Parameters:
            font (pygame.font.Font): The font used for rendering.
            config (Config): The configuration object.
            menu_layer (MenuLayer): The associated menu layer.
        """
        self.font: pygame.font.Font = font
        self.config: Config = config
        self.menu_layer: MenuLayer = menu_layer
        self.z = 2
        self.persistent = False
        self.continuous_effect = create_default_continuous_effect(self.config)
        self.continuous_spawn_timer = 0.0
        self.continuous_spawn_interval = 0.2  # spawn interval in seconds
        self.last_selected_index: Optional[int] = self.menu_layer.selected_index

    def update(self, dt: float) -> None:
        self.continuous_effect.update(dt)
        current_index = self.menu_layer.selected_index
        if current_index != self.last_selected_index:
            new_button = self.menu_layer.buttons[current_index]
            self.continuous_effect.spawn_continuous_from_rect(new_button.rect)
            self.last_selected_index = current_index
        self.continuous_spawn_timer += dt
        if self.continuous_spawn_timer >= self.continuous_spawn_interval:
            current_button = self.menu_layer.buttons[self.last_selected_index]
            self.continuous_effect.spawn_continuous_from_rect(current_button.rect)
            self.continuous_spawn_timer = 0.0

    def draw(self, screen: pygame.Surface) -> None:
        self.continuous_effect.draw(screen)

    def on_input(self, event: pygame.event.Event) -> None:
        pass