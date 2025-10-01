"""
Bowling scoring logic engine.
Handles complex scoring rules including strikes, spares, and 10th frame bonuses.
"""

from typing import List, Optional, Dict


class BowlingGame:
    """Represents a single player's bowling game with full scoring logic."""
    
    def __init__(self, player_id: int, player_name: str, game_id: Optional[int] = None):
        """
        Initialize a new bowling game for a player.
        
        Args:
            player_id: Database ID of the player
            player_name: Name of the player
            game_id: Database game ID (if already created)
        """
        self.player_id = player_id
        self.player_name = player_name
        self.game_id = game_id
        
        # Initialize 10 frames, each can hold up to 3 rolls (10th frame)
        self.frames = [[] for _ in range(10)]
        self.current_frame = 0
        self.is_complete = False
    
    def add_roll(self, pins: int) -> Dict:
        """
        Add a roll to the current frame.
        
        Args:
            pins: Number of pins knocked down (0-10)
            
        Returns:
            Dictionary with roll result info (is_strike, is_spare, frame_complete)
            
        Raises:
            ValueError: If invalid number of pins or game is complete
        """
        if self.is_complete:
            raise ValueError("Game is already complete")
        
        if pins < 0 or pins > 10:
            raise ValueError("Pins must be between 0 and 10")
        
        result = {
            'is_strike': False,
            'is_spare': False,
            'frame_complete': False,
            'game_complete': False
        }
        
        # Add the roll to current frame
        self.frames[self.current_frame].append(pins)
        
        # Check if frame is complete
        if self.current_frame < 9:  # Frames 1-9
            if pins == 10:  # Strike
                result['is_strike'] = True
                result['frame_complete'] = True
                self.current_frame += 1
            elif len(self.frames[self.current_frame]) == 2:  # Second roll
                if sum(self.frames[self.current_frame]) == 10:
                    result['is_spare'] = True
                result['frame_complete'] = True
                self.current_frame += 1
        else:  # 10th frame (index 9)
            frame_10 = self.frames[9]
            
            # Check for strike or spare to determine if we get a 3rd roll
            if len(frame_10) == 1 and pins == 10:
                result['is_strike'] = True
            elif len(frame_10) == 2:
                # Check for spare
                if sum(frame_10) == 10:
                    result['is_spare'] = True
                # Check if frame is complete (only if no strike on first roll AND no spare)
                if frame_10[0] < 10 and sum(frame_10) < 10:
                    result['frame_complete'] = True
                    self.is_complete = True
                    result['game_complete'] = True
            elif len(frame_10) == 3:
                result['frame_complete'] = True
                self.is_complete = True
                result['game_complete'] = True
        
        # Check if we're at the end of the game
        if self.current_frame >= 10:
            self.is_complete = True
            result['game_complete'] = True
        
        return result
    
    def calculate_frame_score(self, frame_index: int) -> Optional[int]:
        """
        Calculate the score for a specific frame.
        May return None if the score cannot be calculated yet (waiting for bonus rolls).
        
        Args:
            frame_index: Frame number (0-9)
            
        Returns:
            Score for the frame or None if not yet calculable
        """
        frame = self.frames[frame_index]
        
        if not frame:
            return None
        
        # 10th frame (special case - no look-ahead needed)
        if frame_index == 9:
            return sum(frame) if frame else None
        
        # Strike
        if frame[0] == 10:
            # Need next 2 rolls
            next_rolls = self._get_next_n_rolls(frame_index, 2)
            if len(next_rolls) < 2:
                return None  # Can't calculate yet
            return 10 + sum(next_rolls)
        
        # Spare
        if len(frame) == 2 and sum(frame) == 10:
            # Need next 1 roll
            next_rolls = self._get_next_n_rolls(frame_index, 1)
            if len(next_rolls) < 1:
                return None  # Can't calculate yet
            return 10 + next_rolls[0]
        
        # Regular frame
        if len(frame) == 2:
            return sum(frame)
        
        return None  # Frame not complete yet
    
    def _get_next_n_rolls(self, frame_index: int, n: int) -> List[int]:
        """
        Get the next N rolls after a given frame.
        
        Args:
            frame_index: Starting frame index
            n: Number of rolls to retrieve
            
        Returns:
            List of roll values
        """
        rolls = []
        current_idx = frame_index + 1
        
        while len(rolls) < n and current_idx < 10:
            for roll in self.frames[current_idx]:
                rolls.append(roll)
                if len(rolls) >= n:
                    break
            current_idx += 1
        
        return rolls
    
    def get_total_score(self) -> Optional[int]:
        """
        Calculate the total score for the game so far.
        
        Returns:
            Total score (sum of calculable frames), or None if no frames can be scored
        """
        total = 0
        any_scored = False
        
        for i in range(10):
            frame_score = self.calculate_frame_score(i)
            if frame_score is not None:
                total += frame_score
                any_scored = True
            else:
                # Can't calculate this frame yet, stop here
                break
        
        return total if any_scored else None
    
    def get_cumulative_scores(self) -> List[Optional[int]]:
        """
        Get cumulative scores for each frame.
        
        Returns:
            List of cumulative scores (None for frames that can't be scored yet)
        """
        cumulative = []
        running_total = 0
        
        for i in range(10):
            frame_score = self.calculate_frame_score(i)
            if frame_score is None:
                cumulative.append(None)
                # Once we hit a None, all subsequent frames will also be None
                for j in range(i + 1, 10):
                    cumulative.append(None)
                break
            else:
                running_total += frame_score
                cumulative.append(running_total)
        
        return cumulative
    
    def get_current_frame_number(self) -> int:
        """
        Get the current frame number (1-based).
        
        Returns:
            Current frame number (1-10)
        """
        return min(self.current_frame + 1, 10)
    
    def get_current_roll_in_frame(self) -> int:
        """
        Get which roll we're on in the current frame.
        
        Returns:
            Roll number (1, 2, or 3)
        """
        return len(self.frames[self.current_frame]) + 1
    
    def is_frame_complete(self, frame_index: int) -> bool:
        """
        Check if a specific frame is complete.
        
        Args:
            frame_index: Frame number (0-9)
            
        Returns:
            True if frame is complete
        """
        frame = self.frames[frame_index]
        
        if frame_index < 9:
            # Strike or 2 rolls
            return len(frame) > 0 and (frame[0] == 10 or len(frame) == 2)
        else:
            # 10th frame
            if len(frame) < 2:
                return False
            # If strike or spare in 10th, need 3 rolls
            if frame[0] == 10 or (len(frame) >= 2 and sum(frame[:2]) == 10):
                return len(frame) == 3
            # Otherwise need 2 rolls
            return len(frame) == 2
    
    def get_max_pins_for_current_roll(self) -> int:
        """
        Get the maximum number of pins that can be knocked down on the current roll.
        
        Returns:
            Maximum pins (0-10)
        """
        if self.is_complete:
            return 0
        
        current_rolls = self.frames[self.current_frame]
        
        # First roll is always 10
        if len(current_rolls) == 0:
            return 10
        
        # 10th frame has special rules
        if self.current_frame == 9:
            if len(current_rolls) == 1:
                # If first roll was a strike, second roll can be 10
                if current_rolls[0] == 10:
                    return 10
                # Otherwise, max is 10 minus first roll
                return 10 - current_rolls[0]
            elif len(current_rolls) == 2:
                # Third roll: if second was a strike, can knock down 10
                if current_rolls[1] == 10:
                    return 10
                # If spare on first two rolls, can knock down 10
                if current_rolls[0] + current_rolls[1] == 10:
                    return 10
                # Otherwise, shouldn't get here
                return 0
        
        # Regular frames: second roll is 10 minus first roll
        return 10 - current_rolls[0]


class GameManager:
    """Manages multiple players in a single bowling match."""
    
    def __init__(self):
        """Initialize the game manager."""
        self.players: List[BowlingGame] = []
        self.current_player_index = 0
    
    def add_player(self, player_id: int, player_name: str, game_id: Optional[int] = None):
        """
        Add a player to the game.
        
        Args:
            player_id: Database ID of the player
            player_name: Name of the player
            game_id: Database game ID (if already created)
        """
        game = BowlingGame(player_id, player_name, game_id)
        self.players.append(game)
    
    def get_current_player(self) -> Optional[BowlingGame]:
        """
        Get the currently active player.
        
        Returns:
            BowlingGame object for current player or None
        """
        if not self.players:
            return None
        return self.players[self.current_player_index]
    
    def record_roll(self, pins: int) -> Dict:
        """
        Record a roll for the current player and advance turn if needed.
        
        Args:
            pins: Number of pins knocked down
            
        Returns:
            Dictionary with roll result information
        """
        current_player = self.get_current_player()
        if not current_player:
            raise ValueError("No players in game")
        
        result = current_player.add_roll(pins)
        result['player_name'] = current_player.player_name
        
        # Check if we should advance to next player
        # Advance whenever a frame is complete (even if that player is now done)
        if result['frame_complete']:
            self._advance_to_next_player()
        
        # Check if all players are done
        if all(player.is_complete for player in self.players):
            result['all_games_complete'] = True
        else:
            result['all_games_complete'] = False
        
        return result
    
    def _advance_to_next_player(self):
        """Advance to the next player's turn."""
        # Move to next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Skip players who have finished, but only if there are unfinished players
        attempts = 0
        while attempts < len(self.players):
            current = self.players[self.current_player_index]
            if not current.is_complete:
                # Found an active player
                break
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            attempts += 1
    
    def get_winner(self) -> Optional[BowlingGame]:
        """
        Get the winner of the game (player with highest score).
        
        Returns:
            BowlingGame object of winner or None if game not complete
        """
        if not all(player.is_complete for player in self.players):
            return None
        
        winner = None
        highest_score = -1
        
        for player in self.players:
            score = player.get_total_score()
            if score is not None and score > highest_score:
                highest_score = score
                winner = player
        
        return winner
    
    def is_game_complete(self) -> bool:
        """
        Check if all players have completed their games.
        
        Returns:
            True if all games are complete
        """
        return all(player.is_complete for player in self.players)

