"""
Sound manager for playing strike and spare sound effects.
"""

import os
import pygame
import random


class SoundManager:
    """Handles playing sound effects for bowling events."""
    
    def __init__(self):
        """Initialize pygame mixer for sound playback."""
        try:
            pygame.mixer.init()
            self.enabled = True
            self.strike_sounds = []
            self.spare_sounds = []
            self.pin_sound = None
            self.leaderboard_music = None
            self._load_sounds()
        except:
            self.enabled = False
            print("Sound system not available")
    
    def _load_sounds(self):
        """Load sound files if they exist."""
        assets_path = os.path.join("assets", "animations")
        
        # Load multiple strike sounds (strike.wav, strike1.wav, strike2.wav, etc.)
        for ext in ['.wav', '.mp3', '.ogg']:
            # Try base file first
            strike_path = os.path.join(assets_path, f"strike{ext}")
            if os.path.exists(strike_path):
                try:
                    self.strike_sounds.append(pygame.mixer.Sound(strike_path))
                except:
                    pass
            
            # Try numbered files (strike1, strike2, etc.)
            for i in range(1, 10):  # Support up to 9 variations
                strike_path = os.path.join(assets_path, f"strike{i}{ext}")
                if os.path.exists(strike_path):
                    try:
                        self.strike_sounds.append(pygame.mixer.Sound(strike_path))
                    except:
                        pass
        
        # Load multiple spare sounds
        for ext in ['.wav', '.mp3', '.ogg']:
            # Try base file first
            spare_path = os.path.join(assets_path, f"spare{ext}")
            if os.path.exists(spare_path):
                try:
                    self.spare_sounds.append(pygame.mixer.Sound(spare_path))
                except:
                    pass
            
            # Try numbered files
            for i in range(1, 10):
                spare_path = os.path.join(assets_path, f"spare{i}{ext}")
                if os.path.exists(spare_path):
                    try:
                        self.spare_sounds.append(pygame.mixer.Sound(spare_path))
                    except:
                        pass
        
        # Load pin knock sound
        for ext in ['.wav', '.mp3', '.ogg']:
            pin_path = os.path.join(assets_path, f"pin{ext}")
            if os.path.exists(pin_path):
                try:
                    self.pin_sound = pygame.mixer.Sound(pin_path)
                    break
                except:
                    pass
        
        # Load leaderboard music (longer, can loop)
        for ext in ['.wav', '.mp3', '.ogg']:
            music_path = os.path.join(assets_path, f"leaderboard{ext}")
            if os.path.exists(music_path):
                try:
                    self.leaderboard_music = music_path
                    break
                except:
                    pass
    
    def play_strike(self):
        """Play random strike sound effect."""
        if self.enabled and self.strike_sounds:
            random.choice(self.strike_sounds).play()
    
    def play_spare(self):
        """Play random spare sound effect."""
        if self.enabled and self.spare_sounds:
            random.choice(self.spare_sounds).play()
    
    def play_pin_knock(self):
        """Play pin knock sound effect."""
        if self.enabled and self.pin_sound:
            self.pin_sound.play()
    
    def play_leaderboard_music(self, loops=-1):
        """
        Play leaderboard background music.
        
        Args:
            loops: Number of times to loop (-1 for infinite)
        """
        if self.enabled and self.leaderboard_music:
            try:
                pygame.mixer.music.load(self.leaderboard_music)
                pygame.mixer.music.play(loops)
            except:
                pass
    
    def stop_music(self):
        """Stop background music."""
        if self.enabled:
            try:
                pygame.mixer.music.stop()
            except:
                pass
    
    def set_volume(self, volume: float):
        """
        Set volume for all sounds.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if self.enabled:
            for sound in self.strike_sounds:
                sound.set_volume(volume)
            for sound in self.spare_sounds:
                sound.set_volume(volume)
            if self.pin_sound:
                self.pin_sound.set_volume(volume)
            try:
                pygame.mixer.music.set_volume(volume)
            except:
                pass

