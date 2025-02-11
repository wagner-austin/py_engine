# FileName: documentation.py
# version: 1.0
# Summary: Provides an overview of the project structure, describing the purpose of each file,
#          and instructions for adding new scenes, modifying the border, adding new layers, and
#          changing settings or implementing additional features.
# Tags: documentation, project guide, developer reference, modular, layers, scenes

"""
PROJECT DOCUMENTATION & DEVELOPER REFERENCE

Project Structure:
------------------

1. config.py
   - Purpose:
       Contains global configuration settings such as the base resolution (BASE_WIDTH, BASE_HEIGHT),
       FPS, BASE_FONT_SIZE, and universal theme settings in the THEME dictionary.
   - How to Change Settings:
       Modify values such as FPS, BASE_FONT_SIZE, or any color settings in THEME.
       Adjust scaling factors (config.SCALE) are calculated in main.py based on these values.

2. main.py
   - Purpose:
       The main entry point for the application. It initializes pygame, sets screen scaling,
       creates the SceneManager, loads scenes, and runs the main loop.
   - How to Add New Scenes:
       Import your new scene module and add your scene instance to the SceneManager with:
         scene_manager.add_scene("my_scene", my_scene_instance)
       Then call scene_manager.set_scene("my_scene") to switch to it.
   - Note:
       This file ties together all modules and starts the application.

3. scene_manager.py
   - Purpose:
       Manages scene transitions, updates, and drawing. It also centralizes input handling
       (e.g., pressing Q or Escape returns to the main menu).
   - How to Add/Modify Scenes:
       Use add_scene() to register new scenes and set_scene() to change the active scene.

4. base_scene.py
   - Purpose:
       Provides the BaseScene class that all scene classes should inherit from. It defines common
       methods for input handling, updating layers, and drawing layers in a defined order.
   - How to Extend:
       Create a new scene class that inherits from BaseScene and override on_input(), update(), and draw()
       as needed. Use the layers system to add or remove visual components.

5. ui_manager.py
   - Purpose:
       Contains UI elements such as the Button class, which is used for interactive elements.
   - How to Use:
       Create buttons by instantiating Button with a rectangle, label, callback, font, and optional colors.
       Use these buttons in your scene layers for interactive controls.

6. art_assets.py
   - Purpose:
       Contains ASCII art assets (e.g., STAR_ART, CROCODILE, etc.). These arrays can be updated to change the artwork.
   - How to Update:
       Modify the art arrays to include your desired artwork. These assets are referenced by the art layer modules.

7. art_layers.py
   - Purpose:
       Provides art-related layers such as StarArtLayer and CrocodileLayer. StarArtLayer renders the star art
       background, stretching it horizontally and vertically. CrocodileLayer renders crocodile ASCII art.
   - How to Modify:
       Change the rendering logic or the colors inside these classes. For example, adjust the stretching algorithm
       in stretch_line() or change the color passed to font.render().

8. effect_layers.py
   - Purpose:
       Provides effect layers such as RainEffectLayer, which animates falling rain.
   - How to Modify:
       Change parameters (like the number of rain lines, speed, or color) to alter the rain effect.

9. instruction_layer.py
   - Purpose:
       Displays on-screen instructions (e.g., which keys to press) using a fixed text string.
   - How to Modify:
       Change the instruction text or style (color, font, position) within this file.

10. menu_layer.py
    - Purpose:
        Provides the interactive menu layer. It displays the title and buttons, and handles input
        (using W/S to navigate and Enter/Space to select).
    - How to Modify:
        Update the menu_items list or change the appearance and behavior of the buttons.
        This is where you can adjust the menu’s interactive features.

11. border_layer.py
    - Purpose:
        Draws a border around the screen.
    - How to Modify:
        Change the border color by updating config.THEME["border_color"] in config.py or directly in BorderLayer.
        Adjust thickness by modifying the self.thickness value in BorderLayer.
        The border is drawn inside the screen bounds (width and height reduced by 1) so that the bottom edge remains visible.

12. universal_layers.py
    - Purpose:
        Aggregates universal layers by importing individual layer modules (from art_layers.py, effect_layers.py,
        instruction_layer.py, and border_layer.py) and returning them as a list via get_universal_layers(font).
    - How to Modify:
        To change the composition or order of universal layers, update the list returned by get_universal_layers().
        To add a new universal layer, create a new module for it and add its instance to this list.

13. scenes/menu_scene.py
    - Purpose:
        Implements the main menu scene using a layered system. It combines the universal layers with an interactive
        menu layer (MenuLayer).
    - How to Modify:
        Add or change menu items in the menu_items list. For further customization, modify or add additional layers.
        The scene’s input is forwarded to the highest z-index layer that implements an on_input() method.

14. scenes/test_scene.py
    - Purpose:
        A simple test scene to verify that scene switching and layered rendering work properly.
    - How to Use:
        Use this as a template for creating additional scenes. It combines the universal layers with a custom TestLayer.
    - How to Modify:
        Edit TestLayer to display your test content, or create new scene-specific layers.

Adding New Scenes:
------------------
1. Create a new file in the scenes/ directory (e.g., scenes/my_new_scene.py) that inherits from BaseScene.
2. Implement the on_input(), update(), and draw() methods as needed.
3. Optionally, create custom layers for unique effects or UI elements.
4. In main.py, import your new scene and register it with the SceneManager using:
       scene_manager.add_scene("my_new_scene", my_new_scene_instance)
5. Switch to your new scene with scene_manager.set_scene("my_new_scene").

Modifying the Border:
---------------------
- Open border_layer.py and change properties:
    • To change color, update self.border_color (or change config.THEME["border_color"] in config.py).
    • To change thickness, modify self.thickness.
- The border is drawn using pygame.draw.rect() with the rectangle defined as (0, 0, config.SCREEN_WIDTH - 1, config.SCREEN_HEIGHT - 1)
  to ensure the bottom line is visible.

Adding New Layers:
------------------
1. Create a new module (e.g., my_new_layer.py) that defines a layer class.
    • Your layer class should have a 'z' attribute, update(), and draw() methods.
2. If your layer requires input handling, implement an on_input() method.
3. Import your new layer in universal_layers.py (or in your scene file) and add an instance to the list of layers.
4. Your new layer will then be drawn (or updated) automatically in the order determined by its z-index.

Changing Settings:
------------------
- Edit config.py for any universal settings, such as screen dimensions, FPS, font size, or theme colors.
- These settings are used throughout the project to ensure consistency.

Implementing Additional Features:
----------------------------------
- Follow the existing file structure and create new modules for new features.
- Use the UI elements in ui_manager.py for interactive components.
- Update universal_layers.py to include any new layers you create.
- Document your changes in this file (documentation.py) so future developers have a clear understanding.

This file serves as a reference guide to help you navigate and extend the project. It’s recommended to update
this documentation as you add new features or modify the architecture.

To view this documentation from the command line, simply run:
    python documentation.py
"""

if __name__ == "__main__":
    print(__doc__)