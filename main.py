"""
main.py - Main entry point for the application. Initializes pygame, updates configuration,
sets up managers (InputManager, a shared LayerManager, and SceneManager), and runs the main loop.

Version: 1.5 (modified to use Play and Settings scenes)
"""

import pygame
import sys
from config import Config
from managers.scene_manager import SceneManager
from scenes.menu_scene import MenuScene
from scenes.play_scene import PlayScene
from scenes.settings_scene import SettingsScene
from managers.input_manager import InputManager
from managers.layer_manager import LayerManager
from layers.universal_layers import UniversalLayerFactory

def main() -> None:
    pygame.init()
    # Initialize text input once; it will be re-enabled on touch events.
    pygame.key.start_text_input()

    info = pygame.display.Info()

    # Retrieve initial dimensions from display info.
    initial_width: int = info.current_w
    initial_height: int = info.current_h

    # Set the display mode.
    screen: pygame.Surface = pygame.display.set_mode((initial_width, initial_height))

    # Instantiate configuration and update dimensions and scale.
    config: Config = Config()
    config.update_dimensions(*screen.get_size())

    pygame.display.set_caption("Retro Menu Demo")
    # Create font based on updated configuration.
    font: pygame.font.Font = pygame.font.SysFont(
        None, int(config.base_font_size * config.scale)
    )
    clock = pygame.time.Clock()

    # Create managers using dependency injection.
    input_manager = InputManager(config)
    layer_manager = LayerManager()
    universal_factory = UniversalLayerFactory()
    scene_manager = SceneManager(config, input_manager)

    # Create and register scenes.
    menu_scene = MenuScene(scene_manager, font, config, layer_manager, universal_factory)
    play_scene = PlayScene(font, config, layer_manager, universal_factory)
    settings_scene = SettingsScene(font, config, layer_manager, universal_factory)
    scene_manager.add_scene("menu", menu_scene)
    scene_manager.add_scene("play", play_scene)
    scene_manager.add_scene("settings", settings_scene)

    # Start with the main menu.
    scene_manager.set_scene("menu")

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                input_manager.process_event(event)

        scene_manager.update()
        scene_manager.draw(screen)

        pygame.display.flip()
        clock.tick(config.fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()