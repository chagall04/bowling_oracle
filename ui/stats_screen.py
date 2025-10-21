"""
statistics screen with player performance data and charts
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QComboBox, QTableWidget, QTableWidgetItem,
                             QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from database import DatabaseHandler
from ui.sound_manager import SoundManager
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PerformanceChart(FigureCanvas):
    """matplotlib chart showing player performance over time"""
    
    def __init__(self, parent=None):
        """initialize performance chart"""
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)
        
        # Configure plot
        self.figure.patch.set_facecolor('#ecf0f1')
        self.axes.set_facecolor('white')
        self.axes.grid(True, alpha=0.3)
    
    def plot_scores(self, games_data):
        """
        Plot player scores over time.
        
        Args:
            games_data: List of game dictionaries with final_score and game_date
        """
        self.axes.clear()
        
        if not games_data:
            self.axes.text(
                0.5, 0.5, 'No game data available',
                horizontalalignment='center',
                verticalalignment='center',
                transform=self.axes.transAxes,
                fontsize=14,
                color='#7f8c8d'
            )
            self.draw()
            return
        
        # Extract data
        game_numbers = list(range(1, len(games_data) + 1))
        scores = [game['final_score'] for game in games_data]
        
        # Plot
        self.axes.plot(game_numbers, scores, marker='o', linewidth=2, 
                      markersize=6, color='#3498db', label='Score')
        
        # Add average line
        if scores:
            avg_score = sum(scores) / len(scores)
            self.axes.axhline(y=avg_score, color='#e74c3c', linestyle='--', 
                            linewidth=2, label=f'Average ({avg_score:.1f})')
        
        # Labels and title
        self.axes.set_xlabel('Game Number', fontsize=11, fontweight='bold')
        self.axes.set_ylabel('Score', fontsize=11, fontweight='bold')
        self.axes.set_title('Performance Over Time', fontsize=13, fontweight='bold')
        self.axes.legend(loc='upper left')
        self.axes.grid(True, alpha=0.3)
        
        # Set integer x-axis
        self.axes.set_xticks(game_numbers)
        
        self.figure.tight_layout()
        self.draw()


class StatsScreen(QWidget):
    """statistics screen showing player performance and history"""
    
    # Signal for navigation
    back_clicked = pyqtSignal()
    
    def __init__(self, db: DatabaseHandler):
        """initialize stats screen"""
        super().__init__()
        self.db = db
        self.sound_manager = SoundManager()
        self.current_player_id = None
        self.init_ui()
    
    def init_ui(self):
        """set up user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title with subtle wizard theme
        title_layout = QHBoxLayout()
        
        # Left subtle emoji
        left_emoji = QLabel("🔮")
        left_emoji.setFont(QFont("Arial", 18))
        left_emoji.setStyleSheet("color: #9b59b6;")
        title_layout.addWidget(left_emoji)
        
        # Main title
        title = QLabel("Player Statistics")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        title_layout.addWidget(title)
        
        # Right subtle emoji
        right_emoji = QLabel("✨")
        right_emoji.setFont(QFont("Arial", 18))
        right_emoji.setStyleSheet("color: #9b59b6;")
        title_layout.addWidget(right_emoji)
        
        layout.addLayout(title_layout)
        
        # Player selection
        selection_layout = QHBoxLayout()
        selection_label = QLabel("Select Player:")
        selection_label.setFont(QFont("Arial", 12, QFont.Bold))
        
        self.player_combo = QComboBox()
        self.player_combo.setFont(QFont("Arial", 11))
        self.player_combo.setMinimumHeight(35)
        self.player_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
            QComboBox:hover {
                border: 2px solid #3498db;
            }
        """)
        self.player_combo.currentIndexChanged.connect(self.on_player_selected)
        
        selection_layout.addWidget(selection_label)
        selection_layout.addWidget(self.player_combo, stretch=1)
        layout.addLayout(selection_layout)
        
        # Stats summary cards
        stats_container = QHBoxLayout()
        stats_container.setSpacing(10)
        
        self.high_score_label = self._create_stat_card("High Score", "0", "#27ae60")
        self.avg_score_label = self._create_stat_card("Average Score", "0.0", "#3498db")
        self.total_games_label = self._create_stat_card("Total Games", "0", "#9b59b6")
        self.strike_pct_label = self._create_stat_card("Strike %", "0%", "#e67e22")
        
        stats_container.addWidget(self.high_score_label)
        stats_container.addWidget(self.avg_score_label)
        stats_container.addWidget(self.total_games_label)
        stats_container.addWidget(self.strike_pct_label)
        
        layout.addLayout(stats_container)
        
        # Performance chart
        chart_frame = QFrame()
        chart_frame.setFrameStyle(QFrame.StyledPanel)
        chart_frame.setStyleSheet("background-color: #ecf0f1; border-radius: 10px; padding: 10px;")
        chart_layout = QVBoxLayout()
        
        chart_title = QLabel("📈 Performance Trend")
        chart_title.setFont(QFont("Arial", 14, QFont.Bold))
        chart_title.setStyleSheet("color: #2c3e50;")
        chart_layout.addWidget(chart_title)
        
        self.performance_chart = PerformanceChart()
        chart_layout.addWidget(self.performance_chart)
        
        chart_frame.setLayout(chart_layout)
        layout.addWidget(chart_frame, stretch=2)
        
        # Game history table
        history_label = QLabel("🎯 Game History")
        history_label.setFont(QFont("Arial", 14, QFont.Bold))
        history_label.setStyleSheet("color: #2c3e50; margin-top: 10px;")
        layout.addWidget(history_label)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Game #", "Date", "Score"])
        self.history_table.setFont(QFont("Arial", 11))
        self.history_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }
        """)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.history_table, stretch=1)
        
        # Back button
        self.back_btn = QPushButton("⬅️ Back to Main Menu")
        self.back_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.back_btn.setMinimumHeight(40)
        self.back_btn.setCursor(Qt.PointingHandCursor)
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
        self.back_btn.clicked.connect(self.back_clicked.emit)
        layout.addWidget(self.back_btn)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def showEvent(self, event):
        """called when screen is shown"""
        super().showEvent(event)
        if hasattr(self, 'sound_manager'):
            self.sound_manager.stop_music()
            self.sound_manager.play_menu_music()
    
    def hideEvent(self, event):
        """Called when the screen is hidden."""
        super().hideEvent(event)
        if hasattr(self, 'sound_manager'):
            self.sound_manager.stop_music()
    
    def _create_stat_card(self, title: str, value: str, color: str) -> QWidget:
        """
        Create a statistics card widget.
        
        Args:
            title: Card title
            value: Statistic value
            color: Accent color
            
        Returns:
            QWidget containing the stat card
        """
        card = QFrame()
        card.setFrameStyle(QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-left: 5px solid {color};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10))
        title_label.setStyleSheet("color: #7f8c8d;")
        title_label.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 20, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setObjectName("value")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        card.setLayout(layout)
        return card
    
    def load_players(self):
        """load all players into combo box"""
        self.player_combo.clear()
        players = self.db.get_all_players()
        
        for player in players:
            self.player_combo.addItem(player['player_name'], player['player_id'])
        
        if players:
            self.on_player_selected(0)
    
    def on_player_selected(self, index: int):
        """
        Handle player selection change.
        
        Args:
            index: Combo box index
        """
        if index < 0:
            return
        
        player_id = self.player_combo.itemData(index)
        if player_id is None:
            return
        
        self.current_player_id = player_id
        self.load_player_stats()
    
    def load_player_stats(self):
        """Load and display statistics for the current player."""
        if self.current_player_id is None:
            return
        
        # Get statistics
        stats = self.db.get_player_stats(self.current_player_id)
        
        # Update stat cards
        high_score_value = self.high_score_label.findChild(QLabel, "value")
        if high_score_value:
            high_score_value.setText(str(stats['high_score']))
        
        avg_score_value = self.avg_score_label.findChild(QLabel, "value")
        if avg_score_value:
            avg_score_value.setText(f"{stats['average_score']:.1f}")
        
        total_games_value = self.total_games_label.findChild(QLabel, "value")
        if total_games_value:
            total_games_value.setText(str(stats['total_games']))
        
        strike_pct_value = self.strike_pct_label.findChild(QLabel, "value")
        if strike_pct_value:
            strike_pct_value.setText(f"{stats['strike_percentage']:.1f}%")
        
        # Load game history
        games = self.db.get_player_games(self.current_player_id)
        
        # Reverse to show oldest first for chart
        games_for_chart = list(reversed(games))
        self.performance_chart.plot_scores(games_for_chart)
        
        # Populate history table (newest first)
        self.history_table.setRowCount(len(games))
        
        for row, game in enumerate(games):
            # Game number (reverse order, so newest is #1)
            game_num_item = QTableWidgetItem(str(len(games) - row))
            game_num_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 0, game_num_item)
            
            # Date
            date_str = game['game_date'][:10]  # Just the date part
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 1, date_item)
            
            # Score
            score_item = QTableWidgetItem(str(game['final_score']))
            score_item.setFont(QFont("Arial", 11, QFont.Bold))
            score_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 2, score_item)
        
        self.history_table.resizeColumnsToContents()
    
    def showEvent(self, event):
        """Reload players when screen is shown."""
        super().showEvent(event)
        self.load_players()

