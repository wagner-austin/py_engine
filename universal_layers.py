"""
universal_layers.py - Aggregates universal layers for scenes by instantiating new layer objects based on
the current font and configuration. Caches static layers to avoid unnecessary reinitialization.

Version: 1.1
"""

from art_layers import StarArtLayer, BackGroundArtLayer
from instruction_layer import InstructionLayer
from border_layer import BorderLayer
from effect_layers import RainEffectLayer

class UniversalLayerFactory:
    """
    Factory for universal layers.
    
    Caches static layers so that they are reinitialized only when configuration or font changes.
    The persistent rain effect is reinitialized if the configuration changes.
    """

    def __init__(self):
        """
        Initializes the UniversalLayerFactory with no cached layers.
        """
        self._persistent_rain_layer = None
        self._static_star_art = None
        self._static_background_art = None
        self._static_instruction = None
        self._static_border = None
        self._last_snapshot = None  # Snapshot for static layers: (config.scale, config.screen_width, config.screen_height, id(font))
        self._rain_snapshot = None  # Snapshot for the rain effect: (config.scale, config.screen_width, config.screen_height)

    def refresh_universal_layers(self, font, config):
        """
        Reinitializes cached static layers if the configuration or font has changed.
        
        Parameters:
            font: The pygame font to be used for rendering text.
            config: The configuration object containing theme and scaling information.
        """
        new_snapshot = (config.scale, config.screen_width, config.screen_height, id(font))
        if self._last_snapshot != new_snapshot:
            self._static_star_art = StarArtLayer(font, config)
            self._static_background_art = BackGroundArtLayer(font, config)
            self._static_instruction = InstructionLayer(font, config)
            self._static_border = BorderLayer(config)
            self._last_snapshot = new_snapshot

        # Check and refresh persistent rain layer separately.
        rain_snapshot = (config.scale, config.screen_width, config.screen_height)
        if self._persistent_rain_layer is None or self._rain_snapshot != rain_snapshot:
            self._persistent_rain_layer = RainEffectLayer(config)
            self._rain_snapshot = rain_snapshot

    def get_universal_layers(self, font, config):
        """
        Returns a list of universal layer instances based on the current font and configuration.
        Cached static layers are returned if available.
        
        Parameters:
            font: The pygame font to be used for rendering text.
            config: The configuration object containing theme and scaling information.
        
        Returns:
            A list of universal layer instances.
        """
        self.refresh_universal_layers(font, config)
        return [
            self._static_star_art,         # z=0: Star art background
            self._persistent_rain_layer,   # z=1: Rain effect (persistent)
            self._static_background_art,   # z=2: Background art foreground
            self._static_instruction,      # z=3: On-screen instructions
            self._static_border,           # z=5: Border drawn on top
        ]