"""
Database handler for bowling score tracker.
Manages SQLite database operations for players, games, and frames.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class DatabaseHandler:
    """Handles all database operations for the bowling tracker application."""
    
    def __init__(self, db_name: str = "bowling_tracker.db"):
        """
        Initialize database connection and create tables if they don't exist.
        
        Args:
            db_name: Name of the SQLite database file
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establish connection to the SQLite database."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
    
    def _create_tables(self):
        """Create the database schema if tables don't exist."""
        # Player table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Player (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL UNIQUE,
                date_joined TEXT NOT NULL
            )
        """)
        
        # Game table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Game (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                final_score INTEGER NOT NULL,
                game_date TEXT NOT NULL,
                FOREIGN KEY (player_id) REFERENCES Player(player_id)
            )
        """)
        
        # Frame table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Frame (
                frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER NOT NULL,
                frame_number INTEGER NOT NULL,
                roll1_pins INTEGER,
                roll2_pins INTEGER,
                roll3_pins INTEGER,
                FOREIGN KEY (game_id) REFERENCES Game(game_id),
                CHECK (frame_number >= 1 AND frame_number <= 10)
            )
        """)
        
        self.connection.commit()
    
    # ==================== Player Operations ====================
    
    def add_player(self, player_name: str) -> int:
        """
        Add a new player to the database.
        
        Args:
            player_name: Name of the player
            
        Returns:
            player_id of the newly added player
            
        Raises:
            sqlite3.IntegrityError: If player name already exists
        """
        date_joined = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO Player (player_name, date_joined) VALUES (?, ?)",
            (player_name, date_joined)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_player(self, player_id: int) -> Optional[Dict]:
        """
        Retrieve player information by ID.
        
        Args:
            player_id: ID of the player
            
        Returns:
            Dictionary with player data or None if not found
        """
        self.cursor.execute(
            "SELECT player_id, player_name, date_joined FROM Player WHERE player_id = ?",
            (player_id,)
        )
        result = self.cursor.fetchone()
        if result:
            return {
                'player_id': result[0],
                'player_name': result[1],
                'date_joined': result[2]
            }
        return None
    
    def get_all_players(self) -> List[Dict]:
        """
        Retrieve all players from the database.
        
        Returns:
            List of dictionaries containing player data
        """
        self.cursor.execute(
            "SELECT player_id, player_name, date_joined FROM Player ORDER BY player_name"
        )
        results = self.cursor.fetchall()
        return [
            {
                'player_id': row[0],
                'player_name': row[1],
                'date_joined': row[2]
            }
            for row in results
        ]
    
    def delete_player(self, player_id: int):
        """
        Delete a player and all associated games and frames.
        
        Args:
            player_id: ID of the player to delete
        """
        # Get all game IDs for this player
        self.cursor.execute("SELECT game_id FROM Game WHERE player_id = ?", (player_id,))
        game_ids = [row[0] for row in self.cursor.fetchall()]
        
        # Delete all frames for these games
        for game_id in game_ids:
            self.cursor.execute("DELETE FROM Frame WHERE game_id = ?", (game_id,))
        
        # Delete all games for this player
        self.cursor.execute("DELETE FROM Game WHERE player_id = ?", (player_id,))
        
        # Delete the player
        self.cursor.execute("DELETE FROM Player WHERE player_id = ?", (player_id,))
        
        self.connection.commit()
    
    def search_players(self, search_term: str) -> List[Dict]:
        """
        Search for players by name (case-insensitive partial match).
        
        Args:
            search_term: Search string
            
        Returns:
            List of matching player dictionaries
        """
        self.cursor.execute(
            "SELECT player_id, player_name, date_joined FROM Player WHERE player_name LIKE ? ORDER BY player_name",
            (f"%{search_term}%",)
        )
        results = self.cursor.fetchall()
        return [
            {
                'player_id': row[0],
                'player_name': row[1],
                'date_joined': row[2]
            }
            for row in results
        ]
    
    # ==================== Game Operations ====================
    
    def create_game(self, player_id: int) -> int:
        """
        Create a new game for a player.
        
        Args:
            player_id: ID of the player
            
        Returns:
            game_id of the newly created game
        """
        game_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO Game (player_id, final_score, game_date) VALUES (?, ?, ?)",
            (player_id, 0, game_date)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def update_game_score(self, game_id: int, final_score: int):
        """
        Update the final score for a completed game.
        
        Args:
            game_id: ID of the game
            final_score: Final calculated score
        """
        self.cursor.execute(
            "UPDATE Game SET final_score = ? WHERE game_id = ?",
            (final_score, game_id)
        )
        self.connection.commit()
    
    def get_player_games(self, player_id: int) -> List[Dict]:
        """
        Get all games for a specific player.
        
        Args:
            player_id: ID of the player
            
        Returns:
            List of game dictionaries
        """
        self.cursor.execute(
            "SELECT game_id, final_score, game_date FROM Game WHERE player_id = ? ORDER BY game_date DESC",
            (player_id,)
        )
        results = self.cursor.fetchall()
        return [
            {
                'game_id': row[0],
                'final_score': row[1],
                'game_date': row[2]
            }
            for row in results
        ]
    
    # ==================== Frame Operations ====================
    
    def add_frame(self, game_id: int, frame_number: int, roll1_pins: int,
                  roll2_pins: Optional[int] = None, roll3_pins: Optional[int] = None):
        """
        Add a frame record to the database.
        
        Args:
            game_id: ID of the game
            frame_number: Frame number (1-10)
            roll1_pins: Pins knocked down on first roll
            roll2_pins: Pins knocked down on second roll (optional)
            roll3_pins: Pins knocked down on third roll (10th frame only)
        """
        self.cursor.execute(
            "INSERT INTO Frame (game_id, frame_number, roll1_pins, roll2_pins, roll3_pins) VALUES (?, ?, ?, ?, ?)",
            (game_id, frame_number, roll1_pins, roll2_pins, roll3_pins)
        )
        self.connection.commit()
    
    def get_game_frames(self, game_id: int) -> List[Dict]:
        """
        Get all frames for a specific game.
        
        Args:
            game_id: ID of the game
            
        Returns:
            List of frame dictionaries ordered by frame number
        """
        self.cursor.execute(
            "SELECT frame_id, frame_number, roll1_pins, roll2_pins, roll3_pins FROM Frame WHERE game_id = ? ORDER BY frame_number",
            (game_id,)
        )
        results = self.cursor.fetchall()
        return [
            {
                'frame_id': row[0],
                'frame_number': row[1],
                'roll1_pins': row[2],
                'roll2_pins': row[3],
                'roll3_pins': row[4]
            }
            for row in results
        ]
    
    # ==================== Statistics Operations ====================
    
    def get_player_stats(self, player_id: int) -> Dict:
        """
        Calculate comprehensive statistics for a player.
        
        Args:
            player_id: ID of the player
            
        Returns:
            Dictionary containing player statistics
        """
        # Get all games
        games = self.get_player_games(player_id)
        
        if not games:
            return {
                'total_games': 0,
                'high_score': 0,
                'average_score': 0.0,
                'strike_percentage': 0.0
            }
        
        # Calculate basic stats
        total_games = len(games)
        scores = [game['final_score'] for game in games]
        high_score = max(scores)
        average_score = sum(scores) / total_games
        
        # Calculate strike percentage
        total_strikes = 0
        total_first_rolls = 0
        
        for game in games:
            frames = self.get_game_frames(game['game_id'])
            for frame in frames:
                if frame['roll1_pins'] is not None:
                    total_first_rolls += 1
                    if frame['roll1_pins'] == 10:
                        total_strikes += 1
        
        strike_percentage = (total_strikes / total_first_rolls * 100) if total_first_rolls > 0 else 0.0
        
        return {
            'total_games': total_games,
            'high_score': high_score,
            'average_score': round(average_score, 1),
            'strike_percentage': round(strike_percentage, 1)
        }
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()

