# FileName: universal_layers.py
# version: 1.1
# Summary: Aggregates universal layers for scenes by importing individual layer modules.
#          Now returns persistent (singleton) layer instances so that effects like the rain do not reset on scene changes.
# Tags: layers, universal, modular, persistent
from art_layers import StarArtLayer, BackGroundArtLayer
from effect_layers import RainEffectLayer
from instruction_layer import InstructionLayer
from border_layer import BorderLayer

_universal_layers = None

def get_universal_layers(font):
    """
    Returns a persistent list of universal layer instances.
    This ensures that effects such as the rain (in RainEffectLayer) maintain their state
    across scene transitions.
    """
    global _universal_layers
    if _universal_layers is None:
        _universal_layers = [
            StarArtLayer(font),       # z=0: Star art background
            RainEffectLayer(),        # z=1: Rain effect
           BackGroundArtLayer(font),     # z=2: Background art foreground
            InstructionLayer(font),   # z=3: On-screen instructions
            BorderLayer()             # z=5: Border drawn on top
        ]
    return _universal_layers