# FileName: main.py
# version: 1.3
# Summary: Main entry point for the application. Initializes pygame, updates configuration,
#          sets up managers (InputManager, UIManager, LayerManager, SceneManager), and runs the main loop.
# Tags: main, initialization, dependency injection, modular

import pygame
import sys
import config  # Using config.config
from scene_manager import SceneManager
from scenes.menu_scene import MenuScene
from scenes.test_scene import TestScene
from input_manager import InputManager
from ui_manager import UIManager
from layer_manager import LayerManager

def main():
    pygame.init()
    info = pygame.display.Info()
    
    # Retrieve initial dimensions from display info.
    initial_width = info.current_w
    initial_height = info.current_h

    # Set the display mode.
    screen = pygame.display.set_mode((initial_width, initial_height))
    
    # Update configuration dimensions and scale.
    config.config.update_dimensions(*screen.get_size())
    
    pygame.display.set_caption("Retro Menu Demo")
    # Create font based on updated configuration.
    font = pygame.font.SysFont(None, int(config.config.base_font_size * config.config.scale))
    clock = pygame.time.Clock()

    # Start text input for on-screen keyboards.
    pygame.key.start_text_input()

    # Create managers using dependency injection.
    input_manager = InputManager()
    ui_manager = UIManager()       # Available for UI elements.
    layer_manager = LayerManager() # Available for managing scene layers.
    scene_manager = SceneManager(config.config, input_manager)

    # Create and register scenes.
    menu_scene = MenuScene(scene_manager, font, config.config)
    test_scene = TestScene(scene_manager, font, config.config)
    scene_manager.add_scene("menu", menu_scene)
    scene_manager.add_scene("test", test_scene)
    
    # Start with the main menu.
    scene_manager.set_scene("menu")
    
    running = True
    while running:
        # Process input events through the InputManager.
        input_manager.process_events()
    
        scene_manager.update()
        scene_manager.draw(screen)
    
        pygame.display.flip()
        clock.tick(config.config.fps)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()