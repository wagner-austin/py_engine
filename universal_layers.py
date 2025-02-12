# File: universal_layers.py
# Version: 1.3 (modified)
# Summary: Aggregates universal layers for scenes by importing individual layer modules.
#          Now returns new instances of layers based on the current font and configuration.
#          The RainEffectLayer is persistent across scenes to ensure smooth animation.
# Tags: layers, universal, modular, persistent

from art_layers import StarArtLayer, BackGroundArtLayer
from effect_layers import RainEffectLayer
from instruction_layer import InstructionLayer
from border_layer import BorderLayer

# Persistent instance for the rain effect layer. This instance will be reused across scene changes.
_persistent_rain_layer = None

def get_universal_layers(font, config):
    """
    Returns a list of universal layer instances based on the current font and configuration.
    Note: The RainEffectLayer is persistent between scenes.
    """
    global _persistent_rain_layer
    if _persistent_rain_layer is None:
        _persistent_rain_layer = RainEffectLayer(config)
    return [
        StarArtLayer(font, config),         # z=0: Star art background
        _persistent_rain_layer,             # z=1: Rain effect (persistent)
        BackGroundArtLayer(font, config),     # z=2: Background art foreground
        InstructionLayer(font, config),       # z=3: On-screen instructions
        BorderLayer(config),                  # z=5: Border drawn on top
    ]