"""
bowling scoring logic engine
handles strikes, spares, and 10th frame bonuses
"""

from typing import List, Optional, Dict


class BowlingGame:
    """single player bowling game with scoring logic"""
    
    def __init__(self, player_id: int, player_name: str, game_id: Optional[int] = None):
        self.player_id = player_id
        self.player_name = player_name
        self.game_id = game_id
        
        # initialize 10 frames
        self.frames = [[] for _ in range(10)]
        self.current_frame = 0
        self.is_complete = False
    
    def add_roll(self, pins: int) -> Dict:
        """add roll to current frame"""
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
        
        # add roll to current frame
        self.frames[self.current_frame].append(pins)
        
        # check if frame complete
        if self.current_frame < 9:  # frames 1-9
            if pins == 10 and len(self.frames[self.current_frame]) == 1:  # strike only on first roll
                result['is_strike'] = True
                result['frame_complete'] = True
                self.current_frame += 1
            elif len(self.frames[self.current_frame]) == 2:  # second roll
                if sum(self.frames[self.current_frame]) == 10:
                    result['is_spare'] = True
                result['frame_complete'] = True
                self.current_frame += 1
        else:  # 10th frame
            frame_10 = self.frames[9]
            
            # check for strike or spare
            if len(frame_10) == 1 and pins == 10:
                result['is_strike'] = True
            elif len(frame_10) == 2:
                # check for spare
                if sum(frame_10) == 10:
                    result['is_spare'] = True
                elif pins == 10:
                    result['is_strike'] = True
                else:
                    result['frame_complete'] = True
                    self.is_complete = True
                    result['game_complete'] = True
                    result['should_end_after_animation'] = True
            elif len(frame_10) == 3:
                if pins == 10:
                    result['is_strike'] = True
                result['frame_complete'] = True
                self.is_complete = True
                result['game_complete'] = True
                result['should_end_after_animation'] = True
        
        return result
    
    def calculate_frame_score(self, frame_index: int) -> Optional[int]:
        """calculate score for specific frame"""
        frame = self.frames[frame_index]
        
        if not frame:
            return None
        
        # 10th frame special case
        if frame_index == 9:
            if not frame:
                return None
            return sum(frame)
        
        # strike
        if frame[0] == 10:
            next_rolls = self._get_next_n_rolls(frame_index, 2)
            if len(next_rolls) < 2:
                return None
            return 10 + sum(next_rolls)
        
        # spare
        if len(frame) == 2 and sum(frame) == 10:
            next_rolls = self._get_next_n_rolls(frame_index, 1)
            if len(next_rolls) < 1:
                return None
            return 10 + next_rolls[0]
        
        # regular frame
        if len(frame) == 2:
            return sum(frame)
        
        return None
    
    def _get_next_n_rolls(self, frame_index: int, n: int) -> List[int]:
        """get next n rolls after frame"""
        rolls = []
        current_idx = frame_index + 1
        
        while len(rolls) < n and current_idx < 10:
            for roll in self.frames[current_idx]:
                rolls.append(roll)
                if len(rolls) >= n:
                    break
            current_idx += 1
        
        return rolls
    
    def get_provisional_frame_score(self, frame_index: int) -> int:
        """calculate provisional score treating missing bonus as 0"""
        frame = self.frames[frame_index]
        
        if not frame:
            return 0
        
        # 10th frame
        if frame_index == 9:
            return sum(frame)
        
        # strike
        if frame[0] == 10:
            score = 10
            next_rolls = self._get_next_n_rolls(frame_index, 2)
            score += sum(next_rolls)
            return score
        
        # spare
        if len(frame) == 2 and sum(frame) == 10:
            score = 10
            next_rolls = self._get_next_n_rolls(frame_index, 1)
            score += sum(next_rolls)
            return score
        
        return sum(frame)
    
    def get_total_score(self) -> Optional[int]:
        """calculate total score for game"""
        total = 0
        any_scored = False
        
        for i in range(10):
            frame_score = self.calculate_frame_score(i)
            if frame_score is not None:
                total += frame_score
                any_scored = True
            else:
                break
        
        return total if any_scored else None
    
    def get_cumulative_scores(self) -> List[Optional[int]]:
        """get cumulative scores for each frame"""
        cumulative = []
        running_total = 0
        
        for i in range(10):
            frame_score = self.calculate_frame_score(i)
            if frame_score is None:
                cumulative.append(None)
                for j in range(i + 1, 10):
                    cumulative.append(None)
                break
            else:
                running_total += frame_score
                cumulative.append(running_total)
        
        return cumulative
    
    def get_current_frame_number(self) -> int:
        """get current frame number (1-based)"""
        return min(self.current_frame + 1, 10)
    
    def get_current_roll_in_frame(self) -> int:
        """get which roll in current frame"""
        if self.current_frame >= 10 or self.is_complete:
            if self.current_frame == 9:
                return min(len(self.frames[9]), 3)
            return 1
        return len(self.frames[self.current_frame]) + 1
    
    def is_frame_complete(self, frame_index: int) -> bool:
        """check if frame is complete"""
        frame = self.frames[frame_index]
        
        if frame_index < 9:
            return len(frame) > 0 and (frame[0] == 10 or len(frame) == 2)
        else:
            if len(frame) < 2:
                return False
            if frame[0] == 10 or (len(frame) >= 2 and sum(frame[:2]) == 10):
                return len(frame) == 3
            return len(frame) == 2
    
    def get_max_pins_for_current_roll(self) -> int:
        """get max pins for current roll"""
        current_rolls = self.frames[self.current_frame]
        
        if len(current_rolls) == 0:
            return 10
        
        # 10th frame rules
        if self.current_frame == 9:
            if len(current_rolls) == 1:
                if current_rolls[0] == 10:
                    return 10
                return 10 - current_rolls[0]
            elif len(current_rolls) == 2:
                if current_rolls[1] == 10:
                    return 10
                if current_rolls[0] + current_rolls[1] == 10:
                    return 10
                return 0
        
        return 10 - current_rolls[0]


class GameManager:
    """manages multiple players in bowling match"""
    
    def __init__(self):
        """initialize game manager"""
        self.players: List[BowlingGame] = []
        self.current_player_index = 0
    
    def add_player(self, player_id: int, player_name: str, game_id: Optional[int] = None):
        """add player to game"""
        game = BowlingGame(player_id, player_name, game_id)
        self.players.append(game)
    
    def get_current_player(self) -> Optional[BowlingGame]:
        """get currently active player"""
        if not self.players:
            return None
        return self.players[self.current_player_index]
    
    def record_roll(self, pins: int) -> Dict:
        """record roll and advance turn if needed"""
        current_player = self.get_current_player()
        if not current_player:
            raise ValueError("No players in game")
        
        result = current_player.add_roll(pins)
        result['player_name'] = current_player.player_name
        
        # check if advance to next player
        if result['frame_complete']:
            # special case: 10th frame with strike/spare
            if (current_player.current_frame == 9 and 
                len(current_player.frames[9]) >= 1 and 
                (current_player.frames[9][0] == 10 or 
                 (len(current_player.frames[9]) >= 2 and sum(current_player.frames[9][:2]) == 10))):
                pass
            else:
                self._advance_to_next_player()
        
        if current_player.is_complete:
            self._advance_to_next_player()
        
        all_complete = all(player.is_complete for player in self.players)
        result['all_games_complete'] = all_complete
        
        return result
    
    def _advance_to_next_player(self):
        """advance to next player turn"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        attempts = 0
        while attempts < len(self.players):
            current = self.players[self.current_player_index]
            if not current.is_complete:
                break
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            attempts += 1
    
    def get_winner(self) -> Optional[BowlingGame]:
        """get winner (highest score)"""
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
        """check if all players complete"""
        return all(player.is_complete for player in self.players)


