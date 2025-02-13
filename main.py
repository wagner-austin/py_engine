"""
main.py
Version: 1.5
Summary: Main entry point for the application. Initializes pygame, updates configuration,
         sets up managers (InputManager, LayerManager, and SceneManager), loads all plugin modules,
         creates and registers scenes, and runs the main loop.
"""

import pygame
import sys
from config import Config
from managers.scene_manager import SceneManager
from managers.input_manager import InputManager
from managers.layer_manager import LayerManager
from layers.universal_layers import UniversalLayerFactory

# -----------------------------------------------------------------------------
# Load all plugin modules so that their decorators (and hence plugin registrations)
# are executed. This eliminates the need for redundant direct imports solely to trigger
# registration.
from plugin_loader import load_all_plugins

PLUGIN_PACKAGES = [
    "layers",    # Universal layers (art layers, border, instruction, etc.)
    "effects",   # Effect layers (snow, rain, etc.)
    "scenes",    # Scene definitions
    "themes",    # Theme definitions
]
load_all_plugins(PLUGIN_PACKAGES)

# -----------------------------------------------------------------------------
# Initialize pygame and update configuration.
pygame.init()
pygame.key.start_text_input()

info = pygame.display.Info()
initial_width: int = info.current_w
initial_height: int = info.current_h

screen: pygame.Surface = pygame.display.set_mode((initial_width, initial_height))

config: Config = Config()
config.update_dimensions(*screen.get_size())

pygame.display.set_caption("Retro Menu Demo")
font: pygame.font.Font = pygame.font.SysFont(None, int(config.base_font_size * config.scale))
clock = pygame.time.Clock()

# -----------------------------------------------------------------------------
# Create managers.
input_manager = InputManager(config)
layer_manager = LayerManager()
universal_factory = UniversalLayerFactory()
scene_manager = SceneManager(config, input_manager)

# -----------------------------------------------------------------------------
# Create and register scenes.
from scenes.menu_scene import MenuScene
from scenes.play_scene import PlayScene
from scenes.settings_scene import SettingsScene

menu_scene = MenuScene(scene_manager, font, config, layer_manager, universal_factory)
play_scene = PlayScene(font, config, layer_manager, universal_factory)
settings_scene = SettingsScene(font, config, layer_manager, universal_factory)

scene_manager.add_scene("menu", menu_scene)
scene_manager.add_scene("play", play_scene)
scene_manager.add_scene("settings", settings_scene)

# Start with the main menu.
scene_manager.set_scene("menu")

# -----------------------------------------------------------------------------
# Main loop.
running: bool = True
while running:
    dt = clock.tick(config.fps) / 1000.0  # Actual delta time in seconds.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            input_manager.process_event(event)

    scene_manager.update(dt)
    scene_manager.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()