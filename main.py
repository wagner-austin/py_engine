"""
main.py - Main entry point for the application.
Version: 1.5.3
Summary: Initializes pygame, loads plugins, creates managers, and registers scenes.
"""

import pygame
import sys
from core.config import Config
from managers.scene_manager import SceneManager
from managers.input_manager import InputManager
from managers.layer_manager import LayerManager
from plugins.plugin_loader import load_all_plugins
from plugins.plugins import layer_registry  # Import the registry for debugging

# -----------------------------------------------------------------------------
# Load all plugin modules so that plugin registrations are executed.
PLUGIN_PACKAGES = [
    "layers",    # Layers (art layers, border, instruction, etc.)
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
initial_width = info.current_w
initial_height = info.current_h

screen = pygame.display.set_mode((initial_width, initial_height))
config = Config()
config.update_dimensions(*screen.get_size())

pygame.display.set_caption("Retro Menu Demo")
font = pygame.font.SysFont(None, int(config.base_font_size * config.scale))
clock = pygame.time.Clock()

# -----------------------------------------------------------------------------
# Create managers.
input_manager = InputManager(config)
layer_manager = LayerManager()
scene_manager = SceneManager(config, input_manager)

# -----------------------------------------------------------------------------
# Debug: Print the layer registry contents at startup.
#print("=== Main: Layer registry at startup ===")
#if layer_registry:
#    for key, info in layer_registry.items():
#        print(f"Layer key: '{key}', category: '{info['category']}', class: {info['class']}")
#else:
#    print("Layer registry is empty!")
#print("========================================")

# -----------------------------------------------------------------------------
# Create and register scenes.
from scenes.menu_scene import MenuScene
from scenes.play_scene import PlayScene
from scenes.settings_scene import SettingsScene

menu_scene = MenuScene(scene_manager, font, config, layer_manager)
play_scene = PlayScene(font, config, layer_manager)
settings_scene = SettingsScene(scene_manager, font, config, layer_manager)

scene_manager.add_scene("menu", menu_scene)
scene_manager.add_scene("play", play_scene)
scene_manager.add_scene("settings", settings_scene)

# Start with the main menu.
scene_manager.set_scene("menu")

# -----------------------------------------------------------------------------
# Main loop.
running = True
while running:
    dt = clock.tick(config.fps) / 1000.0  # Delta time in seconds.
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