"""
plugins.py - Plugin registry for layers, scenes, and effects.

Version: 1.0
"""

# Global registries
scene_registry = {}
layer_registry = {}
effect_registry = {}

def register_scene(key: str):
    """
    Decorator to register a scene class with a given key.
    """
    def decorator(cls):
        scene_registry[key] = cls
        return cls
    return decorator

def register_layer(key: str):
    """
    Decorator to register a layer class with a given key.
    """
    def decorator(cls):
        layer_registry[key] = cls
        return cls
    return decorator

def register_effect(key: str):
    """
    Decorator to register an effect layer class with a given key.
    """
    def decorator(cls):
        effect_registry[key] = cls
        return cls
    return decorator