"""
plugins.py - Central plugin registries for scenes, layers, effects, themes, transitions, and play modes.
Version: 1.3.3
Summary: Added duplicate key checks in registration decorators to warn when duplicate registration is attempted.
"""

import logging

# Set up logging configuration if not already configured.
logging.basicConfig(level=logging.INFO)

# Plugin registries
scene_registry = {}
layer_registry = {}   # Unified registry for all layers
effect_registry = {}
theme_registry = {}
transition_registry = {}
play_mode_registry = {}

def register_scene(key: str):
    """
    Decorator to register a scene class with a given key.
    Version: 1.3.3
    """
    def decorator(cls):
        lower_key = key.lower()
        if lower_key in scene_registry:
            logging.warning("Duplicate scene registration for key '%s'. Overwriting previous registration.", key)
        scene_registry[lower_key] = cls
        return cls
    return decorator

def register_layer(key: str, category: str = "foreground"):
    """
    Decorator to register a layer class with a given key and optional category.
    Version: 1.3.3
    """
    def decorator(cls):
        lower_key = key.lower()
        if lower_key in layer_registry:
            logging.warning("Duplicate layer registration for key '%s'. Overwriting previous registration.", key)
        layer_registry[lower_key] = {
            "class": cls,
            "category": category.lower()
        }
        return cls
    return decorator

def register_effect(key: str):
    """
    Decorator to register an effect layer class with a given key.
    Version: 1.3.3
    """
    def decorator(cls):
        lower_key = key.lower()
        if lower_key in effect_registry:
            logging.warning("Duplicate effect registration for key '%s'. Overwriting previous registration.", key)
        effect_registry[lower_key] = cls
        return cls
    return decorator

def register_theme(key: str):
    """
    Decorator to register a theme with a given key.
    Version: 1.3.3
    """
    def decorator(func):
        lower_key = key.lower()
        if lower_key in theme_registry:
            logging.warning("Duplicate theme registration for key '%s'. Overwriting previous registration.", key)
        theme_registry[lower_key] = func()
        return func
    return decorator

def register_transition(key: str):
    """
    Decorator to register a transition with a given key.
    Version: 1.3.3
    """
    def decorator(func):
        lower_key = key.lower()
        if lower_key in transition_registry:
            logging.warning("Duplicate transition registration for key '%s'. Overwriting previous registration.", key)
        transition_registry[lower_key] = func
        return func
    return decorator

def register_play_mode(key: str):
    """
    Decorator to register a play mode class with a given key.
    Version: 1.3.3
    """
    def decorator(cls):
        lower_key = key.lower()
        if lower_key in play_mode_registry:
            logging.warning("Duplicate play mode registration for key '%s'. Overwriting previous registration.", key)
        play_mode_registry[lower_key] = cls
        return cls
    return decorator

all = [
    "scene_registry", "layer_registry", "effect_registry", "theme_registry", "transition_registry", "play_mode_registry",
    "register_scene", "register_layer", "register_effect", "register_theme", "register_transition", "register_play_mode"
]