"""
sound manager for playing strike and spare sound effects
"""

import os
import pygame
import random


class SoundManager:
    """handles playing sound effects for bowling events"""
    
    def __init__(self):
        """initialize pygame mixer for sound playback"""
        try:
            pygame.mixer.init()
            self.enabled = True
            self.strike_sounds = []
            self.spare_sounds = []
            self.pin_sound = None
            self.gutter_sound = None
            self.perfect_sound = None
            self.menu_music = None
            self.game_music = None
            self.game_over_music = None
            self._load_sounds()
        except:
            self.enabled = False
    
    def _load_sounds(self):
        """load sound files if they exist"""
        assets_path = os.path.join("assets", "audio")
        
        # load multiple strike sounds (strike.wav, strike1.wav, strike2.wav, etc.)
        for ext in ['.wav', '.mp3', '.ogg']:
            # try base file first
            strike_path = os.path.join(assets_path, f"strike{ext}")
            if os.path.exists(strike_path):
                try:
                    self.strike_sounds.append(pygame.mixer.Sound(strike_path))
                except:
                    pass
            
            # try numbered files (strike1, strike2, etc.)
            for i in range(1, 10):  # support up to 9 variations
                strike_path = os.path.join(assets_path, f"strike{i}{ext}")
                if os.path.exists(strike_path):
                    try:
                        self.strike_sounds.append(pygame.mixer.Sound(strike_path))
                    except:
                        pass
        
        # load multiple spare sounds
        for ext in ['.wav', '.mp3', '.ogg']:
            # try base file first
            spare_path = os.path.join(assets_path, f"spare{ext}")
            if os.path.exists(spare_path):
                try:
                    self.spare_sounds.append(pygame.mixer.Sound(spare_path))
                except:
                    pass
            
            # try numbered files
            for i in range(1, 10):
                spare_path = os.path.join(assets_path, f"spare{i}{ext}")
                if os.path.exists(spare_path):
                    try:
                        self.spare_sounds.append(pygame.mixer.Sound(spare_path))
                    except:
                        pass
        
        # load pin knock sound
        for ext in ['.wav', '.mp3', '.ogg']:
            pin_path = os.path.join(assets_path, f"pin{ext}")
            if os.path.exists(pin_path):
                try:
                    self.pin_sound = pygame.mixer.Sound(pin_path)
                    break
                except:
                    pass
        
        # load gutter ball sound
        for ext in ['.wav', '.mp3', '.ogg']:
            gutter_path = os.path.join(assets_path, f"gutterball{ext}")
            if os.path.exists(gutter_path):
                try:
                    self.gutter_sound = pygame.mixer.Sound(gutter_path)
                    break
                except:
                    pass
        
        # load perfect game sound
        for ext in ['.wav', '.mp3', '.ogg']:
            perfect_path = os.path.join(assets_path, f"perfect{ext}")
            if os.path.exists(perfect_path):
                try:
                    self.perfect_sound = pygame.mixer.Sound(perfect_path)
                    break
                except:
                    pass
        
        # load different types of music
        music_types = [
            ("menu_music", "menu"),
            ("game_music", "game"), 
            ("game_over_music", "gameover")
        ]
        
        for music_attr, filename in music_types:
            for ext in ['.wav', '.mp3', '.ogg']:
                music_path = os.path.join(assets_path, f"{filename}{ext}")
                if os.path.exists(music_path):
                    try:
                        setattr(self, music_attr, music_path)
                        break
                    except Exception as e:
                        pass
    
    def play_strike(self):
        """play random strike sound effect"""
        if self.enabled and self.strike_sounds:
            random.choice(self.strike_sounds).play()
    
    def play_spare(self):
        """play random spare sound effect"""
        if self.enabled and self.spare_sounds:
            random.choice(self.spare_sounds).play()
    
    def play_pin_knock(self):
        """play pin knock sound effect"""
        if self.enabled and self.pin_sound:
            self.pin_sound.play()
    
    def play_gutter_ball(self):
        """play gutter ball sound effect"""
        if self.enabled and self.gutter_sound:
            self.gutter_sound.play()
    
    def play_perfect_game(self):
        """play perfect game sound effect"""
        if self.enabled and self.perfect_sound:
            self.perfect_sound.play()
    
    def play_menu_music(self, loops=-1):
        """play menu background music"""
        if self.enabled and self.menu_music:
            try:
                pygame.mixer.music.load(self.menu_music)
                pygame.mixer.music.play(loops)
            except Exception as e:
                pass
        else:
            pass
    
    def play_game_music(self, loops=-1):
        """play in-game background music"""
        if self.enabled and self.game_music:
            try:
                pygame.mixer.music.load(self.game_music)
                pygame.mixer.music.play(loops)
            except Exception as e:
                pass
        else:
            pass
    
    def play_game_over_music(self, loops=-1):
        """play game over screen music"""
        if self.enabled and self.game_over_music:
            try:
                pygame.mixer.music.load(self.game_over_music)
                pygame.mixer.music.play(loops)
            except:
                pass
    
    def play_leaderboard_music(self, loops=-1):
        """play leaderboard background music (legacy method for compatibility)"""
        # use game music as fallback for leaderboard
        self.play_game_music(loops)
    
    def stop_music(self):
        """stop background music"""
        if self.enabled:
            try:
                pygame.mixer.music.stop()
            except Exception as e:
                pass
    
    def set_volume(self, volume: float):
        """set volume for all sounds"""
        if self.enabled:
            for sound in self.strike_sounds:
                sound.set_volume(volume)
            for sound in self.spare_sounds:
                sound.set_volume(volume)
            if self.pin_sound:
                self.pin_sound.set_volume(volume)
            if self.gutter_sound:
                self.gutter_sound.set_volume(volume)
            if self.perfect_sound:
                self.perfect_sound.set_volume(volume)
            try:
                pygame.mixer.music.set_volume(volume)
            except:
                pass

