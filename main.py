# File: main.py
# Version: 1.5 (modified for touch keyboard support)
# Summary: Main entry point for the application. Initializes pygame, updates configuration,
#          sets up managers (InputManager, LayerManager, SceneManager), and runs the main loop.
#          Now supports continuous text input checks and touch screen events to trigger the on-screen keyboard.
# Tags: main, initialization, dependency injection, modular

import pygame
import sys
from config import GLOBAL_CONFIG
from scene_manager import SceneManager
from scenes.menu_scene import MenuScene
from scenes.test_scene import TestScene
from input_manager import InputManager
from layer_manager import LayerManager

def main():
    pygame.init()
    # Initialize text input once; it will be re-enabled on touch events.
    pygame.key.start_text_input()

    info = pygame.display.Info()

    # Retrieve initial dimensions from display info.
    initial_width = info.current_w
    initial_height = info.current_h

    # Set the display mode.
    screen = pygame.display.set_mode((initial_width, initial_height))

    # Update configuration dimensions and scale.
    GLOBAL_CONFIG.update_dimensions(*screen.get_size())

    pygame.display.set_caption("Retro Menu Demo")
    # Create font based on updated configuration.
    font = pygame.font.SysFont(
        None, int(GLOBAL_CONFIG.base_font_size * GLOBAL_CONFIG.scale)
    )
    clock = pygame.time.Clock()

    # Create managers using dependency injection.
    input_manager = InputManager()
    # Removed UIManager instantiation as it was unused.
    layer_manager = LayerManager()  # Available for managing scene layers.
    scene_manager = SceneManager(GLOBAL_CONFIG, input_manager)

    # Create and register scenes.
    menu_scene = MenuScene(scene_manager, font, GLOBAL_CONFIG)
    test_scene = TestScene(scene_manager, font, GLOBAL_CONFIG)
    scene_manager.add_scene("menu", menu_scene)
    scene_manager.add_scene("test", test_scene)

    # Start with the main menu.
    scene_manager.set_scene("menu")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                input_manager.process_event(event)

        scene_manager.update()
        scene_manager.draw(screen)

        pygame.display.flip()
        clock.tick(GLOBAL_CONFIG.fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()