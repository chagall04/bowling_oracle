"""
game over screen showing winner and final scores
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from typing import List, Dict
from ui.sound_manager import SoundManager


class GameOverScreen(QWidget):
    """screen shown when game is completed"""
    
    # signals
    rematch_clicked = pyqtSignal(list)  # emits list of player ids for rematch
    main_menu_clicked = pyqtSignal()
    
    def __init__(self):
        """initialize game over screen"""
        super().__init__()
        self.game_results = []
        self.sound_manager = SoundManager()  # Initialize sound system
        self.init_ui()
    
    def init_ui(self):
        """set up user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Game Over title with wizard theme
        title_layout = QHBoxLayout()
        
        # Left magic emojis
        left_magic = QLabel("🧙")
        left_magic.setFont(QFont("Arial", 24))
        left_magic.setStyleSheet("color: #9b59b6;")
        title_layout.addWidget(left_magic)
        
        # Main title with purple banner background
        self.game_over_label = QLabel("🎳 GAME OVER 🎳")
        self.game_over_label.setFont(QFont("Arial", 36, QFont.Bold))
        self.game_over_label.setAlignment(Qt.AlignCenter)
        self.game_over_label.setStyleSheet("""
            color: white; 
            background-color: #9b59b6; 
            border: 3px solid #8e44ad;
            border-radius: 15px;
            padding: 20px;
            margin: 20px;
        """)
        title_layout.addWidget(self.game_over_label)
        
        # Right magic emojis
        right_magic = QLabel("🔮")
        right_magic.setFont(QFont("Arial", 24))
        right_magic.setStyleSheet("color: #9b59b6;")
        title_layout.addWidget(right_magic)
        
        layout.addLayout(title_layout)
        
        # Winner announcement with magic theme
        self.winner_label = QLabel("")
        self.winner_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.winner_label.setAlignment(Qt.AlignCenter)
        self.winner_label.setStyleSheet("color: #27ae60; margin: 20px;")
        layout.addWidget(self.winner_label)
        
        # Magic trophy display
        trophy_layout = QHBoxLayout()
        
        # Left sparkles
        left_sparkles = QLabel("✨ ⭐")
        left_sparkles.setFont(QFont("Arial", 36))
        left_sparkles.setStyleSheet("color: #f39c12;")
        trophy_layout.addWidget(left_sparkles)
        
        # Trophy emoji for winner
        self.trophy_label = QLabel("🏆")
        self.trophy_label.setFont(QFont("Arial", 72))
        self.trophy_label.setAlignment(Qt.AlignCenter)
        trophy_layout.addWidget(self.trophy_label)
        
        # Right sparkles
        right_sparkles = QLabel("⭐ ✨")
        right_sparkles.setFont(QFont("Arial", 36))
        right_sparkles.setStyleSheet("color: #f39c12;")
        trophy_layout.addWidget(right_sparkles)
        
        layout.addLayout(trophy_layout)
        
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
        """display game results and play music"""
        self.game_results = results
        
        # sort by score (descending)
        sorted_results = sorted(results, key=lambda x: x['final_score'], reverse=True)
        
        # display winner
        if sorted_results:
            winner = sorted_results[0]
            # extract just the name without the number prefix
            winner_name = winner['player_name'].split('. ', 1)[-1] if '. ' in winner['player_name'] else winner['player_name']
            self.winner_label.setText(
                f"🎉 {winner_name} wins with {winner['final_score']} points! 🎉"
            )
        
        # start playing game over music
        self.sound_manager.play_game_over_music()
        
        # populate table
        self.scores_table.setRowCount(len(sorted_results))
        
        for row, result in enumerate(sorted_results):
            # rank
            rank_item = QTableWidgetItem(str(row + 1))
            rank_item.setFont(QFont("Arial", 12, QFont.Bold))
            rank_item.setTextAlignment(Qt.AlignCenter)
            if row == 0:
                rank_item.setBackground(Qt.yellow)
            self.scores_table.setItem(row, 0, rank_item)
            
            # player name (clean up by removing number prefix)
            player_name = result['player_name'].split('. ', 1)[-1] if '. ' in result['player_name'] else result['player_name']
            name_item = QTableWidgetItem(player_name)
            name_item.setFont(QFont("Arial", 12))
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            if row == 0:
                name_item.setFont(QFont("Arial", 12, QFont.Bold))
                name_item.setBackground(Qt.yellow)
            self.scores_table.setItem(row, 1, name_item)
            
            # score
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


