"""
plugins.py - Central plugin registries for scenes, layers, effects, themes, transitions, and universal layers.

Version: 1.3 (updated)

This module centralizes all plugin registrations. All plugins (scenes, layers, effects, themes, transitions, etc.)
are registered here and can be easily imported elsewhere. The transition_registry is dedicated solely for transitions.
A new universal_layer_registry has been added along with the corresponding decorator for registering universal layers by category.
"""

# Plugin registries
scene_registry = {}
layer_registry = {}
effect_registry = {}
theme_registry = {}
transition_registry = {}

# New universal layer registry.
# This registry stores universal layer classes along with a category (e.g., "background", "effect", or "foreground").
universal_layer_registry = {}

def register_scene(key: str):
    """
    Decorator to register a scene class with a given key.
    """
    def decorator(cls):
        scene_registry[key.lower()] = cls
        return cls
    return decorator

def register_layer(key: str):
    """
    Decorator to register a layer class with a given key.
    """
    def decorator(cls):
        layer_registry[key.lower()] = cls
        return cls
    return decorator

def register_effect(key: str):
    """
    Decorator to register an effect layer class with a given key.
    """
    def decorator(cls):
        effect_registry[key.lower()] = cls
        return cls
    return decorator

def register_theme(key: str):
    """
    Decorator to register a theme with a given key.
    The decorated function should return a Theme instance.
    """
    def decorator(func):
        theme_registry[key.lower()] = func()
        return func
    return decorator

def register_transition(key: str):
    """
    Decorator to register a transition with a given key.
    The decorated function should be a factory that returns a Transition instance.
    """
    def decorator(func):
        transition_registry[key.lower()] = func
        return func
    return decorator

def register_universal_layer(key: str, category: str):
    """
    Decorator to register a universal layer with a given key and category.
    
    Parameters:
      key (str): The unique identifier for the layer.
      category (str): The category of the universal layer (e.g., "background", "effect", or "foreground").
    
    The layer's class is stored along with its category in the universal_layer_registry.
    """
    def decorator(cls):
        universal_layer_registry[key.lower()] = {"class": cls, "category": category.lower()}
        return cls
    return decorator

__all__ = [
    "scene_registry", "layer_registry", "effect_registry", "theme_registry", "transition_registry",
    "universal_layer_registry",
    "register_scene", "register_layer", "register_effect", "register_theme", "register_transition", "register_universal_layer"
]