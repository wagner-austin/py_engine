"""
plugins.py - Central plugin registries for scenes, layers, effects, themes, transitions, and play modes.
Version: 1.3.2
Summary: Added play_mode_registry and register_play_mode for plug-and-play play mode integration.
"""

# Plugin registries
scene_registry = {}
layer_registry = {}   # Unified registry for all layers
effect_registry = {}
theme_registry = {}
transition_registry = {}

def register_scene(key: str):
    """
    Decorator to register a scene class with a given key.
    Version: 1.3.2
    """
    def decorator(cls):
        scene_registry[key.lower()] = cls
        return cls
    return decorator

def register_layer(key: str, category: str = "foreground"):
    """
    Decorator to register a layer class with a given key and optional category.
    Version: 1.3.2
    """
    def decorator(cls):
        layer_registry[key.lower()] = {
            "class": cls,
            "category": category.lower()
        }
        return cls
    return decorator

def register_effect(key: str):
    """
    Decorator to register an effect layer class with a given key.
    Version: 1.3.2
    """
    def decorator(cls):
        effect_registry[key.lower()] = cls
        return cls
    return decorator

def register_theme(key: str):
    """
    Decorator to register a theme with a given key.
    Version: 1.3.2
    """
    def decorator(func):
        theme_registry[key.lower()] = func()
        return func
    return decorator

def register_transition(key: str):
    """
    Decorator to register a transition with a given key.
    Version: 1.3.2
    """
    def decorator(func):
        transition_registry[key.lower()] = func
        return func
    return decorator

# New registry for play modes.
play_mode_registry = {}

def register_play_mode(key: str):
    """
    Decorator to register a play mode class with a given key.
    Version: 1.3.2
    """
    def decorator(cls):
        play_mode_registry[key.lower()] = cls
        return cls
    return decorator

all = [
    "scene_registry", "layer_registry", "effect_registry", "theme_registry", "transition_registry", "play_mode_registry",
    "register_scene", "register_layer", "register_effect", "register_theme", "register_transition", "register_play_mode"
]