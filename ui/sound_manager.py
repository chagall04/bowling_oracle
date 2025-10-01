"""
Sound manager for playing strike and spare sound effects.
"""

import os
import pygame


class SoundManager:
    """Handles playing sound effects for bowling events."""
    
    def __init__(self):
        """Initialize pygame mixer for sound playback."""
        try:
            pygame.mixer.init()
            self.enabled = True
            self.strike_sound = None
            self.spare_sound = None
            self._load_sounds()
        except:
            self.enabled = False
            print("Sound system not available")
    
    def _load_sounds(self):
        """Load sound files if they exist."""
        assets_path = os.path.join("assets", "animations")
        
        # Try to load strike sound (try both .wav and .mp3)
        for ext in ['.wav', '.mp3', '.ogg']:
            strike_path = os.path.join(assets_path, f"strike{ext}")
            if os.path.exists(strike_path):
                try:
                    self.strike_sound = pygame.mixer.Sound(strike_path)
                    break
                except:
                    pass
        
        # Try to load spare sound
        for ext in ['.wav', '.mp3', '.ogg']:
            spare_path = os.path.join(assets_path, f"spare{ext}")
            if os.path.exists(spare_path):
                try:
                    self.spare_sound = pygame.mixer.Sound(spare_path)
                    break
                except:
                    pass
    
    def play_strike(self):
        """Play strike sound effect."""
        if self.enabled and self.strike_sound:
            self.strike_sound.play()
    
    def play_spare(self):
        """Play spare sound effect."""
        if self.enabled and self.spare_sound:
            self.spare_sound.play()
    
    def set_volume(self, volume: float):
        """
        Set volume for all sounds.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if self.enabled:
            if self.strike_sound:
                self.strike_sound.set_volume(volume)
            if self.spare_sound:
                self.spare_sound.set_volume(volume)

