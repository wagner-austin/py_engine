# FileName: main.py
# version: 1.2.3 (modified to work with new config structure)
# Summary: Main entry point for the application. Initializes pygame, updates configuration dimensions,
#          sets up the scene manager and scenes, and runs the main loop.
# Tags: main, initialization, scene management, modular, layered

import pygame
import sys
import config  # Now using config.config for configuration values.
from scene_manager import SceneManager
from scenes.menu_scene import MenuScene
from scenes.test_scene import TestScene

def main():
    pygame.init()
    info = pygame.display.Info()
    
    # Retrieve initial dimensions from display info.
    initial_width = info.current_w
    initial_height = info.current_h

    # Set the display mode.
    screen = pygame.display.set_mode((initial_width, initial_height))
    
    # Immediately update the global configuration dimensions and scale using the actual drawing surface size.
    config.config.update_dimensions(*screen.get_size())
    
    pygame.display.set_caption("Retro Menu Demo")
    # Create font based on updated configuration
    font = pygame.font.SysFont(None, int(config.config.base_font_size * config.config.scale))
    clock = pygame.time.Clock()

    # Start text input for on-screen keyboards.
    pygame.key.start_text_input()

    scene_manager = SceneManager()
    # Create and register scenes.
    menu_scene = MenuScene(scene_manager, font)
    test_scene = TestScene(scene_manager, font)
    scene_manager.add_scene("menu", menu_scene)
    scene_manager.add_scene("test", test_scene)
    
    # Start with the main menu.
    scene_manager.set_scene("menu")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene_manager.handle_event(event)
    
        scene_manager.update()
        scene_manager.draw(screen)
    
        pygame.display.flip()
        clock.tick(config.config.fps)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()