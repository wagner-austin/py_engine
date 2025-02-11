# FileName: universal_layers.py
# version: 1.1 (modified)
# Summary: Aggregates universal layers for scenes by importing individual layer modules.
#          Now returns new instances of layers based on the current font/scaling.
# Tags: layers, universal, modular, persistent

from art_layers import StarArtLayer, BackGroundArtLayer
from effect_layers import RainEffectLayer
from instruction_layer import InstructionLayer
from border_layer import BorderLayer

def get_universal_layers(font):
    """
    Returns a list of universal layer instances based on the current font.
    Note: Previously cached as a singleton; now returning new instances to reflect updated settings.
    """
    return [
        StarArtLayer(font),         # z=0: Star art background
        RainEffectLayer(),          # z=1: Rain effect
        BackGroundArtLayer(font),   # z=2: Background art foreground
        InstructionLayer(font),     # z=3: On-screen instructions
        BorderLayer()               # z=5: Border drawn on top
    ]