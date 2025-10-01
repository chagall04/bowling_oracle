"""
Live scoring screen with scorecard and input system.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QGridLayout, QFrame, QMessageBox,
                             QListWidget, QListWidgetItem, QDialog, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap
from typing import List
from database import DatabaseHandler
from scoring import GameManager, BowlingGame
import os


class PlayerSelectionDialog(QDialog):
    """Dialog for selecting players for a new game."""
    
    def __init__(self, db: DatabaseHandler, parent=None):
        """
        Initialize player selection dialog.
        
        Args:
            db: Database handler instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.db = db
        self.selected_players = []
        self.init_ui()
        self.load_players()
    
    def init_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Select Players")
        self.setMinimumSize(500, 600)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Select Players for Game")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("Click on players to select them (minimum 1, maximum 6)")
        instructions.setFont(QFont("Arial", 10))
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("color: #7f8c8d; margin: 10px;")
        layout.addWidget(instructions)
        
        # Player list
        self.player_list = QListWidget()
        self.player_list.setFont(QFont("Arial", 12))
        self.player_list.setSelectionMode(QListWidget.MultiSelection)
        self.player_list.setStyleSheet("""
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        layout.addWidget(self.player_list)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Game")
        self.start_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.start_btn.clicked.connect(self.accept_selection)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(QFont("Arial", 12))
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_players(self):
        """Load all players from database."""
        players = self.db.get_all_players()
        
        if not players:
            QMessageBox.warning(
                self,
                "No Players",
                "Please add players before starting a game!"
            )
            self.reject()
            return
        
        for player in players:
            item = QListWidgetItem(player['player_name'])
            item.setData(Qt.UserRole, player['player_id'])
            self.player_list.addItem(item)
    
    def accept_selection(self):
        """Validate and accept player selection."""
        selected_items = self.player_list.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, "No Players", "Please select at least one player!")
            return
        
        if len(selected_items) > 6:
            QMessageBox.warning(self, "Too Many Players", "Maximum 6 players allowed!")
            return
        
        self.selected_players = [
            {
                'player_id': item.data(Qt.UserRole),
                'player_name': item.text()
            }
            for item in selected_items
        ]
        
        self.accept()


class ScoringScreen(QWidget):
    """Live scoring screen with scorecard and pin input."""
    
    # Signals
    game_complete = pyqtSignal(list)  # Emits list of player results
    back_clicked = pyqtSignal()
    
    def __init__(self, db: DatabaseHandler):
        """
        Initialize the scoring screen.
        
        Args:
            db: Database handler instance
        """
        super().__init__()
        self.db = db
        self.game_manager = None
        self.frame_widgets = {}  # Store frame display widgets
        self.score_labels = {}   # Store score labels
        self.init_ui()
    
    def init_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title and current player
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("🎳 Live Scoring")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        
        self.current_player_label = QLabel("")
        self.current_player_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.current_player_label.setStyleSheet("color: #27ae60;")
        self.current_player_label.setAlignment(Qt.AlignRight)
        
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.current_player_label)
        
        layout.addLayout(header_layout)
        
        # Scorecard area (scrollable)
        self.scorecard_container = QWidget()
        self.scorecard_layout = QVBoxLayout()
        self.scorecard_container.setLayout(self.scorecard_layout)
        self.scorecard_container.setStyleSheet("background-color: white; border-radius: 10px;")
        
        layout.addWidget(self.scorecard_container, stretch=3)
        
        # Pin input area
        input_frame = QFrame()
        input_frame.setFrameStyle(QFrame.StyledPanel)
        input_frame.setStyleSheet("background-color: #ecf0f1; border-radius: 10px; padding: 15px;")
        input_layout = QVBoxLayout()
        
        self.instruction_label = QLabel("Select pins knocked down:")
        self.instruction_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.instruction_label.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(self.instruction_label)
        
        # Number pad
        numpad_layout = QGridLayout()
        numpad_layout.setSpacing(10)
        
        self.pin_buttons = []
        for i in range(11):  # 0-10
            btn = QPushButton(str(i))
            btn.setMinimumSize(60, 60)
            btn.setFont(QFont("Arial", 16, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:disabled {
                    background-color: #bdc3c7;
                    color: #7f8c8d;
                }
            """)
            btn.clicked.connect(lambda checked, pins=i: self.record_pins(pins))
            self.pin_buttons.append(btn)
            
            row = i // 4
            col = i % 4
            numpad_layout.addWidget(btn, row, col)
        
        input_layout.addLayout(numpad_layout)
        input_frame.setLayout(input_layout)
        layout.addWidget(input_frame, stretch=1)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        
        self.back_btn = QPushButton("⬅️ Back to Menu")
        self.back_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.back_btn.setMinimumHeight(40)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.back_btn.clicked.connect(self.confirm_exit)
        
        bottom_layout.addWidget(self.back_btn)
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def start_new_game(self) -> bool:
        """
        Show player selection and start a new game.
        
        Returns:
            True if game started successfully
        """
        dialog = PlayerSelectionDialog(self.db, self)
        
        if dialog.exec_() != QDialog.Accepted:
            return False
        
        # Create new game manager
        self.game_manager = GameManager()
        
        # Create game records and add players
        for player_data in dialog.selected_players:
            game_id = self.db.create_game(player_data['player_id'])
            self.game_manager.add_player(
                player_data['player_id'],
                player_data['player_name'],
                game_id
            )
        
        # Build scorecard
        self.build_scorecard()
        self.update_display()
        
        return True
    
    def build_scorecard(self):
        """Build the scorecard display for all players."""
        # Clear existing scorecard
        while self.scorecard_layout.count():
            child = self.scorecard_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.frame_widgets.clear()
        self.score_labels.clear()
        
        # Build scorecard for each player
        for player_game in self.game_manager.players:
            player_widget = self.create_player_scorecard(player_game)
            self.scorecard_layout.addWidget(player_widget)
    
    def create_player_scorecard(self, player_game: BowlingGame) -> QWidget:
        """
        Create scorecard widget for a single player.
        
        Args:
            player_game: BowlingGame instance
            
        Returns:
            QWidget containing player's scorecard
        """
        widget = QFrame()
        widget.setFrameStyle(QFrame.Box)
        widget.setStyleSheet("border: 2px solid #bdc3c7; border-radius: 5px; background-color: white; margin: 5px;")
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # Player name
        name_label = QLabel(player_game.player_name)
        name_label.setFont(QFont("Arial", 14, QFont.Bold))
        name_label.setStyleSheet("border: none; color: #2c3e50;")
        layout.addWidget(name_label)
        
        # Frames
        frames_layout = QHBoxLayout()
        frames_layout.setSpacing(2)
        
        self.frame_widgets[player_game.player_id] = []
        
        for frame_num in range(1, 11):
            frame_widget = self.create_frame_widget(frame_num)
            self.frame_widgets[player_game.player_id].append(frame_widget)
            frames_layout.addWidget(frame_widget)
        
        layout.addLayout(frames_layout)
        
        # Total score
        total_label = QLabel("Total: 0")
        total_label.setFont(QFont("Arial", 16, QFont.Bold))
        total_label.setStyleSheet("border: none; color: #27ae60;")
        total_label.setAlignment(Qt.AlignCenter)
        self.score_labels[player_game.player_id] = total_label
        layout.addWidget(total_label)
        
        widget.setLayout(layout)
        return widget
    
    def create_frame_widget(self, frame_num: int) -> QWidget:
        """
        Create a single frame display widget.
        
        Args:
            frame_num: Frame number (1-10)
            
        Returns:
            QWidget for the frame
        """
        widget = QFrame()
        widget.setFrameStyle(QFrame.Box)
        widget.setMinimumWidth(60)
        widget.setStyleSheet("border: 1px solid #95a5a6;")
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(2, 2, 2, 2)
        
        # Frame number
        num_label = QLabel(str(frame_num))
        num_label.setFont(QFont("Arial", 8))
        num_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(num_label)
        
        # Rolls display
        if frame_num == 10:
            rolls_widget = QWidget()
            rolls_layout = QHBoxLayout()
            rolls_layout.setSpacing(1)
            rolls_layout.setContentsMargins(0, 0, 0, 0)
            
            for i in range(3):
                roll_label = QLabel("")
                roll_label.setFont(QFont("Arial", 12, QFont.Bold))
                roll_label.setAlignment(Qt.AlignCenter)
                roll_label.setMinimumHeight(25)
                roll_label.setStyleSheet("border: 1px solid #bdc3c7;")
                roll_label.setObjectName(f"roll{i+1}")
                rolls_layout.addWidget(roll_label)
            
            rolls_widget.setLayout(rolls_layout)
            layout.addWidget(rolls_widget)
        else:
            rolls_widget = QWidget()
            rolls_layout = QHBoxLayout()
            rolls_layout.setSpacing(1)
            rolls_layout.setContentsMargins(0, 0, 0, 0)
            
            for i in range(2):
                roll_label = QLabel("")
                roll_label.setFont(QFont("Arial", 12, QFont.Bold))
                roll_label.setAlignment(Qt.AlignCenter)
                roll_label.setMinimumHeight(25)
                roll_label.setStyleSheet("border: 1px solid #bdc3c7;")
                roll_label.setObjectName(f"roll{i+1}")
                rolls_layout.addWidget(roll_label)
            
            rolls_widget.setLayout(rolls_layout)
            layout.addWidget(rolls_widget)
        
        # Cumulative score
        score_label = QLabel("")
        score_label.setFont(QFont("Arial", 14, QFont.Bold))
        score_label.setAlignment(Qt.AlignCenter)
        score_label.setMinimumHeight(30)
        score_label.setStyleSheet("background-color: #ecf0f1;")
        score_label.setObjectName("cumulative")
        layout.addWidget(score_label)
        
        widget.setLayout(layout)
        return widget
    
    def record_pins(self, pins: int):
        """
        Record pins knocked down for current player.
        
        Args:
            pins: Number of pins (0-10)
        """
        if not self.game_manager:
            return
        
        try:
            result = self.game_manager.record_roll(pins)
            
            # Update scorecard display
            self.update_display()
            
            # Show animation for strike/spare
            if result.get('is_strike'):
                self.show_animation('strike')
            elif result.get('is_spare'):
                self.show_animation('spare')
            
            # Check if game is complete
            if result.get('all_games_complete'):
                self.complete_game()
        
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def update_display(self):
        """Update the scorecard display with current game state."""
        if not self.game_manager:
            return
        
        current_player = self.game_manager.get_current_player()
        
        if current_player:
            self.current_player_label.setText(
                f"Current Player: {current_player.player_name} | "
                f"Frame {current_player.get_current_frame_number()} | "
                f"Roll {current_player.get_current_roll_in_frame()}"
            )
            
            # Update available pins
            max_pins = current_player.get_max_pins_for_current_roll()
            for i, btn in enumerate(self.pin_buttons):
                btn.setEnabled(i <= max_pins)
        
        # Update all player scorecards
        for player_game in self.game_manager.players:
            self.update_player_scorecard(player_game)
    
    def update_player_scorecard(self, player_game: BowlingGame):
        """
        Update scorecard for a specific player.
        
        Args:
            player_game: BowlingGame instance
        """
        frame_widgets = self.frame_widgets.get(player_game.player_id, [])
        cumulative_scores = player_game.get_cumulative_scores()
        
        for frame_num in range(10):
            if frame_num >= len(frame_widgets):
                continue
            
            frame_widget = frame_widgets[frame_num]
            rolls = player_game.frames[frame_num]
            
            # Update roll displays
            for i, roll_val in enumerate(rolls):
                roll_label = frame_widget.findChild(QLabel, f"roll{i+1}")
                if roll_label:
                    # Format display (X for strike, / for spare)
                    if frame_num < 9:  # Frames 1-9
                        if i == 0 and roll_val == 10:
                            roll_label.setText("X")
                        elif i == 1 and sum(rolls[:2]) == 10:
                            roll_label.setText("/")
                        elif roll_val == 0:
                            roll_label.setText("-")
                        else:
                            roll_label.setText(str(roll_val))
                    else:  # 10th frame
                        if roll_val == 10:
                            roll_label.setText("X")
                        elif i > 0 and len(rolls) > i and rolls[i-1] != 10 and rolls[i-1] + roll_val == 10:
                            roll_label.setText("/")
                        elif roll_val == 0:
                            roll_label.setText("-")
                        else:
                            roll_label.setText(str(roll_val))
            
            # Update cumulative score
            score_label = frame_widget.findChild(QLabel, "cumulative")
            if score_label and frame_num < len(cumulative_scores):
                score = cumulative_scores[frame_num]
                score_label.setText(str(score) if score is not None else "")
        
        # Update total score
        total_label = self.score_labels.get(player_game.player_id)
        if total_label:
            total = player_game.get_total_score()
            total_label.setText(f"Total: {total if total is not None else 0}")
    
    def show_animation(self, animation_type: str):
        """
        Show strike or spare animation.
        
        Args:
            animation_type: 'strike' or 'spare'
        """
        # This will be implemented with GIFs later
        # For now, just show a simple message
        pass
    
    def complete_game(self):
        """Handle game completion."""
        # Save final scores to database
        results = []
        
        for player_game in self.game_manager.players:
            final_score = player_game.get_total_score() or 0
            self.db.update_game_score(player_game.game_id, final_score)
            
            # Save all frames
            for frame_num, rolls in enumerate(player_game.frames, 1):
                roll1 = rolls[0] if len(rolls) > 0 else None
                roll2 = rolls[1] if len(rolls) > 1 else None
                roll3 = rolls[2] if len(rolls) > 2 else None
                self.db.add_frame(player_game.game_id, frame_num, roll1, roll2, roll3)
            
            results.append({
                'player_name': player_game.player_name,
                'player_id': player_game.player_id,
                'final_score': final_score
            })
        
        # Emit completion signal
        self.game_complete.emit(results)
    
    def confirm_exit(self):
        """Confirm before exiting an active game."""
        if self.game_manager and not self.game_manager.is_game_complete():
            reply = QMessageBox.question(
                self,
                "Exit Game",
                "Game is in progress. Exit anyway?\n(Progress will be lost)",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                return
        
        self.back_clicked.emit()

