"""
Game over screen showing winner and final scores.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from typing import List, Dict
from ui.sound_manager import SoundManager


class GameOverScreen(QWidget):
    """Screen shown when a game is completed."""
    
    # Signals
    rematch_clicked = pyqtSignal(list)  # Emits list of player IDs for rematch
    main_menu_clicked = pyqtSignal()
    
    def __init__(self):
        """Initialize the game over screen."""
        super().__init__()
        self.game_results = []
        self.sound_manager = SoundManager()  # Initialize sound system
        self.init_ui()
    
    def init_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Game Over title
        self.game_over_label = QLabel("🎳 GAME OVER 🎳")
        self.game_over_label.setFont(QFont("Arial", 36, QFont.Bold))
        self.game_over_label.setAlignment(Qt.AlignCenter)
        self.game_over_label.setStyleSheet("color: #2c3e50; margin: 20px;")
        layout.addWidget(self.game_over_label)
        
        # Winner announcement
        self.winner_label = QLabel("")
        self.winner_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.winner_label.setAlignment(Qt.AlignCenter)
        self.winner_label.setStyleSheet("color: #27ae60; margin: 20px;")
        layout.addWidget(self.winner_label)
        
        # Trophy emoji for winner
        self.trophy_label = QLabel("🏆")
        self.trophy_label.setFont(QFont("Arial", 72))
        self.trophy_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.trophy_label)
        
        # Scores table
        self.scores_table = QTableWidget()
        self.scores_table.setColumnCount(3)
        self.scores_table.setHorizontalHeaderLabels(["Rank", "Player", "Score"])
        self.scores_table.setFont(QFont("Arial", 12))
        self.scores_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
        """)
        self.scores_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.scores_table.setSelectionMode(QTableWidget.NoSelection)
        self.scores_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.scores_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        self.rematch_btn = QPushButton("🔄 Rematch")
        self.rematch_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.rematch_btn.setMinimumSize(200, 60)
        self.rematch_btn.setCursor(Qt.PointingHandCursor)
        self.rematch_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.rematch_btn.clicked.connect(self.handle_rematch)
        
        self.menu_btn = QPushButton("🏠 Main Menu")
        self.menu_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.menu_btn.setMinimumSize(200, 60)
        self.menu_btn.setCursor(Qt.PointingHandCursor)
        self.menu_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.menu_btn.clicked.connect(self.handle_main_menu)
        
        button_layout.addStretch()
        button_layout.addWidget(self.rematch_btn)
        button_layout.addWidget(self.menu_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def display_results(self, results: List[Dict]):
        """
        Display game results and play leaderboard music.
        
        Args:
            results: List of dictionaries with player_name, player_id, and final_score
        """
        self.game_results = results
        
        # Sort by score (descending)
        sorted_results = sorted(results, key=lambda x: x['final_score'], reverse=True)
        
        # Display winner
        if sorted_results:
            winner = sorted_results[0]
            self.winner_label.setText(
                f"🎉 {winner['player_name']} wins with {winner['final_score']} points! 🎉"
            )
        
        # Start playing leaderboard music
        self.sound_manager.play_leaderboard_music()
        
        # Populate table
        self.scores_table.setRowCount(len(sorted_results))
        
        for row, result in enumerate(sorted_results):
            # Rank
            rank_item = QTableWidgetItem(str(row + 1))
            rank_item.setFont(QFont("Arial", 12, QFont.Bold))
            rank_item.setTextAlignment(Qt.AlignCenter)
            if row == 0:
                rank_item.setBackground(Qt.yellow)
            self.scores_table.setItem(row, 0, rank_item)
            
            # Player name
            name_item = QTableWidgetItem(result['player_name'])
            name_item.setFont(QFont("Arial", 12))
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            if row == 0:
                name_item.setFont(QFont("Arial", 12, QFont.Bold))
                name_item.setBackground(Qt.yellow)
            self.scores_table.setItem(row, 1, name_item)
            
            # Score
            score_item = QTableWidgetItem(str(result['final_score']))
            score_item.setFont(QFont("Arial", 12, QFont.Bold))
            score_item.setTextAlignment(Qt.AlignCenter)
            if row == 0:
                score_item.setBackground(Qt.yellow)
            self.scores_table.setItem(row, 2, score_item)
        
        self.scores_table.resizeColumnsToContents()
    
    def handle_rematch(self):
        """Handle rematch button click and stop music."""
        # Stop leaderboard music
        self.sound_manager.stop_music()
        
        player_ids = [result['player_id'] for result in self.game_results]
        self.rematch_clicked.emit(player_ids)
    
    def handle_main_menu(self):
        """Handle main menu button click and stop music."""
        # Stop leaderboard music
        self.sound_manager.stop_music()
        self.main_menu_clicked.emit()
    
    def hideEvent(self, event):
        """Stop music when leaving this screen."""
        self.sound_manager.stop_music()
        super().hideEvent(event)

