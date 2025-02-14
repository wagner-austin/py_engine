"""
plugins.py - Central plugin registries for scenes, layers, effects, themes, transitions.
Version: 1.3.1 (Updated to use a unified layer registry)
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
    """
    def decorator(cls):
        scene_registry[key.lower()] = cls
        return cls
    return decorator

def register_layer(key: str, category: str = "foreground"):
    """
    Decorator to register a layer class with a given key and optional category.
    This replaces the old "register_universal_layer" and stores all layers in the same registry.
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

__all__ = [
    "scene_registry", "layer_registry", "effect_registry", "theme_registry", "transition_registry",
    "register_scene", "register_layer", "register_effect", "register_theme", "register_transition"
]