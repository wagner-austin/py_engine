# FileName: main.py
# version: 1.2.2
# Summary: Main entry point for the application. Initializes pygame, sets screen scaling
#          using config.update_dimensions (so all modules import the correct values), and manages scene transitions.
# Tags: main, initialization, scene management, modular, layered

import pygame
import sys
import config
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
    
    # Immediately update the global screen dimensions and scale using the actual drawing surface size.
    config.update_dimensions(*screen.get_size())
    
    pygame.display.set_caption("Retro Menu Demo")
    config.FONT = pygame.font.SysFont(None, int(config.BASE_FONT_SIZE * config.SCALE))
    clock = pygame.time.Clock()

    # Start text input for on-screen keyboards.
    pygame.key.start_text_input()

    scene_manager = SceneManager()
    # Create and register scenes.
    menu_scene = MenuScene(scene_manager, config.FONT)
    test_scene = TestScene(scene_manager, config.FONT)
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
        clock.tick(config.FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()