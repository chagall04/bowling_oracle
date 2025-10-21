"""
database handler for bowling oracle
manages sqlite database operations
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class DatabaseHandler:
    """handles all database operations"""
    
    def __init__(self, db_name: str = "bowling_tracker.db"):
        """initialize database connection"""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """establish connection to sqlite database"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
    
    def _create_tables(self):
        """create database schema if tables don't exist"""
        # player table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Player (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL UNIQUE,
                date_joined TEXT NOT NULL
            )
        """)
        
        # game table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Game (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                final_score INTEGER NOT NULL,
                game_date TEXT NOT NULL,
                FOREIGN KEY (player_id) REFERENCES Player(player_id)
            )
        """)
        
        # frame table
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
    
    # Player Operations
    
    def add_player(self, player_name: str) -> int:
        """add new player to database"""
        date_joined = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO Player (player_name, date_joined) VALUES (?, ?)",
            (player_name, date_joined)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_player(self, player_id: int) -> Optional[Dict]:
        """retrieve player by id"""
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
        """retrieve all players from database"""
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
        """delete player and all their data"""
        # get all game ids for this player
        self.cursor.execute("SELECT game_id FROM Game WHERE player_id = ?", (player_id,))
        game_ids = [row[0] for row in self.cursor.fetchall()]
        
        # delete all frames for these games
        for game_id in game_ids:
            self.cursor.execute("DELETE FROM Frame WHERE game_id = ?", (game_id,))
        
        # delete all games for this player
        self.cursor.execute("DELETE FROM Game WHERE player_id = ?", (player_id,))
        
        # delete the player
        self.cursor.execute("DELETE FROM Player WHERE player_id = ?", (player_id,))
        
        self.connection.commit()
    
    def search_players(self, search_term: str) -> List[Dict]:
        """search players by name"""
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
    
    # game operations
    
    def create_game(self, player_id: int) -> int:
        """create new game for player"""
        game_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO Game (player_id, final_score, game_date) VALUES (?, ?, ?)",
            (player_id, 0, game_date)
        )
        self.connection.commit()
        return self.cursor.lastrowid
    
    def update_game_score(self, game_id: int, final_score: int):
        """update final score for completed game"""
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
    
    # frame operations
    
    def add_frame(self, game_id: int, frame_number: int, roll1_pins: int,
                  roll2_pins: Optional[int] = None, roll3_pins: Optional[int] = None):
        """add frame record to database"""
        self.cursor.execute(
            "INSERT INTO Frame (game_id, frame_number, roll1_pins, roll2_pins, roll3_pins) VALUES (?, ?, ?, ?, ?)",
            (game_id, frame_number, roll1_pins, roll2_pins, roll3_pins)
        )
        self.connection.commit()
    
    def get_game_frames(self, game_id: int) -> List[Dict]:
        """get all frames for specific game"""
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
        """get player statistics"""
        # get all games
        games = self.get_player_games(player_id)
        
        if not games:
            return {
                'total_games': 0,
                'high_score': 0,
                'average_score': 0.0,
                'strike_percentage': 0.0
            }
        
        # calculate basic stats
        total_games = len(games)
        scores = [game['final_score'] for game in games]
        high_score = max(scores)
        average_score = sum(scores) / total_games
        
        # calculate strike percentage
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
        """close database connection"""
        if self.connection:
            self.connection.close()

