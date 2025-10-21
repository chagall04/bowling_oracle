"""
live scoring screen with scorecard and input system
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QGridLayout, QFrame, QMessageBox,
                             QListWidget, QListWidgetItem, QDialog, QSizePolicy,
                             QGraphicsOpacityEffect, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPixmap
from typing import List
from database import DatabaseHandler
from scoring import GameManager, BowlingGame
from ui.sound_manager import SoundManager
import os


class PlayerSelectionDialog(QDialog):
    """dialog for selecting players for new game"""
    
    def __init__(self, db: DatabaseHandler, parent=None):
        """initialize player selection dialog"""
        super().__init__(parent)
        self.db = db
        self.selected_players = []
        self.init_ui()
        self.load_players()
    
    def init_ui(self):
        """set up the user interface"""
        self.setWindowTitle("Select Players")
        self.setMinimumSize(500, 600)
        
        layout = QVBoxLayout()
        
        # title
        title = QLabel("Select Players for Game")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # instructions
        instructions = QLabel("Click on players to select them (minimum 2, maximum 6)")
        instructions.setFont(QFont("Arial", 10))
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("color: #7f8c8d; margin: 10px;")
        layout.addWidget(instructions)
        
        # sort controls
        sort_layout = QHBoxLayout()
        sort_label = QLabel("Sort by:")
        sort_label.setFont(QFont("Arial", 10))
        self.sort_combo = QComboBox()
        self.sort_combo.setFont(QFont("Arial", 10))
        self.sort_combo.addItems(["Alphabetical", "Average Score", "Date Joined"])
        self.sort_combo.currentTextChanged.connect(self.sort_players)
        
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_combo)
        sort_layout.addStretch()
        layout.addLayout(sort_layout)
        
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
        self.player_list.itemSelectionChanged.connect(self.update_selection_numbers)
        layout.addWidget(self.player_list)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Game")
        self.start_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
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
        """load all players from database"""
        self.player_list.clear()
        players = self.db.get_all_players()
        
        if not players:
            QMessageBox.warning(
                self,
                "No Players",
                "Please add players before starting a game!"
            )
            self.reject()
            return
        
        # sort players based on current selection
        self.sort_players_data(players)
        
        for player in players:
            # get player stats for display
            stats = self.db.get_player_stats(player['player_id'])
            avg_score = stats['average_score']
            
            item_text = f"{player['player_name']} (Avg: {avg_score:.1f})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, player['player_id'])
            self.player_list.addItem(item)
    
    def sort_players_data(self, players):
        """sort players based on current sort selection"""
        sort_by = self.sort_combo.currentText()
        
        if sort_by == "Alphabetical":
            players.sort(key=lambda x: x['player_name'].lower())
        elif sort_by == "Average Score":
            # sort by average score (descending)
            players.sort(key=lambda x: self.db.get_player_stats(x['player_id'])['average_score'], reverse=True)
        elif sort_by == "Date Joined":
            # sort by date joined (newest first)
            players.sort(key=lambda x: x['date_joined'], reverse=True)
    
    def sort_players(self):
        """handle sort selection change"""
        self.load_players()
    
    def update_selection_numbers(self):
        """update player list to show selection numbers"""
        selected_items = self.player_list.selectedItems()
        
        # clear all numbers first
        for i in range(self.player_list.count()):
            item = self.player_list.item(i)
            text = item.text()
            # remove any existing number prefix
            if text.startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ')):
                text = text[3:]  # Remove "X. " prefix
            item.setText(text)
        
        # add numbers to selected items
        for i, item in enumerate(selected_items, 1):
            text = item.text()
            if not text.startswith(f'{i}. '):
                item.setText(f'{i}. {text}')
    
    def accept_selection(self):
        """validate and accept player selection"""
        selected_items = self.player_list.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, "No Players", "Please select at least one player!")
            return
        
        if len(selected_items) == 1:
            QMessageBox.warning(self, "Single Player", "Please select at least 2 players for a competitive game!")
            return
        
        if len(selected_items) > 6:
            QMessageBox.warning(self, "Too Many Players", "Maximum 6 players allowed!")
            return
        
        self.selected_players = [
            {
                'player_id': item.data(Qt.UserRole),
                'player_name': item.text().split(' (Avg:')[0]  # remove avg from name
            }
            for item in selected_items
        ]
        
        self.accept()


class ScoringScreen(QWidget):
    """live scoring screen with scorecard and pin input"""
    
    # signals
    game_complete = pyqtSignal(list)  # emits list of player results
    back_clicked = pyqtSignal()
    
    def __init__(self, db: DatabaseHandler):
        """initialize the scoring screen"""
        super().__init__()
        self.db = db
        self.game_manager = None
        self.frame_widgets = {}  # store frame display widgets
        self.score_labels = {}   # store score labels
        self.sound_manager = SoundManager()  # initialize sound system
        self.frame_counter_frozen = False  # add frame counter freeze mechanism
        self.game_complete_pending = False  # flag to track pending game completion
        self.init_ui()
    
    def init_ui(self):
        """set up the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # title and current player with wizard theme
        header_layout = QHBoxLayout()
        
        # title with magic emojis
        title_layout = QHBoxLayout()
        
        # left magic emojis
        left_magic = QLabel("✨🔮🧙")
        left_magic.setFont(QFont("Arial", 14))
        left_magic.setStyleSheet("color: #9b59b6;")
        title_layout.addWidget(left_magic)
        
        # main title
        self.title_label = QLabel("🔮 LIVE SCORE TRACKER 🎳")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setStyleSheet("color: #2c3e50; background: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.title_label)
        
        # right magic emojis
        right_magic = QLabel("🧙🔮✨")
        right_magic.setFont(QFont("Arial", 14))
        right_magic.setStyleSheet("color: #9b59b6;")
        title_layout.addWidget(right_magic)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        self.current_player_label = QLabel("")
        self.current_player_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.current_player_label.setStyleSheet("color: #9b59b6;")
        self.current_player_label.setAlignment(Qt.AlignRight)
        
        header_layout.addWidget(self.current_player_label)
        
        # add header layout to main layout at the top
        layout.addLayout(header_layout)
        
        # set styling with purple colors but no grey backgrounds
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: #2c3e50;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        
        # scorecard area
        from PyQt5.QtWidgets import QScrollArea, QSizePolicy
        self.scorecard_container = QWidget()
        self.scorecard_layout = QVBoxLayout()
        self.scorecard_layout.setSpacing(10)
        self.scorecard_layout.setContentsMargins(10, 10, 10, 10)
        self.scorecard_container.setLayout(self.scorecard_layout)
        self.scorecard_container.setStyleSheet("background-color: white; border-radius: 10px;")
        self.scorecard_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameStyle(QFrame.NoFrame)
        scroll.setWidget(self.scorecard_container)
        layout.addWidget(scroll, stretch=3)
        
        # pin input area
        input_frame = QFrame()
        input_frame.setFrameStyle(QFrame.StyledPanel)
        input_frame.setStyleSheet("background-color: #ecf0f1; border-radius: 10px; padding: 15px;")
        input_layout = QVBoxLayout()
        
        self.instruction_label = QLabel("Select pins knocked down:")
        self.instruction_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.instruction_label.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(self.instruction_label)
        
        # number pad
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
                    background-color: #9b59b6;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #8e44ad;
                }
                QPushButton:pressed {
                    background-color: #7d3c98;
                }
                QPushButton:disabled {
                    background-color: #bdc3c7;
                    color: #7f8c8d;
                }
            """)
            btn.clicked.connect(lambda checked, pins=i: self.on_pin_button_clicked(pins))
            self.pin_buttons.append(btn)
            
            row = i // 4
            col = i % 4
            numpad_layout.addWidget(btn, row, col)
        
        input_layout.addLayout(numpad_layout)
        
        input_frame.setLayout(input_layout)
        layout.addWidget(input_frame, stretch=1)
        
        # bottom buttons
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
        """show player selection and start a new game"""
        dialog = PlayerSelectionDialog(self.db, self)
        
        if dialog.exec_() != QDialog.Accepted:
            return False
        
        # create new game manager
        self.game_manager = GameManager()
        # track per-player consecutive strikes
        self.player_id_to_consecutive_strikes = {}
        
        # create game records and add players
        for player_data in dialog.selected_players:
            game_id = self.db.create_game(player_data['player_id'])
            self.game_manager.add_player(
                player_data['player_id'],
                player_data['player_name'],
                game_id
            )
            self.player_id_to_consecutive_strikes[player_data['player_id']] = 0
        
        # build scorecard
        self.build_scorecard()
        self.update_display()
        
        # start background music
        try:
            self.sound_manager.stop_music()  # stop any existing music first
            self.sound_manager.play_game_music()
        except Exception as e:
            pass
        
        return True
    
    def build_scorecard(self):
        """build the scorecard display for all players"""
        # clear existing scorecard
        while self.scorecard_layout.count():
            child = self.scorecard_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.frame_widgets.clear()
        self.score_labels.clear()
        
        # build scorecard for each player
        for player_game in self.game_manager.players:
            player_widget = self.create_player_scorecard(player_game)
            self.scorecard_layout.addWidget(player_widget)
    
    def create_player_scorecard(self, player_game: BowlingGame) -> QWidget:
        """create scorecard widget for a single player"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.Box)
        widget.setStyleSheet("border: 2px solid #9b59b6; border-radius: 5px; background-color: white; margin: 5px;")
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # player name
        name_label = QLabel(player_game.player_name)
        name_label.setFont(QFont("Arial", 14, QFont.Bold))
        name_label.setStyleSheet("border: none; color: #2c3e50;")
        layout.addWidget(name_label)
        
        # frames
        frames_layout = QHBoxLayout()
        frames_layout.setSpacing(2)
        
        self.frame_widgets[player_game.player_id] = []
        
        for frame_num in range(1, 11):
            frame_widget = self.create_frame_widget(frame_num)
            self.frame_widgets[player_game.player_id].append(frame_widget)
            frames_layout.addWidget(frame_widget)
        
        layout.addLayout(frames_layout)
        
        # total score
        total_label = QLabel("Total: 0")
        total_label.setFont(QFont("Arial", 16, QFont.Bold))
        total_label.setStyleSheet("border: none; color: #9b59b6;")
        total_label.setAlignment(Qt.AlignCenter)
        self.score_labels[player_game.player_id] = total_label
        layout.addWidget(total_label)
        
        widget.setLayout(layout)
        return widget
    
    def create_frame_widget(self, frame_num: int) -> QWidget:
        """create a single frame display widget"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.Box)
        widget.setMinimumWidth(60)
        widget.setStyleSheet("border: 1px solid #95a5a6;")
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(2, 2, 2, 2)
        
        # frame number
        num_label = QLabel(str(frame_num))
        num_label.setFont(QFont("Arial", 8))
        num_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(num_label)
        
        # rolls display
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
        
        # cumulative score
        score_label = QLabel("")
        score_label.setFont(QFont("Arial", 14, QFont.Bold))
        score_label.setAlignment(Qt.AlignCenter)
        score_label.setMinimumHeight(30)
        score_label.setStyleSheet("background-color: #ecf0f1;")
        score_label.setObjectName("cumulative")
        layout.addWidget(score_label)
        
        widget.setLayout(layout)
        return widget
    
    def on_pin_button_clicked(self, pins: int):
        """handle pin button click with sound effect"""
        # play pin knock sound for non-gutter balls
        if pins > 0:
            self.sound_manager.play_pin_knock()
        
        # record pins
        self.record_pins(pins)
    
    
    def record_pins(self, pins: int):
        """record pins knocked down for current player"""
        if not self.game_manager:
            return
        
        try:
            # capture the player who is about to roll so we can show animations
            try:
                rolling_player_game = self.game_manager.players[self.game_manager.current_player_index]
            except Exception:
                rolling_player_game = None

            result = self.game_manager.record_roll(pins)
            
            # update scorecard display
            self.update_display()
            
            # show animation and play sound for strike/spare
            if result.get('is_strike'):
                try:
                    # freeze frame counter during animation
                    self.freeze_frame_counter()
                    
                    # maintain simple consecutive strike counter per player
                    if not hasattr(self, 'player_id_to_consecutive_strikes'):
                        self.player_id_to_consecutive_strikes = {}
                    
                    # get the player who just rolled (from the result)
                    player_name = result.get('player_name', '')
                    
                    # find the player by name (more reliable than using rolling_player_game)
                    current_player = None
                    for player in self.game_manager.players:
                        if player.player_name == player_name:
                            current_player = player
                            break
                    
                    if current_player:
                        pid = current_player.player_id
                        
                        # increment consecutive strike counter (works for both regular and 10th frame bonus rolls)
                        old_count = self.player_id_to_consecutive_strikes.get(pid, 0)
                        self.player_id_to_consecutive_strikes[pid] = old_count + 1
                        consecutive_count = self.player_id_to_consecutive_strikes[pid]
                    else:
                        consecutive_count = 1
                    self.show_animation('strike', consecutive_count)
                    
                    # play appropriate sound
                    if consecutive_count == 12:
                        self.sound_manager.play_perfect_game()
                    else:
                        self.sound_manager.play_strike()
                    
                    # unfreeze frame counter after animation completes
                    # regular animations: 3 seconds + 0.5 second fade = 3.5 seconds
                    # perfect game: 4 seconds + 0.5 second fade = 4.5 seconds
                    animation_duration = 4500 if consecutive_count == 12 else 3500
                    QTimer.singleShot(animation_duration, self.unfreeze_frame_counter)
                except Exception as anim_error:
                    # unfreeze even if there's an error
                    animation_duration = 4500 if consecutive_count == 12 else 3500
                    QTimer.singleShot(animation_duration, self.unfreeze_frame_counter)
            elif result.get('is_spare'):
                try:
                    # freeze frame counter during animation
                    self.freeze_frame_counter()
                    # DON'T reset consecutive strikes on spare
                    self.show_animation('spare')
                    self.sound_manager.play_spare()
                    # unfreeze frame counter after spare animation (2 seconds + 0.5 second fade)
                    QTimer.singleShot(2500, self.unfreeze_frame_counter)
                except Exception:
                    QTimer.singleShot(2500, self.unfreeze_frame_counter)
            elif pins == 0:
                try:
                    # freeze frame counter during animation
                    self.freeze_frame_counter()
                    self.show_animation('gutter')
                    self.sound_manager.play_gutter_ball()
                    # unfreeze frame counter after gutter animation (1.5 seconds + 0.5 second fade)
                    QTimer.singleShot(2000, self.unfreeze_frame_counter)
                except Exception:
                    QTimer.singleShot(2000, self.unfreeze_frame_counter)
            else:
                # only reset consecutive strikes on actual non-strike
                if not result.get('is_strike', False) and not result.get('is_spare', False):
                    if hasattr(self, 'player_id_to_consecutive_strikes'):
                        player_name = result.get('player_name', '')
                        for player in self.game_manager.players:
                            if player.player_name == player_name:
                                # only reset if this is NOT a strike and NOT a spare
                                # strikes and spares should never reset the counter
                                old_count = self.player_id_to_consecutive_strikes.get(player.player_id, 0)
                                self.player_id_to_consecutive_strikes[player.player_id] = 0
                                break
                # play pin knock sound for regular rolls
                if pins > 0:
                    self.sound_manager.play_pin_knock()
            
            # check if game is complete to trigger end screen
            if result.get('all_games_complete'):
                # add a small delay before showing game over screen
                QTimer.singleShot(1000, self.complete_game)
        
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def freeze_frame_counter(self):
        """freeze the frame counter display and disable pin buttons"""
        self.frame_counter_frozen = True
        # Disable all pin buttons
        for btn in self.pin_buttons:
            btn.setEnabled(False)
    
    def unfreeze_frame_counter(self):
        """unfreeze the frame counter display and re-enable pin buttons"""
        self.frame_counter_frozen = False
        # re-enable pin buttons based on current game state
        if self.game_manager and hasattr(self.game_manager, 'get_current_player'):
            try:
                current_player = self.game_manager.get_current_player()
                if current_player and not current_player.is_complete:
                    max_pins = current_player.get_max_pins_for_current_roll()
                    for i, btn in enumerate(self.pin_buttons):
                        btn.setEnabled(i <= max_pins)
                else:
                    # if no current player or game complete, disable all buttons
                    for btn in self.pin_buttons:
                        btn.setEnabled(False)
            except Exception as e:
                pass
        else:
            # no game manager, disable all buttons
            for btn in self.pin_buttons:
                btn.setEnabled(False)
        
        self.update_display()  # refresh display
    
    def update_display(self):
        """update the scorecard display with current game state"""
        if not self.game_manager:
            return
        
        current_player = self.game_manager.get_current_player()
        
        if current_player and not self.frame_counter_frozen:
            # shorten player name if too long
            player_name = current_player.player_name
            if len(player_name) > 15:
                player_name = player_name[:12] + "..."
            
            self.current_player_label.setText(
                f"Player: {player_name} | "
                f"Frame {current_player.get_current_frame_number()} | "
                f"Roll {current_player.get_current_roll_in_frame()}"
            )
            
            # update available pins
            max_pins = current_player.get_max_pins_for_current_roll()
            for i, btn in enumerate(self.pin_buttons):
                btn.setEnabled(i <= max_pins)
        else:
            # no current player or frame counter frozen
            for btn in self.pin_buttons:
                btn.setEnabled(False)
        
        # update all player scorecards
        for player_game in self.game_manager.players:
            self.update_player_scorecard(player_game)
    
    def update_player_scorecard(self, player_game: BowlingGame):
        """update scorecard for a specific player"""
        frame_widgets = self.frame_widgets.get(player_game.player_id, [])
        cumulative_scores = player_game.get_cumulative_scores()
        
        for frame_num in range(10):
            if frame_num >= len(frame_widgets):
                continue
            
            frame_widget = frame_widgets[frame_num]
            rolls = player_game.frames[frame_num]
            
            # update roll displays
            for i, roll_val in enumerate(rolls):
                roll_label = frame_widget.findChild(QLabel, f"roll{i+1}")
                if roll_label:
                    # format display (X for strike, / for spare)
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
            
            # update cumulative score (with provisional for strike/spare)
            score_label = frame_widget.findChild(QLabel, "cumulative")
            if score_label:
                # only show cumulative score if this frame has been played
                if rolls:  # frame has been started
                    # calculate cumulative score for this specific frame only
                    cumulative_score = 0
                    for k in range(frame_num + 1): # Sum up to current frame (inclusive)
                        cumulative_score += player_game.get_provisional_frame_score(k)
                    
                    score_label.setText(str(cumulative_score))
                else:
                    # frame hasn't been played yet, show empty
                    score_label.setText("")
        
        # update total score
        total_label = self.score_labels.get(player_game.player_id)
        if total_label:
            # use the same provisional scoring logic as individual frames
            total_score = 0
            for i in range(10):
                total_score += player_game.get_provisional_frame_score(i)
            
            total_label.setText(f"Total: {total_score}")
    
    def show_animation(self, animation_type: str, consecutive_count: int = 1):
        """show strike or spare animation"""
        try:
            from ui.animations import AnimationWidget
            
            # clean up any existing animation widget
            if hasattr(self, 'animation_widget') and self.animation_widget:
                try:
                    self.animation_widget.hide()
                    # don't delete immediately
                except:
                    pass
            
            # create and show animation widget as overlay
            self.animation_widget = AnimationWidget(self)
            
            # position manually instead of adding to layout
            self.animation_widget.setParent(self)
            
            if animation_type == 'strike':
                self.animation_widget.show_strike(consecutive_count)
            elif animation_type == 'spare':
                self.animation_widget.show_spare()
            elif animation_type == 'gutter':
                self.animation_widget.show_gutter_ball()
            
            # force update the widget
            self.animation_widget.update()
            self.animation_widget.repaint()
            
        except Exception as e:
            pass
    
    def _emit_game_complete(self, results):
        """emit the game complete signal after animation delay"""
        self.game_complete.emit(results)
    
    def get_consecutive_strikes(self, player_game) -> int:
        """count consecutive strikes at the end of the player's game"""
        consecutive = 0
        # check frames in reverse order
        for i in range(len(player_game.frames) - 1, -1, -1):
            frame = player_game.frames[i]
            if frame and frame[0] == 10:  # strike
                consecutive += 1
            else:
                break
        return consecutive
    
    def show_consecutive_strike_animation(self, consecutive_count: int):
        """show appropriate animation for consecutive strikes"""
        try:
            from ui.animations import AnimationWidget
            
            # create and show animation widget
            self.animation_widget = AnimationWidget(self)
            
            # add to main layout as overlay
            self.layout().addWidget(self.animation_widget)
            
            if consecutive_count == 2:
                self.animation_widget.show_double()
            elif consecutive_count == 3:
                self.animation_widget.show_turkey()
            elif consecutive_count == 4:
                self.animation_widget.show_hambone()
            elif consecutive_count >= 5:
                self.animation_widget.show_x_bagger(consecutive_count)
        except Exception as e:
            pass
    
    def complete_game(self):
        """handle game completion"""
        try:
            # save final scores to database
            results = []
            
            for player_game in self.game_manager.players:
                
                # force calculate total score for completed game
                total = 0
                for i in range(10):
                    frame_score = player_game.calculate_frame_score(i)
                    if frame_score is not None:
                        total += frame_score
                
                final_score = total
                
                # update game score in database
                try:
                    self.db.update_game_score(player_game.game_id, final_score)
                except Exception as db_error:
                    pass
                
                # save all frames
                try:
                    for frame_num, rolls in enumerate(player_game.frames, 1):
                        roll1 = rolls[0] if len(rolls) > 0 else None
                        roll2 = rolls[1] if len(rolls) > 1 else None
                        roll3 = rolls[2] if len(rolls) > 2 else None
                        self.db.add_frame(player_game.game_id, frame_num, roll1, roll2, roll3)
                except Exception as frame_error:
                    pass
                
                results.append({
                    'player_name': player_game.player_name,
                    'player_id': player_game.player_id,
                    'final_score': final_score
                })
            
            
            # wait for animations to finish before transitioning to end menu
            # perfect game animations take 4 seconds + 0.5 second fade = 4.5 seconds
            animation_delay = 3000  # 3 seconds - reduced for faster transition
            
            QTimer.singleShot(animation_delay, lambda: self._emit_game_complete(results))
            
        except Exception as e:
            
            # emit the signal with basic results
            results = []
            for player_game in self.game_manager.players:
                results.append({
                    'player_name': player_game.player_name,
                    'player_id': player_game.player_id,
                    'final_score': player_game.get_total_score() or 0
                })
            self.game_complete.emit(results)
    
    def confirm_exit(self):
        """confirm before exiting an active game"""
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
        
        # stop background music
        try:
            self.sound_manager.stop_music()
        except:
            pass
        
        self.back_clicked.emit()

